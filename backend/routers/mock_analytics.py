"""Mock analytics router for demo deployment."""
from fastapi import APIRouter
from backend.services.mock_data import MockDataService

router = APIRouter()

@router.get("/tracks")
async def get_tracks():
    """Get list of available tracks."""
    return MockDataService.get_tracks()

@router.get("/track/{track_name}/sessions")
async def get_sessions(track_name: str):
    """Get sessions for a track."""
    return MockDataService.get_sessions(track_name)

@router.get("/track/{track_name}/session/{session}/drivers")
async def get_drivers(track_name: str, session: str):
    """Get drivers for a session."""
    return MockDataService.get_drivers(track_name, session)

@router.get("/track/{track_name}/session/{session}/best-lap")
async def get_best_lap(track_name: str, session: str):
    """Get best lap for a session."""
    return MockDataService.get_best_lap(track_name, session)

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/performance")
async def get_driver_performance(track_name: str, session: str, driver_id: str):
    """Get driver performance."""
    return MockDataService.get_driver_performance(track_name, session, driver_id)

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/detailed-performance")
async def get_detailed_performance(track_name: str, session: str, driver_id: str):
    """Get detailed driver performance."""
    return MockDataService.get_driver_performance(track_name, session, driver_id)

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/speed-analysis")
async def get_speed_analysis(track_name: str, session: str, driver_id: str):
    """Get speed analysis."""
    return {
        "driver_id": driver_id,
        "vmax": 185.3,
        "vmin": 65.2,
        "vavg": 142.7,
        "speed_range": 120.1
    }

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/braking-analysis")
async def get_braking_analysis(track_name: str, session: str, driver_id: str):
    """Get braking analysis."""
    return {
        "driver_id": driver_id,
        "brake_applications": 156,
        "avg_brake_pressure": 65.3,
        "max_brake_pressure": 98.7,
        "braking_efficiency": 66.1
    }

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/amicos-analysis")
async def get_amicos_analysis(track_name: str, session: str, driver_id: str):
    """Get AMICOS analysis."""
    return {
        "driver_id": driver_id,
        "analysis": "Demo data - full analysis available locally"
    }
