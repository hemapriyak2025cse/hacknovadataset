from fastapi import APIRouter, HTTPException
from app.services.gps_service import get_all_buses, get_bus, get_bus_ids
from app.services.gtfs_service import find_nearest_stop, find_next_stop
from app.services.risk_service import compute_risk
from app.services.passenger_service import get_affected_passengers

router = APIRouter()


@router.get("/buses")
def list_buses():
    return {"buses": get_bus_ids(), "count": len(get_bus_ids())}


@router.get("/live-buses")
def live_buses():
    result = []
    for bus in get_all_buses():
        route_id = bus["route_id"]
        lat, lon = bus["latitude"], bus["longitude"]

        nearest = find_nearest_stop(lat, lon, route_id)
        next_stop = None
        if nearest:
            next_stop = find_next_stop(route_id, nearest["stop_sequence"])

        breakdown_seq = nearest["stop_sequence"] if nearest else 1
        pax = get_affected_passengers(bus["bus_id"], route_id, breakdown_seq)
        risk = compute_risk(
            speed_kmph=bus["speed_kmph"],
            traffic_delay_min=0,
            affected_passengers=pax["affected_passenger_count"],
        )

        status = "ON_TIME"
        if bus["speed_kmph"] < 5:
            status = "STOPPED"
        elif bus["speed_kmph"] < 15:
            status = "SLOW"

        result.append({
            "bus_id": bus["bus_id"],
            "route_id": route_id,
            "trip_id": bus["trip_id"],
            "latitude": bus["latitude"],
            "longitude": bus["longitude"],
            "speed_kmph": bus["speed_kmph"],
            "current_stop": nearest["stop_name"] if nearest else bus.get("current_stop_name"),
            "next_stop": next_stop["stop_name"] if next_stop else None,
            "status": status,
            "risk_level": risk["risk_level"],
            "data_source": bus["source"],
        })
    return result


@router.get("/buses/{bus_id}")
def bus_detail(bus_id: str):
    bus = get_bus(bus_id)
    if not bus:
        raise HTTPException(404, f"Bus {bus_id} not found")

    route_id = bus["route_id"]
    nearest = find_nearest_stop(bus["latitude"], bus["longitude"], route_id)
    next_stop = find_next_stop(route_id, nearest["stop_sequence"]) if nearest else None

    return {
        **bus,
        "nearest_stop": nearest,
        "next_stop": next_stop,
    }
