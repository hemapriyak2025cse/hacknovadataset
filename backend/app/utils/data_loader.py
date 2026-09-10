"""
Data loader — loads all datasets once at startup and caches them.
All services import from here.
"""
import os
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # data-transport-weather/

# ── GTFS ──────────────────────────────────────────────────────────────────────
GTFS_DIR = ROOT / "chennai-unified-gtfs"

routes_df = pd.read_csv(GTFS_DIR / "routes.txt", on_bad_lines="skip")
trips_df = pd.read_csv(GTFS_DIR / "trips.txt", on_bad_lines="skip")
stop_times_df = pd.read_csv(GTFS_DIR / "stop_times.txt", on_bad_lines="skip", low_memory=False)
stops_df = pd.read_csv(GTFS_DIR / "stops.txt", on_bad_lines="skip")

# ── Synthetic route-stop mapping (R01-R05) ────────────────────────────────────
DATASETS_DIR = ROOT / "Datasets"
route_stops_df = pd.read_csv(DATASETS_DIR / "route_stops.csv")

# ── Passenger tickets ─────────────────────────────────────────────────────────
tickets_df = pd.read_csv(DATASETS_DIR / "passenger_tickets.csv")
# Normalise date format to YYYY-MM-DD
tickets_df["boarding_date"] = pd.to_datetime(
    tickets_df["boarding_date"], dayfirst=True
).dt.strftime("%Y-%m-%d")

# Attach stop_sequence for source and destination
_seq = route_stops_df[["route_id", "stop_id", "stop_sequence"]].copy()
tickets_df = tickets_df.merge(
    _seq.rename(columns={"stop_id": "source_stop", "stop_sequence": "source_seq"}),
    on=["route_id", "source_stop"], how="left"
).merge(
    _seq.rename(columns={"stop_id": "destination_stop", "stop_sequence": "dest_seq"}),
    on=["route_id", "destination_stop"], how="left"
)

# ── GPS ───────────────────────────────────────────────────────────────────────
gps_df = pd.read_csv(ROOT / "mtc_synthetic_gps_speed_CORRECTED.csv")
# Convert timestamp_sec (seconds since midnight) to HH:MM:SS string
gps_df["time_str"] = pd.to_datetime(
    gps_df["timestamp_sec"], unit="s", origin="1970-01-01"
).dt.strftime("%H:%M:%S")

# ── Weather ───────────────────────────────────────────────────────────────────
weather_df = pd.read_csv(ROOT / "open-meteo-11.00N76.99E431m.csv", skiprows=2)
weather_df.columns = ["time", "temperature_c", "precipitation_mm", "wind_speed_kmh", "weather_code"]
weather_df["time"] = pd.to_datetime(weather_df["time"])
weather_df["hour"] = weather_df["time"].dt.hour

# ── Bus → Route mapping (from tickets) ───────────────────────────────────────
bus_route_map: dict[str, str] = (
    tickets_df.groupby("bus_id")["route_id"].first().to_dict()
)

# Synthetic bus list with simulated positions (one GPS bus + 14 from tickets)
# We'll generate synthetic positions for the 14 ticket buses using route_stops coords
# Use approximate Chennai stop coordinates
STOP_COORDS: dict[str, tuple[float, float]] = {
    "S01": (13.0694, 80.1000),  # CMBT
    "S02": (13.0694, 80.1050),  # Koyambedu
    "S03": (13.0500, 80.1200),  # Vadapalani
    "S04": (13.0350, 80.1900),  # Ashok Nagar
    "S05": (13.0350, 80.2300),  # T Nagar
    "S06": (13.0100, 80.2200),  # Saidapet
    "S07": (12.9900, 80.2200),  # Guindy
    "S08": (13.0050, 80.2560),  # Adyar
    "S09": (12.9900, 80.2700),  # Thiruvanmiyur
    "S10": (12.9700, 80.2400),  # Taramani
    "S11": (13.1140, 80.1600),  # Ambattur
    "S12": (13.0900, 80.1700),  # Mogappair
    "S13": (13.0850, 80.2100),  # Anna Nagar
    "S14": (13.0800, 80.2400),  # Kilpauk
    "S15": (13.0700, 80.2600),  # Egmore
    "S16": (13.0827, 80.2707),  # Central
    "S17": (13.0900, 80.2850),  # Parrys
    "S18": (13.0500, 80.2820),  # Marina Beach
    "S19": (13.0200, 80.2400),  # Nandanam
    "S20": (12.9800, 80.2200),  # Velachery
    "S21": (12.9600, 80.2400),  # Perungudi
    "S22": (12.9000, 80.2300),  # Sholinganallur
    "S23": (12.8500, 80.2300),  # OMR
    "S24": (12.9250, 80.1200),  # Tambaram
    "S25": (12.9500, 80.1400),  # Chromepet
    "S26": (12.9700, 80.1500),  # Pallavaram
    "S28": (13.0350, 80.1600),  # Porur
    "S29": (13.1150, 80.0900),  # Avadi
    "S30": (13.1000, 80.1100),  # Thirumullaivoyal
    "S31": (13.1000, 80.1800),  # Padi
}
