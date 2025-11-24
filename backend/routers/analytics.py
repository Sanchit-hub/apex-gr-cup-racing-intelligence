"""Analytics endpoints for lap time and sector analysis."""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from backend.services.lap_analyzer import LapAnalyzer
from backend.services.advanced_analytics import AdvancedAnalytics
from backend.services.amicos_engine import AMICOSEngine

router = APIRouter()
analyzer = LapAnalyzer()
advanced = AdvancedAnalytics()
amicos = AMICOSEngine()

@router.get("/tracks")
async def get_tracks() -> List[str]:
    """Get list of available tracks."""
    return analyzer.get_available_tracks()

@router.get("/track/{track_name}/sessions")
async def get_sessions(track_name: str) -> List[str]:
    """Get available sessions for a track."""
    try:
        return analyzer.get_sessions(track_name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/track/{track_name}/session/{session}/best-lap")
async def get_best_lap(track_name: str, session: str) -> Dict[str, Any]:
    """Get theoretical best lap from combined best sectors."""
    try:
        return analyzer.calculate_best_lap(track_name, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/performance")
async def get_driver_performance(track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
    """Get comprehensive driver performance analysis."""
    try:
        return analyzer.analyze_driver_performance(track_name, session, driver_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track/{track_name}/session/{session}/drivers")
async def get_drivers(track_name: str, session: str) -> List[str]:
    """Get list of drivers for a session."""
    try:
        return analyzer.get_drivers(track_name, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/detailed-performance")
async def get_detailed_performance(track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
    """Get detailed performance analysis with vehicle specs."""
    try:
        return advanced.get_detailed_performance(track_name, session, driver_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/speed-analysis")
async def get_advanced_speed_analysis(track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
    """Get advanced speed analysis with GR86 specs."""
    try:
        return advanced.get_speed_analysis(track_name, session, driver_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/braking-analysis")
async def get_advanced_braking_analysis(track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
    """Get advanced braking analysis with Brembo specs."""
    try:
        return advanced.get_braking_analysis(track_name, session, driver_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track/{track_name}/session/{session}/driver/{driver_id}/amicos-analysis")
async def get_amicos_analysis(track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
    """Get AMICOS cornering optimization analysis."""
    try:
        return amicos.analyze_cornering_performance(track_name, session, driver_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/track/{track_name}/session/{session}/sector-analysis")
async def get_sector_analysis(track_name: str, session: str) -> Dict[str, Any]:
    """Get sector-by-sector analysis for all drivers."""
    try:
        return analyzer.analyze_sectors(track_name, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
