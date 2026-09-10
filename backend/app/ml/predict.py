"""
ML Prediction Module — Operational Service Risk Prediction
===========================================================
Loads the pre-trained RandomForest model and feature metadata.
Does NOT retrain on every call.

Usage:
    from app.ml.predict import predict_risk

    result = predict_risk(
        bus_id="B101",
        route_id="R01",
        hour=9,
        day_of_week=2,
        total_passengers=18,
        avg_trip_length=3.5,
        ticket_count=8,
    )
"""

from pathlib import Path
from functools import lru_cache
from typing import Optional

import numpy as np
import pandas as pd
import joblib

MODELS_DIR = Path(__file__).resolve().parents[3] / "backend" / "models"

# Risk level → numeric for ordering
_LEVEL_ORDER = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}


@lru_cache(maxsize=1)
def _load_artifacts():
    """Load model and feature metadata once, cache in memory."""
    model_path = MODELS_DIR / "risk_model.joblib"
    meta_path = MODELS_DIR / "feature_meta.joblib"

    if not model_path.exists() or not meta_path.exists():
        raise FileNotFoundError(
            f"Model files not found in {MODELS_DIR}. "
            "Run: python -m app.ml.train"
        )

    model = joblib.load(model_path)
    meta = joblib.load(meta_path)
    weather_df = pd.DataFrame(meta["weather_hourly"])
    return model, meta, weather_df


def _get_weather_for_hour(weather_df: pd.DataFrame, hour: int) -> dict:
    rows = weather_df[weather_df["hour"] == hour]
    if rows.empty:
        rows = weather_df
    row = rows.iloc[0]
    return {
        "temperature_c": float(row["temperature_c"]),
        "precipitation_mm": float(row["precipitation_mm"]),
        "wind_speed_kmh": float(row["wind_speed_kmh"]),
        "weather_risk_factor": float(row["weather_risk_factor"]),
    }


def _feature_importances(model, meta: dict) -> list[dict]:
    """Return top feature importances from the trained RF."""
    try:
        rf = model.named_steps["classifier"]
        importances = rf.feature_importances_
        features = meta["all_features"]
        pairs = sorted(zip(features, importances), key=lambda x: -x[1])
        return [{"feature": f, "importance": round(float(v), 4)} for f, v in pairs[:5]]
    except Exception:
        return []


def predict_risk(
    bus_id: str,
    route_id: str,
    hour: int,
    day_of_week: int,
    total_passengers: int,
    avg_trip_length: float = 3.0,
    ticket_count: int = 5,
    speed_kmph: Optional[float] = None,
) -> dict:
    """
    Predict operational service risk for a bus at a given hour.

    Parameters
    ----------
    bus_id          : Bus identifier (e.g. "B101")
    route_id        : Route identifier (e.g. "R01")
    hour            : Hour of day (0-23)
    day_of_week     : Day of week (0=Monday, 6=Sunday)
    total_passengers: Total passengers on this bus at this hour
    avg_trip_length : Average trip length in stops
    ticket_count    : Number of ticket transactions
    speed_kmph      : Bus speed; if None, uses demo speed for bus_id

    Returns
    -------
    dict with risk_score, risk_level, prediction, top_reasons, feature_importances
    """
    model, meta, weather_df = _load_artifacts()

    # Resolve speed
    demo_speeds = meta["demo_speeds"]
    if speed_kmph is None:
        speed_kmph = demo_speeds.get(bus_id, 20.0)

    # Weather features for this hour
    w = _get_weather_for_hour(weather_df, hour)

    # Build feature row
    row = pd.DataFrame([{
        "speed_kmph": speed_kmph,
        "total_passengers": total_passengers,
        "avg_trip_length": avg_trip_length,
        "ticket_count": ticket_count,
        "hour": hour,
        "day_of_week": day_of_week,
        "temperature_c": w["temperature_c"],
        "precipitation_mm": w["precipitation_mm"],
        "wind_speed_kmh": w["wind_speed_kmh"],
        "weather_risk_factor": w["weather_risk_factor"],
        "route_id": route_id,
    }])

    # Predict
    prediction = model.predict(row)[0]
    proba = model.predict_proba(row)[0]
    classes = model.classes_

    # Build probability dict
    proba_dict = {cls: round(float(p), 4) for cls, p in zip(classes, proba)}

    # Risk score: weighted average of level order × probability
    risk_score = sum(
        _LEVEL_ORDER.get(cls, 0) * p * 33
        for cls, p in zip(classes, proba)
    )
    risk_score = min(round(risk_score), 100)

    # Top reasons based on feature values
    reasons = _build_reasons(speed_kmph, total_passengers, w, hour)

    # Feature importances
    top_features = _feature_importances(model, meta)

    return {
        "bus_id": bus_id,
        "route_id": route_id,
        "hour": hour,
        "prediction": prediction,
        "risk_level": prediction,
        "risk_score": risk_score,
        "probabilities": proba_dict,
        "top_reasons": reasons,
        "top_feature_importances": top_features,
        "model_type": "RandomForestClassifier",
        "prediction_type": "Operational Service Risk (NOT mechanical failure prediction)",
        "weather_context": w,
        "speed_kmph": speed_kmph,
        "total_passengers": total_passengers,
    }


def _build_reasons(speed: float, pax: int, weather: dict, hour: int) -> list[str]:
    reasons = []
    if speed <= 5:
        reasons.append(f"Bus nearly stationary (speed {speed} km/h)")
    elif speed < 15:
        reasons.append(f"Very low speed ({speed} km/h)")
    elif speed < 25:
        reasons.append(f"Below-average speed ({speed} km/h)")

    if pax > 50:
        reasons.append(f"Very high passenger load ({pax} passengers)")
    elif pax > 20:
        reasons.append(f"High passenger load ({pax} passengers)")
    elif pax > 5:
        reasons.append(f"Moderate passenger load ({pax} passengers)")

    wrf = weather["weather_risk_factor"]
    if wrf >= 0.5:
        reasons.append(f"Severe weather conditions (risk factor {wrf})")
    elif wrf >= 0.3:
        reasons.append(f"Adverse weather (risk factor {wrf})")
    elif wrf > 0:
        reasons.append(f"Mild weather impact (risk factor {wrf})")

    if hour in (7, 8, 9, 17, 18, 19):
        reasons.append(f"Peak hour ({hour}:00) — high demand period")

    return reasons if reasons else ["Normal operating conditions"]
