"""Telemetry endpoints for real-time data analysis."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from backend.services.telemetry_analyzer import TelemetryAnalyzer

router = APIRouter()
telemetry = TelemetryAnalyzer()

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/lap/{lap_number}")
async def get_lap_telemetry(
    track_name: str, 
    session: str, 
    driver_id: str, 
    lap_number: int
) -> Dict[str, Any]:
    """Get detailed telemetry for a specific lap."""
    try:
        return telemetry.get_lap_data(track_name, session, driver_id, lap_number)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/braking-analysis")
async def get_braking_analysis(track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
    """Analyze braking points and efficiency."""
    try:
        return telemetry.analyze_braking(track_name, session, driver_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/speed-analysis")
async def get_speed_analysis(track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
    """Analyze speed profile (vMin, vMax, acceleration)."""
    try:
        return telemetry.analyze_speed(track_name, session, driver_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
