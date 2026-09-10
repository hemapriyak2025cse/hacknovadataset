"""Weather service — uses open-meteo CSV (2025 data, regional proxy for demo)."""
from app.utils.data_loader import weather_df


def get_weather_for_hour(hour: int) -> dict:
    """Return average weather metrics for a given hour across the dataset."""
    rows = weather_df[weather_df["hour"] == hour]
    if rows.empty:
        rows = weather_df

    row = rows.iloc[len(rows) // 2]  # pick a representative row

    code = int(row["weather_code"])
    condition = _wmo_label(code)
    risk_factor = _weather_risk(code, float(row["precipitation_mm"]), float(row["wind_speed_kmh"]))

    return {
        "temperature_c": round(float(row["temperature_c"]), 1),
        "precipitation_mm": round(float(row["precipitation_mm"]), 2),
        "wind_speed_kmh": round(float(row["wind_speed_kmh"]), 1),
        "weather_code": code,
        "condition": condition,
        "weather_risk_factor": risk_factor,
        "data_note": "Regional weather proxy (Coimbatore station, 2025). Not real-time Chennai data.",
    }


def _wmo_label(code: int) -> str:
    if code == 0:
        return "Clear sky"
    if code in (1, 2, 3):
        return "Partly cloudy"
    if code in (45, 48):
        return "Foggy"
    if code in (51, 53, 55):
        return "Drizzle"
    if code in (61, 63, 65):
        return "Rain"
    if code in (80, 81, 82):
        return "Rain showers"
    if code in (95, 96, 99):
        return "Thunderstorm"
    return "Unknown"


def _weather_risk(code: int, precip: float, wind: float) -> float:
    """0.0 = no risk, 1.0 = max risk."""
    risk = 0.0
    if code in (95, 96, 99):
        risk += 0.5
    elif code in (61, 63, 65, 80, 81, 82):
        risk += 0.3
    elif code in (45, 48):
        risk += 0.2
    if precip > 5:
        risk += 0.2
    elif precip > 1:
        risk += 0.1
    if wind > 40:
        risk += 0.2
    elif wind > 20:
        risk += 0.1
    return round(min(risk, 1.0), 2)
