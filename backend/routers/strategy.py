"""Strategy endpoints for race simulation and predictions."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
from backend.services.strategy_engine import StrategyEngine

router = APIRouter()
strategy = StrategyEngine()

class PitStopRequest(BaseModel):
    current_lap: int
    total_laps: int
    tire_age: int
    fuel_level: float

@router.post("/track/{track_name}/session/{session}/driver/{driver_id}/pit-strategy")
async def calculate_pit_strategy(
    track_name: str,
    session: str,
    driver_id: str,
    request: PitStopRequest
) -> Dict[str, Any]:
    """Calculate optimal pit stop strategy."""
    try:
        return strategy.calculate_pit_window(
            track_name, session, driver_id,
            request.current_lap, request.total_laps,
            request.tire_age, request.fuel_level
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/tire-degradation")
async def get_tire_degradation(track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
    """Predict tire degradation over race distance."""
    try:
        return strategy.predict_tire_degradation(track_name, session, driver_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/consistency")
async def get_consistency_metrics(track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
    """Calculate driver consistency metrics."""
    try:
        return strategy.analyze_consistency(track_name, session, driver_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
