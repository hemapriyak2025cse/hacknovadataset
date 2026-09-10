"""
ML Training Script — Operational Service Risk Prediction
=========================================================
This is NOT a mechanical failure predictor.
There is no genuine failure/breakdown label in the existing datasets.

This model predicts OPERATIONAL SERVICE RISK LEVEL (LOW / MEDIUM / HIGH / CRITICAL)
for a bus at a given hour, using:
  - Bus speed (from gps_service demo speeds)
  - Passenger load (aggregated from passenger_tickets.csv)
  - Hour of day, day of week (from boarding_date)
  - Route ID (categorical)
  - Weather features: temperature, precipitation, wind speed, weather code
    (from open-meteo CSV, matched by hour-of-day average)

Target label is derived using the SAME weighted heuristic as risk_service.py
(speed + passenger + weather factors) so the ML model learns to replicate and
generalise that scoring logic from features alone — without calling the heuristic
at inference time.

Chronological split: train on 2026-09-01 to 2026-09-10, test on 2026-09-11 to 2026-09-14.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "backend"))

import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight

# ── Paths ──────────────────────────────────────────────────────────────────────
DATASETS_DIR = ROOT / "Datasets"
MODELS_DIR = ROOT / "backend" / "models"
MODELS_DIR.mkdir(exist_ok=True)

# ── Demo bus speeds (mirrors gps_service.py exactly) ──────────────────────────
DEMO_SPEEDS = {
    "B101": 12.0, "B102": 28.0, "B103": 5.0,
    "B201": 22.0, "B202": 18.0, "B203": 31.0,
    "B301": 8.0,  "B302": 25.0, "B303": 19.0,
    "B401": 14.0, "B402": 27.0, "B403": 6.0,
    "B501": 20.0, "B502": 11.0, "B503": 33.0,
}

# ── Load datasets ──────────────────────────────────────────────────────────────
print("Loading datasets...")
tickets = pd.read_csv(DATASETS_DIR / "passenger_tickets.csv")
route_stops = pd.read_csv(DATASETS_DIR / "route_stops.csv")
weather_raw = pd.read_csv(ROOT / "open-meteo-11.00N76.99E431m.csv", skiprows=2)
weather_raw.columns = ["time", "temperature_c", "precipitation_mm", "wind_speed_kmh", "weather_code"]
weather_raw["time"] = pd.to_datetime(weather_raw["time"])
weather_raw["hour"] = weather_raw["time"].dt.hour

# ── Weather: compute per-hour averages across the full year ───────────────────
weather_hourly = weather_raw.groupby("hour").agg(
    temperature_c=("temperature_c", "mean"),
    precipitation_mm=("precipitation_mm", "mean"),
    wind_speed_kmh=("wind_speed_kmh", "mean"),
    weather_code=("weather_code", lambda x: x.mode()[0]),  # most common code per hour
).reset_index()

def weather_risk_factor(code: int, precip: float, wind: float) -> float:
    """Mirrors weather_service._weather_risk exactly."""
    risk = 0.0
    if code in (95, 96, 99):
        risk += 0.5
    elif code in (61, 63, 65, 80, 81, 82):
        risk += 0.3
    elif code in (45, 48):
        risk += 0.2
    if precip > 5:
        risk += 0.2
    elif precip > 1:
        risk += 0.1
    if wind > 40:
        risk += 0.2
    elif wind > 20:
        risk += 0.1
    return round(min(risk, 1.0), 2)

weather_hourly["weather_risk_factor"] = weather_hourly.apply(
    lambda r: weather_risk_factor(int(r["weather_code"]), r["precipitation_mm"], r["wind_speed_kmh"]),
    axis=1,
)

# ── Merge stop sequences into tickets ─────────────────────────────────────────
seq = route_stops[["route_id", "stop_id", "stop_sequence"]].copy()
tickets = tickets.merge(
    seq.rename(columns={"stop_id": "source_stop", "stop_sequence": "source_seq"}),
    on=["route_id", "source_stop"], how="left"
).merge(
    seq.rename(columns={"stop_id": "destination_stop", "stop_sequence": "dest_seq"}),
    on=["route_id", "destination_stop"], how="left"
)

tickets["hour"] = tickets["boarding_time"].str.split(":").str[0].astype(int)
tickets["trip_length"] = tickets["dest_seq"] - tickets["source_seq"]
tickets["boarding_date"] = pd.to_datetime(tickets["boarding_date"], dayfirst=True)
tickets["day_of_week"] = tickets["boarding_date"].dt.dayofweek

# ── Aggregate passengers per bus × date × hour ────────────────────────────────
agg = tickets.groupby(["bus_id", "route_id", "boarding_date", "hour", "day_of_week"]).agg(
    total_passengers=("passenger_count", "sum"),
    avg_trip_length=("trip_length", "mean"),
    ticket_count=("ticket_id", "count"),
).reset_index()

# ── Attach bus speed with realistic hour-based variation ─────────────────────
# Peak hours (7-9, 17-19) reduce speed by up to 60%; off-peak restore it.
# This mirrors real urban bus behaviour and generates HIGH/CRITICAL samples.
def adjusted_speed(bus_id: str, hour: int) -> float:
    base = DEMO_SPEEDS.get(bus_id, 20.0)
    # Peak congestion: speed drops significantly
    if hour in (7, 8, 9):
        factor = 0.35  # morning peak — heavy congestion
    elif hour in (17, 18, 19):
        factor = 0.40  # evening peak
    elif hour in (10, 11, 12, 13, 14, 15, 16):
        factor = 0.85  # off-peak — near normal
    else:
        factor = 1.0   # early morning / late evening — free flow
    return round(base * factor, 1)

agg["speed_kmph"] = agg.apply(lambda r: adjusted_speed(r["bus_id"], r["hour"]), axis=1)

# ── Attach weather features ────────────────────────────────────────────────────
agg = agg.merge(weather_hourly, on="hour", how="left")

# ── Derive risk label using the SAME heuristic as risk_service.py ─────────────
def compute_risk_label(row) -> str:
    score = 0.0

    # Speed factor (0-35 pts)
    spd = row["speed_kmph"]
    if spd <= 5:
        score += 35
    elif spd < 15:
        score += 22
    elif spd < 25:
        score += 10

    # Traffic delay proxy from hour (0-25 pts)
    # Peak hours imply significant traffic delay
    hour = row["hour"]
    if hour in (8, 9, 18, 19):
        traffic_delay = 18.0   # severe peak
    elif hour in (7, 17):
        traffic_delay = 10.0   # moderate peak
    elif hour in (10, 16):
        traffic_delay = 5.0    # shoulder
    else:
        traffic_delay = 0.0

    if traffic_delay > 15:
        score += 25
    elif traffic_delay > 8:
        score += 15
    elif traffic_delay > 3:
        score += 8

    # Passenger load factor (0-25 pts)
    pax = row["total_passengers"]
    if pax > 50:
        score += 25
    elif pax > 20:
        score += 15
    elif pax > 5:
        score += 8

    # Weather factor (0-20 pts)
    wrf = row["weather_risk_factor"]
    score += round(wrf * 20)

    score = min(round(score), 100)

    if score >= 75:
        return "CRITICAL"
    elif score >= 50:
        return "HIGH"
    elif score >= 25:
        return "MEDIUM"
    else:
        return "LOW"

print("Computing risk labels...")
agg["risk_label"] = agg.apply(compute_risk_label, axis=1)

print("\nLabel distribution:")
print(agg["risk_label"].value_counts())
print(f"\nTotal samples: {len(agg)}")

# ── Chronological split ────────────────────────────────────────────────────────
# Train: 2026-09-01 to 2026-09-10 (10 days)
# Test:  2026-09-11 to 2026-09-14 (4 days)
SPLIT_DATE = pd.Timestamp("2026-09-11")
train_df = agg[agg["boarding_date"] < SPLIT_DATE].copy()
test_df  = agg[agg["boarding_date"] >= SPLIT_DATE].copy()

print(f"\nTrain samples: {len(train_df)} | Test samples: {len(test_df)}")
print("Train label dist:", train_df["risk_label"].value_counts().to_dict())
print("Test label dist: ", test_df["risk_label"].value_counts().to_dict())

# ── Features ───────────────────────────────────────────────────────────────────
NUMERIC_FEATURES = [
    "speed_kmph",
    "total_passengers",
    "avg_trip_length",
    "ticket_count",
    "hour",
    "day_of_week",
    "temperature_c",
    "precipitation_mm",
    "wind_speed_kmh",
    "weather_risk_factor",
]
CATEGORICAL_FEATURES = ["route_id"]
ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "risk_label"

X_train = train_df[ALL_FEATURES]
y_train = train_df[TARGET]
X_test  = test_df[ALL_FEATURES]
y_test  = test_df[TARGET]

# ── Preprocessor ──────────────────────────────────────────────────────────────
preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), NUMERIC_FEATURES),
    ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), CATEGORICAL_FEATURES),
])

# ── Class weights ─────────────────────────────────────────────────────────────
classes = np.array(["CRITICAL", "HIGH", "LOW", "MEDIUM"])
present_classes = np.array(sorted(y_train.unique()))
weights = compute_class_weight("balanced", classes=present_classes, y=y_train)
class_weight_dict = dict(zip(present_classes, weights))
print(f"\nClass weights: {class_weight_dict}")

# ── Model ──────────────────────────────────────────────────────────────────────
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_leaf=3,
        class_weight=class_weight_dict,
        random_state=42,
        n_jobs=-1,
    )),
])

print("\nTraining RandomForestClassifier...")
model.fit(X_train, y_train)

# ── Evaluation ────────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("\n" + "="*60)
print("EVALUATION RESULTS (Test set: 2026-09-11 to 2026-09-14)")
print("="*60)
print(f"Accuracy: {acc:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=sorted(y_test.unique())))

# ── Feature importances ───────────────────────────────────────────────────────
rf = model.named_steps["classifier"]
importances = pd.Series(
    rf.feature_importances_,
    index=NUMERIC_FEATURES + CATEGORICAL_FEATURES
).sort_values(ascending=False)
print("\nTop Feature Importances:")
print(importances.to_string())

# ── Save artifacts ─────────────────────────────────────────────────────────────
print(f"\nSaving model to {MODELS_DIR}/risk_model.joblib ...")
joblib.dump(model, MODELS_DIR / "risk_model.joblib")

# Save feature metadata for predict.py
feature_meta = {
    "numeric_features": NUMERIC_FEATURES,
    "categorical_features": CATEGORICAL_FEATURES,
    "all_features": ALL_FEATURES,
    "target": TARGET,
    "label_order": ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
    "demo_speeds": DEMO_SPEEDS,
    "weather_hourly": weather_hourly.to_dict(orient="records"),
}
joblib.dump(feature_meta, MODELS_DIR / "feature_meta.joblib")

print("Saved: risk_model.joblib, feature_meta.joblib")
print("\nDone.")
