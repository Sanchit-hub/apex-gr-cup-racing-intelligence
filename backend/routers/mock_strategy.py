"""Mock strategy router for demo deployment."""
from fastapi import APIRouter
from backend.services.mock_data import MockDataService

router = APIRouter()

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/consistency")
async def get_consistency(track_name: str, session: str, driver_id: str):
    """Get driver consistency."""
    return MockDataService.get_consistency(track_name, session, driver_id)

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/tire-degradation")
async def get_tire_degradation(track_name: str, session: str, driver_id: str):
    """Get tire degradation."""
    return {
        "driver_id": driver_id,
        "degradation_rate_per_lap": 0.15,
        "best_lap": 89.456,
        "current_delta": 1.23,
        "laps_analyzed": 20
    }
