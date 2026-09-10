"""FastAPI application entry point."""
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from app.api import buses, routes, traffic, risk, recommendations, ml_risk

app = FastAPI(
    title="Predictive Public Transport Operations API",
    description="Ripple Impact Engine — Hackathon MVP",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(buses.router, prefix="/api")
app.include_router(routes.router, prefix="/api")
app.include_router(traffic.router, prefix="/api")
app.include_router(risk.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
app.include_router(ml_risk.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Transport Ripple Impact Engine", "version": "1.0.0"}
