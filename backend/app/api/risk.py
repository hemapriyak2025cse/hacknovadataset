from fastapi import APIRouter, HTTPException
from app.services.gps_service import get_bus, get_all_buses
from app.services.gtfs_service import find_nearest_stop
from app.services.passenger_service import get_affected_passengers
from app.services.risk_service import compute_risk
from app.services.google_routes_service import get_traffic

router = APIRouter()


@router.get("/risk")
def all_risk():
    results = []
    for bus in get_all_buses():
        route_id = bus["route_id"]
        nearest = find_nearest_stop(bus["latitude"], bus["longitude"], route_id)
        seq = nearest["stop_sequence"] if nearest else 1
        pax = get_affected_passengers(bus["bus_id"], route_id, seq)
        risk = compute_risk(
            speed_kmph=bus["speed_kmph"],
            traffic_delay_min=0,
            affected_passengers=pax["affected_passenger_count"],
        )
        results.append({"bus_id": bus["bus_id"], "route_id": route_id, **risk})
    return results


@router.get("/risk/{bus_id}")
def bus_risk(bus_id: str, date: str = "2026-09-10"):
    bus = get_bus(bus_id)
    if not bus:
        raise HTTPException(404, f"Bus {bus_id} not found")

    route_id = bus["route_id"]
    nearest = find_nearest_stop(bus["latitude"], bus["longitude"], route_id)
    seq = nearest["stop_sequence"] if nearest else 1

    pax = get_affected_passengers(bus_id, route_id, seq, date)

    # Get traffic for context
    next_stop_coords = None
    if nearest:
        from app.services.gtfs_service import find_next_stop
        from app.utils.data_loader import STOP_COORDS
        ns = find_next_stop(route_id, nearest["stop_sequence"])
        if ns:
            next_stop_coords = (ns["latitude"], ns["longitude"])

    traffic_delay = 0.0
    traffic_delay_pct = 0.0
    if next_stop_coords:
        traffic = get_traffic(bus["latitude"], bus["longitude"], next_stop_coords[0], next_stop_coords[1])
        traffic_delay = traffic["traffic_delay_min"]
        traffic_delay_pct = traffic["traffic_delay_pct"]

    risk = compute_risk(
        speed_kmph=bus["speed_kmph"],
        traffic_delay_min=traffic_delay,
        affected_passengers=pax["affected_passenger_count"],
        traffic_delay_pct=traffic_delay_pct,
    )

    return {
        "bus_id": bus_id,
        "route_id": route_id,
        "current_stop": nearest["stop_name"] if nearest else None,
        "breakdown_stop_seq": seq,
        "affected_passengers": pax["affected_passenger_count"],
        **risk,
    }
