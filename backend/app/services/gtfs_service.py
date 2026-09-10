"""GTFS + synthetic route-stop service."""
import math
from app.utils.data_loader import routes_df, stops_df, route_stops_df, STOP_COORDS


def get_routes() -> list[dict]:
    return route_stops_df["route_id"].unique().tolist()


def get_route_stops(route_id: str) -> list[dict]:
    rows = route_stops_df[route_stops_df["route_id"] == route_id].sort_values("stop_sequence")
    result = []
    for _, r in rows.iterrows():
        coords = STOP_COORDS.get(r["stop_id"], (None, None))
        result.append({
            "stop_id": r["stop_id"],
            "stop_name": r["stop_name"],
            "stop_sequence": int(r["stop_sequence"]),
            "latitude": coords[0],
            "longitude": coords[1],
        })
    return result


def get_all_stops() -> list[dict]:
    rows = route_stops_df.drop_duplicates("stop_id")
    result = []
    for _, r in rows.iterrows():
        coords = STOP_COORDS.get(r["stop_id"], (None, None))
        result.append({
            "stop_id": r["stop_id"],
            "stop_name": r["stop_name"],
            "latitude": coords[0],
            "longitude": coords[1],
        })
    return result


def _haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def find_nearest_stop(lat: float, lon: float, route_id: str | None = None) -> dict | None:
    rows = route_stops_df if route_id is None else route_stops_df[route_stops_df["route_id"] == route_id]
    best, best_d = None, float("inf")
    for _, r in rows.iterrows():
        coords = STOP_COORDS.get(r["stop_id"])
        if not coords:
            continue
        d = _haversine(lat, lon, coords[0], coords[1])
        if d < best_d:
            best_d = d
            best = r
    if best is None:
        return None
    coords = STOP_COORDS.get(best["stop_id"], (None, None))
    return {
        "stop_id": best["stop_id"],
        "stop_name": best["stop_name"],
        "stop_sequence": int(best["stop_sequence"]),
        "route_id": best["route_id"],
        "latitude": coords[0],
        "longitude": coords[1],
        "distance_km": round(best_d, 3),
    }


def find_next_stop(route_id: str, current_seq: int) -> dict | None:
    rows = route_stops_df[
        (route_stops_df["route_id"] == route_id) &
        (route_stops_df["stop_sequence"] == current_seq + 1)
    ]
    if rows.empty:
        return None
    r = rows.iloc[0]
    coords = STOP_COORDS.get(r["stop_id"], (None, None))
    return {
        "stop_id": r["stop_id"],
        "stop_name": r["stop_name"],
        "stop_sequence": int(r["stop_sequence"]),
        "latitude": coords[0],
        "longitude": coords[1],
    }


def get_stop_sequence(route_id: str, stop_id: str) -> int | None:
    rows = route_stops_df[
        (route_stops_df["route_id"] == route_id) &
        (route_stops_df["stop_id"] == stop_id)
    ]
    return int(rows.iloc[0]["stop_sequence"]) if not rows.empty else None
