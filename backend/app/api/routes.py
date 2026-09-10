from fastapi import APIRouter
from app.services.gtfs_service import get_routes, get_route_stops, get_all_stops

router = APIRouter()


@router.get("/routes")
def list_routes():
    routes = get_routes()
    return {"routes": routes, "count": len(routes)}


@router.get("/routes/{route_id}/stops")
def route_stops(route_id: str):
    stops = get_route_stops(route_id)
    if not stops:
        from fastapi import HTTPException
        raise HTTPException(404, f"Route {route_id} not found")
    return {"route_id": route_id, "stops": stops}


@router.get("/stops")
def list_stops():
    stops = get_all_stops()
    return {"stops": stops, "count": len(stops)}
