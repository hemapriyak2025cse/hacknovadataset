"""Alternate bus finder and Ripple Impact Engine."""
import math
from app.services.gps_service import get_all_buses, get_bus
from app.services.gtfs_service import get_route_stops, find_nearest_stop, _haversine
from app.services.passenger_service import get_affected_passengers
from app.services.google_routes_service import get_traffic
from app.utils.data_loader import route_stops_df, STOP_COORDS


def find_alternate_buses(broken_bus_id: str, breakdown_stop_seq: int, service_date: str = "2026-09-10") -> list[dict]:
    broken = get_bus(broken_bus_id)
    if not broken:
        return []

    broken_route = broken["route_id"]
    broken_lat = broken["latitude"]
    broken_lon = broken["longitude"]

    # Downstream stops on broken route
    downstream_stops = route_stops_df[
        (route_stops_df["route_id"] == broken_route) &
        (route_stops_df["stop_sequence"] > breakdown_stop_seq)
    ]["stop_id"].tolist()

    candidates = []
    for bus in get_all_buses():
        if bus["bus_id"] == broken_bus_id:
            continue
        bus_route = bus["route_id"]
        # Check if candidate serves any downstream stop
        overlap = route_stops_df[
            (route_stops_df["route_id"] == bus_route) &
            (route_stops_df["stop_id"].isin(downstream_stops))
        ]
        if overlap.empty:
            continue

        # Distance from candidate to breakdown location
        dist_km = _haversine(bus["latitude"], bus["longitude"], broken_lat, broken_lon)
        # ETA estimate
        speed = max(bus["speed_kmph"], 10.0)
        eta_min = round(dist_km / speed * 60, 1)

        # Traffic info
        traffic = get_traffic(bus["latitude"], bus["longitude"], broken_lat, broken_lon)
        if traffic["traffic_available"]:
            eta_min = traffic["eta_minutes"]

        # Compatibility score: how many downstream stops covered
        coverage = len(overlap) / max(len(downstream_stops), 1)

        # Candidate score (lower ETA + higher coverage = better)
        score = round((coverage * 50) - (eta_min * 0.5) + (50 - min(dist_km * 2, 50)), 1)

        candidates.append({
            "bus_id": bus["bus_id"],
            "route_id": bus_route,
            "current_lat": bus["latitude"],
            "current_lon": bus["longitude"],
            "current_speed_kmph": bus["speed_kmph"],
            "distance_to_incident_km": round(dist_km, 2),
            "eta_minutes": eta_min,
            "downstream_stops_covered": int(len(overlap)),
            "coverage_ratio": round(coverage, 2),
            "traffic_source": traffic["source"],
            "score": score,
        })

    candidates.sort(key=lambda x: -x["score"])
    return candidates[:5]


def compute_ripple_impact(broken_bus_id: str, breakdown_stop_seq: int, service_date: str = "2026-09-10") -> dict:
    broken = get_bus(broken_bus_id)
    if not broken:
        return {}

    route_id = broken["route_id"]
    impact = get_affected_passengers(broken_bus_id, route_id, breakdown_stop_seq, service_date)
    affected_pax = impact["affected_passenger_count"]

    candidates = find_alternate_buses(broken_bus_id, breakdown_stop_seq, service_date)

    options = []
    for i, cand in enumerate(candidates[:3]):
        # Secondary ripple: passengers on candidate bus that may be delayed
        cand_impact = get_affected_passengers(cand["bus_id"], cand["route_id"], 1, service_date)
        secondary_pax = cand_impact["affected_passenger_count"]

        # Score formula
        passenger_benefit = min(affected_pax / max(affected_pax, 1), 1.0) * 40
        response_penalty = min(cand["eta_minutes"] / 30, 1.0) * 20
        coverage_bonus = cand["coverage_ratio"] * 20
        secondary_penalty = min(secondary_pax / max(affected_pax, 1), 1.0) * 10
        traffic_penalty = (1 - (1 / (1 + cand["distance_to_incident_km"]))) * 10

        overall = round(passenger_benefit + coverage_bonus - response_penalty - secondary_penalty - traffic_penalty, 1)

        options.append({
            "option": f"OPTION_{chr(65+i)}",
            "bus_id": cand["bus_id"],
            "route_id": cand["route_id"],
            "eta_minutes": cand["eta_minutes"],
            "distance_km": cand["distance_to_incident_km"],
            "downstream_stops_covered": cand["downstream_stops_covered"],
            "coverage_ratio": cand["coverage_ratio"],
            "secondary_pax_impact": secondary_pax,
            "overall_score": overall,
            "explanation": (
                f"Deploy {cand['bus_id']} (route {cand['route_id']}): "
                f"covers {cand['downstream_stops_covered']} downstream stops, "
                f"ETA {cand['eta_minutes']} min, "
                f"secondary impact {secondary_pax} passengers."
            ),
        })

    options.sort(key=lambda x: -x["overall_score"])
    best = options[0] if options else None

    return {
        "broken_bus": broken_bus_id,
        "route_id": route_id,
        "breakdown_stop_seq": breakdown_stop_seq,
        "direct_passenger_impact": affected_pax,
        "downstream_stops": impact["downstream_stops"],
        "intervention_options": options,
        "recommended_option": best,
        "ripple_note": (
            "Best action is not always the closest bus. "
            "Coverage ratio and secondary passenger impact are factored in."
        ),
    }
