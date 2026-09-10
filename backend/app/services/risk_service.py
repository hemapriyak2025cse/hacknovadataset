"""Operational Risk Score engine.
Transparent weighted scoring — NOT a mechanical failure predictor.
"""
from app.services.weather_service import get_weather_for_hour


def compute_risk(
    speed_kmph: float,
    traffic_delay_min: float,
    affected_passengers: int,
    weather_hour: int = 9,
    traffic_delay_pct: float = 0.0,
) -> dict:
    reasons = []
    score = 0.0

    # Speed factor (0-35 pts)
    if speed_kmph <= 5:
        score += 35
        reasons.append("Bus is nearly stationary (speed ≤ 5 km/h)")
    elif speed_kmph < 15:
        score += 22
        reasons.append("Very low speed (< 15 km/h)")
    elif speed_kmph < 25:
        score += 10
        reasons.append("Below-average speed (< 25 km/h)")

    # Traffic delay factor (0-25 pts)
    if traffic_delay_min > 15:
        score += 25
        reasons.append(f"Severe traffic delay ({traffic_delay_min:.0f} min)")
    elif traffic_delay_min > 8:
        score += 15
        reasons.append(f"Moderate traffic delay ({traffic_delay_min:.0f} min)")
    elif traffic_delay_min > 3:
        score += 8
        reasons.append(f"Minor traffic delay ({traffic_delay_min:.0f} min)")

    # Passenger load factor (0-25 pts)
    if affected_passengers > 50:
        score += 25
        reasons.append(f"High passenger impact ({affected_passengers} passengers)")
    elif affected_passengers > 20:
        score += 15
        reasons.append(f"Moderate passenger impact ({affected_passengers} passengers)")
    elif affected_passengers > 5:
        score += 8
        reasons.append(f"Low passenger impact ({affected_passengers} passengers)")

    # Weather factor (0-20 pts)
    weather = get_weather_for_hour(weather_hour)
    wrf = weather["weather_risk_factor"]
    weather_pts = round(wrf * 20)
    if weather_pts > 0:
        score += weather_pts
        reasons.append(f"Weather: {weather['condition']} (risk factor {wrf})")

    score = min(round(score), 100)

    if score >= 75:
        level = "CRITICAL"
    elif score >= 50:
        level = "HIGH"
    elif score >= 25:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_score": score,
        "risk_level": level,
        "risk_reasons": reasons,
        "weather_context": weather,
        "score_type": "Operational Risk Score (heuristic weighted)",
    }
