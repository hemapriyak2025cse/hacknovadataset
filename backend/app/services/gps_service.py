"""GPS service — uses mtc_synthetic_gps_speed_CORRECTED.csv.
The dataset contains one synthetic bus (SYN_MTC_001).
For the 14 ticket buses (B101-B503) we generate synthetic positions
derived from their route stops so the demo works end-to-end.
"""
import math
import random
from app.utils.data_loader import gps_df, bus_route_map, route_stops_df, STOP_COORDS

# Seed for reproducibility
random.seed(42)

# Build synthetic GPS snapshot for ticket buses
_SYNTHETIC_BUS_GPS: dict[str, dict] = {}

_DEMO_SPEEDS = {
    "B101": 12.0, "B102": 28.0, "B103": 5.0,
    "B201": 22.0, "B202": 18.0, "B203": 31.0,
    "B301": 8.0,  "B302": 25.0, "B303": 19.0,
    "B401": 14.0, "B402": 27.0, "B403": 6.0,
    "B501": 20.0, "B502": 11.0, "B503": 33.0,
}

for _bus, _route in bus_route_map.items():
    _stops = route_stops_df[route_stops_df["route_id"] == _route].sort_values("stop_sequence")
    # Place bus at a mid-route stop
    _mid = len(_stops) // 2
    _row = _stops.iloc[_mid]
    _coords = STOP_COORDS.get(_row["stop_id"], (13.0827, 80.2707))
    _SYNTHETIC_BUS_GPS[_bus] = {
        "bus_id": _bus,
        "route_id": _route,
        "trip_id": f"TRIP_{_bus}",
        "latitude": _coords[0] + random.uniform(-0.002, 0.002),
        "longitude": _coords[1] + random.uniform(-0.002, 0.002),
        "speed_kmph": _DEMO_SPEEDS.get(_bus, 20.0),
        "timestamp_sec": 32400,  # 09:00 AM
        "time_str": "09:00:00",
        "source": "synthetic_ticket_bus",
        "current_stop_id": _row["stop_id"],
        "current_stop_name": _row["stop_name"],
        "current_stop_seq": int(_row["stop_sequence"]),
    }

# Also include the real GPS bus
_real = gps_df.sort_values("timestamp_sec").iloc[-1]
_SYNTHETIC_BUS_GPS["SYN_MTC_001"] = {
    "bus_id": "SYN_MTC_001",
    "route_id": str(_real["route_id"]),
    "trip_id": str(_real["trip_id"]),
    "latitude": float(_real["latitude"]),
    "longitude": float(_real["longitude"]),
    "speed_kmph": float(_real["speed_kmph"]),
    "timestamp_sec": int(_real["timestamp_sec"]),
    "time_str": _real["time_str"],
    "source": "synthetic_from_MTC_GTFS",
    "current_stop_id": None,
    "current_stop_name": None,
    "current_stop_seq": None,
}


def get_all_buses() -> list[dict]:
    return list(_SYNTHETIC_BUS_GPS.values())


def get_bus(bus_id: str) -> dict | None:
    return _SYNTHETIC_BUS_GPS.get(bus_id)


def get_bus_ids() -> list[str]:
    return list(_SYNTHETIC_BUS_GPS.keys())
