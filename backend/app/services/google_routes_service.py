"""Google Routes API integration with fallback."""
import math
import os
import httpx
from app.utils import cache

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"


def get_traffic(origin_lat: float, origin_lon: float, dest_lat: float, dest_lon: float) -> dict:
    cache_key = f"traffic:{origin_lat:.4f},{origin_lon:.4f}:{dest_lat:.4f},{dest_lon:.4f}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    if GOOGLE_API_KEY:
        result = _call_google(origin_lat, origin_lon, dest_lat, dest_lon)
        if result:
            cache.set(cache_key, result, ttl=180)
            return result

    result = _fallback(origin_lat, origin_lon, dest_lat, dest_lon)
    cache.set(cache_key, result, ttl=180)
    return result


def _call_google(olat, olon, dlat, dlon) -> dict | None:
    body = {
        "origin": {"location": {"latLng": {"latitude": olat, "longitude": olon}}},
        "destination": {"location": {"latLng": {"latitude": dlat, "longitude": dlon}}},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternativeRoutes": True,
    }
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.staticDuration,routes.distanceMeters,routes.description",
    }
    try:
        resp = httpx.post(ROUTES_URL, json=body, headers=headers, timeout=5.0)
        resp.raise_for_status()
        data = resp.json()
        routes = data.get("routes", [])
        if not routes:
            return None
        best = routes[0]
        duration_s = int(best.get("duration", "0s").rstrip("s"))
        static_s = int(best.get("staticDuration", "0s").rstrip("s"))
        distance_m = best.get("distanceMeters", 0)
        delay_s = max(0, duration_s - static_s)
        delay_pct = round(delay_s / static_s * 100, 1) if static_s > 0 else 0.0

        alt_routes = []
        for r in routes[1:]:
            d_s = int(r.get("duration", "0s").rstrip("s"))
            alt_routes.append({
                "duration_min": round(d_s / 60, 1),
                "distance_m": r.get("distanceMeters", 0),
                "description": r.get("description", ""),
            })

        return {
            "source": "google",
            "traffic_available": True,
            "duration_min": round(duration_s / 60, 1),
            "static_duration_min": round(static_s / 60, 1),
            "distance_m": distance_m,
            "traffic_delay_min": round(delay_s / 60, 1),
            "traffic_delay_pct": delay_pct,
            "eta_minutes": round(duration_s / 60, 1),
            "alternate_road_routes": alt_routes,
        }
    except Exception:
        return None


def _fallback(olat, olon, dlat, dlon) -> dict:
    dist_km = _haversine(olat, olon, dlat, dlon)
    avg_speed = 25.0  # urban Chennai estimate km/h
    eta_min = round(dist_km / avg_speed * 60, 1)
    return {
        "source": "fallback",
        "traffic_available": False,
        "duration_min": eta_min,
        "static_duration_min": eta_min,
        "distance_m": round(dist_km * 1000),
        "traffic_delay_min": 0.0,
        "traffic_delay_pct": 0.0,
        "eta_minutes": eta_min,
        "alternate_road_routes": [],
    }


def _haversine(lat1, lon1, lat2, lon2) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
