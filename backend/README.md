# Predictive Public Transport Operations — Backend API

Ripple Impact Engine for Chennai MTC bus network. Detects operational risk, computes passenger impact, and recommends alternate buses in real-time.

---

## Tech Stack

- **FastAPI** + **Uvicorn** — REST API server
- **Pandas / NumPy** — data processing
- **httpx** — Google Routes API calls
- **scikit-learn** — (reserved for future ML models)
- **python-dotenv** — environment config

---

## Project Structure

```
backend/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── api/
│   │   ├── buses.py             # Bus listing & live status endpoints
│   │   ├── routes.py            # GTFS route & stop endpoints
│   │   ├── traffic.py           # Traffic & alternate road route endpoints
│   │   ├── risk.py              # Operational risk scoring endpoints
│   │   └── recommendations.py  # Ripple impact & recommendation endpoints
│   ├── services/
│   │   ├── gps_service.py       # GPS snapshot (synthetic + real MTC data)
│   │   ├── gtfs_service.py      # GTFS stop/route resolution, haversine
│   │   ├── passenger_service.py # Affected passenger computation
│   │   ├── risk_service.py      # Weighted operational risk engine
│   │   ├── recommendation_service.py  # Alternate bus finder + ripple engine
│   │   ├── weather_service.py   # Open-Meteo CSV weather integration
│   │   └── google_routes_service.py   # Google Routes API + fallback
│   ├── utils/
│   │   ├── data_loader.py       # Loads all datasets once at startup
│   │   └── cache.py             # In-memory TTL cache
│   └── ml/                      # (empty — reserved for ML models)
├── .env.example
├── requirements.txt
└── server.log
```

---

## Datasets Used

| File | Description |
|------|-------------|
| `chennai-unified-gtfs/` | Chennai MTC GTFS feed (routes, stops, trips, stop_times) |
| `Datasets/route_stops.csv` | Synthetic route-stop mapping for routes R01–R05 |
| `Datasets/passenger_tickets.csv` | Synthetic passenger ticket data (2026-09-01 to 2026-09-14) |
| `mtc_synthetic_gps_speed_CORRECTED.csv` | Synthetic GPS + speed data for MTC buses |
| `open-meteo-11.00N76.99E431m.csv` | Historical weather data (Coimbatore proxy, 2025) |

---

## Setup

### 1. Prerequisites

- Python 3.11+
- pip

### 2. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure environment

```bash
copy .env.example .env
```

Edit `.env` and add your Google Maps API key (optional — fallback works without it):

```
GOOGLE_MAPS_API_KEY=your_key_here
```

### 4. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server starts at: `http://localhost:8000`

---

## API Endpoints

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Server health check |

### Buses
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/buses` | List all bus IDs |
| GET | `/api/live-buses` | All buses with live status, risk level, current/next stop |
| GET | `/api/buses/{bus_id}` | Single bus detail with nearest and next stop |

### Routes & Stops
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/routes` | List all route IDs |
| GET | `/api/routes/{route_id}/stops` | All stops for a route |
| GET | `/api/stops` | All stops across all routes |

### Traffic
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/traffic/{bus_id}` | Traffic delay between current and next stop |
| GET | `/api/alternate-routes/{bus_id}` | Alternate road routes via Google Routes API |

### Risk
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/risk` | Risk scores for all buses |
| GET | `/api/risk/{bus_id}?date=YYYY-MM-DD` | Detailed risk score for a specific bus |

### Recommendations & Alerts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/alternate-buses/{bus_id}?date=YYYY-MM-DD` | Candidate alternate buses ranked by score |
| GET | `/api/recommendation/{bus_id}?date=YYYY-MM-DD` | Full ripple impact + recommended action |
| POST | `/api/predict` | Same as recommendation (POST body: `{"bus_id": "B101", "date": "2026-09-10"}`) |
| GET | `/api/alerts?date=YYYY-MM-DD` | All buses with HIGH or CRITICAL risk |

> Default date for all date params: `2026-09-10`

---

## Risk Scoring Logic

The risk engine (`risk_service.py`) uses a transparent weighted heuristic — **not ML**.

| Factor | Max Points | Trigger |
|--------|-----------|---------|
| Speed | 35 | ≤5 km/h → 35pts, <15 → 22pts, <25 → 10pts |
| Traffic delay | 25 | >15 min → 25pts, >8 min → 15pts, >3 min → 8pts |
| Passenger load | 25 | >50 pax → 25pts, >20 → 15pts, >5 → 8pts |
| Weather | 20 | Based on WMO weather code + precipitation + wind |

**Risk Levels:**
- `LOW` — score < 25
- `MEDIUM` — score 25–49
- `HIGH` — score 50–74
- `CRITICAL` — score ≥ 75

---

## Ripple Impact Engine

`recommendation_service.py` computes the best alternate bus by:

1. Finding all downstream stops of the broken bus
2. Scanning all other buses for route overlap with those stops
3. Scoring candidates by: coverage ratio, ETA, distance, secondary passenger impact
4. Returning top 3 options ranked by overall score

---

## Bus Data

16 buses are available in the demo:

| Bus ID | Speed (km/h) | Status |
|--------|-------------|--------|
| B101 | 12.0 | Slow |
| B102 | 28.0 | Normal |
| B103 | 5.0 | Nearly stopped |
| B201–B203 | 22–31 | Normal/Slow |
| B301 | 8.0 | Slow |
| B302–B303 | 19–25 | Normal |
| B401–B403 | 6–27 | Mixed |
| B501–B503 | 11–33 | Mixed |
| SYN_MTC_001 | From CSV | Real GPS data |

---

## Notes

- All data is **synthetic/demo** — not real-time Chennai MTC data
- Weather data is a **regional proxy** from Coimbatore station (2025)
- Google Routes API is **optional** — haversine-based fallback is used when no API key is set
- Traffic results are cached in-memory for **3 minutes** (TTL cache)
- The `ml/` folder is empty — reserved for future model integration
