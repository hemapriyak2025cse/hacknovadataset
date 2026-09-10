from fastapi import APIRouter, HTTPException
from app.services.gps_service import get_bus
from app.services.gtfs_service import find_nearest_stop, find_next_stop
from app.services.google_routes_service import get_traffic

router = APIRouter()


@router.get("/traffic/{bus_id}")
def bus_traffic(bus_id: str):
    bus = get_bus(bus_id)
    if not bus:
        raise HTTPException(404, f"Bus {bus_id} not found")

    route_id = bus["route_id"]
    nearest = find_nearest_stop(bus["latitude"], bus["longitude"], route_id)
    if not nearest:
        raise HTTPException(404, "No stop found for this bus")

    next_stop = find_next_stop(route_id, nearest["stop_sequence"])
    if not next_stop or not next_stop.get("latitude"):
        return {
            "bus_id": bus_id,
            "source": "fallback",
            "traffic_available": False,
            "message": "No next stop coordinates available",
        }

    traffic = get_traffic(
        bus["latitude"], bus["longitude"],
        next_stop["latitude"], next_stop["longitude"],
    )

    return {
        "bus_id": bus_id,
        "from_stop": nearest["stop_name"],
        "to_stop": next_stop["stop_name"],
        **traffic,
    }


@router.get("/alternate-routes/{bus_id}")
def alternate_routes(bus_id: str):
    bus = get_bus(bus_id)
    if not bus:
        raise HTTPException(404, f"Bus {bus_id} not found")

    route_id = bus["route_id"]
    nearest = find_nearest_stop(bus["latitude"], bus["longitude"], route_id)
    next_stop = find_next_stop(route_id, nearest["stop_sequence"]) if nearest else None

    if not next_stop or not next_stop.get("latitude"):
        return {"bus_id": bus_id, "alternate_road_routes": [], "source": "fallback"}

    traffic = get_traffic(
        bus["latitude"], bus["longitude"],
        next_stop["latitude"], next_stop["longitude"],
    )

    return {
        "bus_id": bus_id,
        "from": nearest["stop_name"] if nearest else None,
        "to": next_stop["stop_name"],
        "primary_route": {
            "duration_min": traffic["duration_min"],
            "distance_m": traffic["distance_m"],
            "traffic_delay_min": traffic["traffic_delay_min"],
        },
        "alternate_road_routes": traffic.get("alternate_road_routes", []),
        "source": traffic["source"],
    }
