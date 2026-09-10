from fastapi import APIRouter, HTTPException
from app.services.gps_service import get_bus
from app.services.gtfs_service import find_nearest_stop
from app.services.recommendation_service import find_alternate_buses, compute_ripple_impact
from app.services.passenger_service import get_affected_passengers
from app.services.risk_service import compute_risk
from app.services.google_routes_service import get_traffic
from app.services.weather_service import get_weather_for_hour
from pydantic import BaseModel

router = APIRouter()


@router.get("/alternate-buses/{bus_id}")
def alternate_buses(bus_id: str, date: str = "2026-09-10"):
    bus = get_bus(bus_id)
    if not bus:
        raise HTTPException(404, f"Bus {bus_id} not found")

    route_id = bus["route_id"]
    nearest = find_nearest_stop(bus["latitude"], bus["longitude"], route_id)
    seq = nearest["stop_sequence"] if nearest else 1

    candidates = find_alternate_buses(bus_id, seq, date)
    return {
        "bus_id": bus_id,
        "breakdown_stop_seq": seq,
        "breakdown_stop": nearest["stop_name"] if nearest else None,
        "candidate_buses": candidates,
    }


@router.get("/recommendation/{bus_id}")
def recommendation(bus_id: str, date: str = "2026-09-10"):
    bus = get_bus(bus_id)
    if not bus:
        raise HTTPException(404, f"Bus {bus_id} not found")

    route_id = bus["route_id"]
    nearest = find_nearest_stop(bus["latitude"], bus["longitude"], route_id)
    seq = nearest["stop_sequence"] if nearest else 1

    pax = get_affected_passengers(bus_id, route_id, seq, date)
    affected_pax = pax["affected_passenger_count"]

    # Traffic
    from app.services.gtfs_service import find_next_stop
    next_stop = find_next_stop(route_id, seq)
    traffic_delay = 0.0
    traffic_info = {"source": "fallback", "traffic_available": False}
    if next_stop and next_stop.get("latitude"):
        traffic_info = get_traffic(bus["latitude"], bus["longitude"], next_stop["latitude"], next_stop["longitude"])
        traffic_delay = traffic_info["traffic_delay_min"]

    risk = compute_risk(
        speed_kmph=bus["speed_kmph"],
        traffic_delay_min=traffic_delay,
        affected_passengers=affected_pax,
    )

    weather = get_weather_for_hour(9)
    ripple = compute_ripple_impact(bus_id, seq, date)

    best_option = ripple.get("recommended_option")
    recommended_bus = best_option["bus_id"] if best_option else None
    recommended_action = (
        f"Deploy {recommended_bus} to cover downstream stops"
        if recommended_bus else "Monitor situation"
    )

    # Confidence label (heuristic, not ML)
    if risk["risk_level"] in ("HIGH", "CRITICAL") and best_option:
        confidence = "HIGH (heuristic: clear risk + viable alternate)"
    elif risk["risk_level"] == "MEDIUM":
        confidence = "MEDIUM (heuristic: moderate risk)"
    else:
        confidence = "LOW (heuristic: low operational risk)"

    return {
        "bus_id": bus_id,
        "route_id": route_id,
        "current_stop": nearest["stop_name"] if nearest else None,
        "risk_level": risk["risk_level"],
        "risk_score": risk["risk_score"],
        "risk_reasons": risk["risk_reasons"],
        "problem": _describe_problem(bus["speed_kmph"], traffic_delay, affected_pax),
        "affected_passengers": affected_pax,
        "downstream_stops": pax["downstream_stops"],
        "weather": weather,
        "traffic": traffic_info,
        "candidate_buses": ripple.get("intervention_options", []),
        "intervention_options": ripple.get("intervention_options", []),
        "recommended_action": recommended_action,
        "recommended_bus": recommended_bus,
        "expected_benefit": (
            f"Rescue ~{affected_pax} stranded passengers, "
            f"covering {best_option['downstream_stops_covered'] if best_option else 0} downstream stops"
        ),
        "reason": best_option["explanation"] if best_option else "No viable alternate found",
        "confidence": confidence,
        "ripple_note": ripple.get("ripple_note", ""),
        "data_note": "Synthetic demo data. Dates: 2026-09-01 to 2026-09-14.",
    }


def _describe_problem(speed: float, delay: float, pax: int) -> str:
    parts = []
    if speed < 5:
        parts.append("bus is stationary")
    elif speed < 15:
        parts.append("bus moving very slowly")
    if delay > 8:
        parts.append(f"traffic delay {delay:.0f} min")
    if pax > 0:
        parts.append(f"{pax} passengers at risk")
    return "; ".join(parts) if parts else "operational monitoring"


class PredictRequest(BaseModel):
    bus_id: str
    date: str = "2026-09-10"


@router.post("/predict")
def predict(req: PredictRequest):
    return recommendation(req.bus_id, req.date)


@router.get("/alerts")
def alerts(date: str = "2026-09-10"):
    from app.services.gps_service import get_all_buses
    from app.services.gtfs_service import find_nearest_stop
    alerts_list = []
    for bus in get_all_buses():
        route_id = bus["route_id"]
        nearest = find_nearest_stop(bus["latitude"], bus["longitude"], route_id)
        seq = nearest["stop_sequence"] if nearest else 1
        pax = get_affected_passengers(bus["bus_id"], route_id, seq, date)
        risk = compute_risk(
            speed_kmph=bus["speed_kmph"],
            traffic_delay_min=0,
            affected_passengers=pax["affected_passenger_count"],
        )
        if risk["risk_level"] in ("HIGH", "CRITICAL"):
            alerts_list.append({
                "bus_id": bus["bus_id"],
                "route_id": route_id,
                "risk_level": risk["risk_level"],
                "risk_score": risk["risk_score"],
                "affected_passengers": pax["affected_passenger_count"],
                "current_stop": nearest["stop_name"] if nearest else None,
            })
    return {"alerts": alerts_list, "count": len(alerts_list)}
