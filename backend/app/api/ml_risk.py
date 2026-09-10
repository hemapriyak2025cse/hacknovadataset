"""
ML Risk Prediction API router.
Exposes the trained RandomForest model via /api/ml/risk/{bus_id}
Does NOT replace or modify the existing heuristic risk endpoints.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from app.services.gps_service import get_bus
from app.services.gtfs_service import find_nearest_stop
from app.services.passenger_service import get_affected_passengers

router = APIRouter(prefix="/ml", tags=["ML Risk Prediction"])


def _get_predictor():
    """Lazy-load the ML predictor to avoid import errors if model not trained yet."""
    try:
        from app.ml.predict import predict_risk
        return predict_risk
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=503,
            detail=f"ML model not available: {e}. Run: python -m app.ml.train",
        )


@router.get("/risk/{bus_id}")
def ml_risk(bus_id: str, date: str = "2026-09-10", hour: int = None):
    """
    ML-based operational service risk prediction for a bus.

    Uses a pre-trained RandomForestClassifier (NOT a mechanical failure predictor).
    Falls back to current hour if hour not specified.
    """
    bus = get_bus(bus_id)
    if not bus:
        raise HTTPException(404, f"Bus {bus_id} not found")

    predict_risk = _get_predictor()

    route_id = bus["route_id"]

    # Resolve hour
    if hour is None:
        hour = datetime.now().hour

    # Day of week from date param
    try:
        dow = datetime.strptime(date, "%Y-%m-%d").weekday()
    except ValueError:
        dow = datetime.now().weekday()

    # Get passenger load for this bus/route/date at this hour
    nearest = find_nearest_stop(bus["latitude"], bus["longitude"], route_id)
    seq = nearest["stop_sequence"] if nearest else 1
    pax_data = get_affected_passengers(bus_id, route_id, seq, date)
    total_passengers = pax_data["affected_passenger_count"]

    # Ticket count proxy: use affected_ticket_count
    ticket_count = pax_data.get("affected_ticket_count", max(1, total_passengers // 2))

    result = predict_risk(
        bus_id=bus_id,
        route_id=route_id,
        hour=hour,
        day_of_week=dow,
        total_passengers=total_passengers,
        avg_trip_length=3.0,
        ticket_count=ticket_count,
        speed_kmph=bus["speed_kmph"],
    )

    return {
        **result,
        "current_stop": nearest["stop_name"] if nearest else None,
        "date": date,
        "note": "ML prediction — Operational Service Risk. NOT mechanical failure prediction.",
    }


@router.get("/risk")
def ml_risk_all(date: str = "2026-09-10", hour: int = None):
    """ML risk prediction for all buses."""
    from app.services.gps_service import get_all_buses

    predict_risk = _get_predictor()

    if hour is None:
        hour = datetime.now().hour

    try:
        dow = datetime.strptime(date, "%Y-%m-%d").weekday()
    except ValueError:
        dow = datetime.now().weekday()

    results = []
    for bus in get_all_buses():
        bus_id = bus["bus_id"]
        route_id = bus["route_id"]
        nearest = find_nearest_stop(bus["latitude"], bus["longitude"], route_id)
        seq = nearest["stop_sequence"] if nearest else 1
        pax_data = get_affected_passengers(bus_id, route_id, seq, date)
        total_passengers = pax_data["affected_passenger_count"]
        ticket_count = pax_data.get("affected_ticket_count", max(1, total_passengers // 2))

        result = predict_risk(
            bus_id=bus_id,
            route_id=route_id,
            hour=hour,
            day_of_week=dow,
            total_passengers=total_passengers,
            avg_trip_length=3.0,
            ticket_count=ticket_count,
            speed_kmph=bus["speed_kmph"],
        )
        results.append({
            "bus_id": bus_id,
            "route_id": route_id,
            "risk_level": result["risk_level"],
            "risk_score": result["risk_score"],
            "probabilities": result["probabilities"],
            "top_reasons": result["top_reasons"],
            "speed_kmph": bus["speed_kmph"],
            "current_stop": nearest["stop_name"] if nearest else None,
        })

    results.sort(key=lambda x: -x["risk_score"])
    return {"predictions": results, "count": len(results), "hour": hour, "date": date}


class MLPredictRequest(BaseModel):
    bus_id: str
    route_id: str
    hour: int
    day_of_week: int
    total_passengers: int
    avg_trip_length: float = 3.0
    ticket_count: int = 5
    speed_kmph: float = None


@router.post("/predict")
def ml_predict(req: MLPredictRequest):
    """
    Direct ML prediction with explicit feature input.
    Useful for testing or frontend integration.
    """
    predict_risk = _get_predictor()
    return predict_risk(
        bus_id=req.bus_id,
        route_id=req.route_id,
        hour=req.hour,
        day_of_week=req.day_of_week,
        total_passengers=req.total_passengers,
        avg_trip_length=req.avg_trip_length,
        ticket_count=req.ticket_count,
        speed_kmph=req.speed_kmph,
    )
