"""Mock data service for demo deployment."""
import random
from typing import List, Dict, Any

class MockDataService:
    """Provides mock racing data for demonstration."""
    
    TRACKS = [
        "barber_motorsports_park",
        "circuit_of_the_americas",
        "indianapolis",
        "road_america",
        "sebring",
        "sonoma",
        "virginia_international_raceway"
    ]
    
    SESSIONS = ["R1", "R2"]
    
    DRIVERS = [
        "GR86-015-000", "GR86-020-000", "GR86-025-000",
        "GR86-030-000", "GR86-035-000", "GR86-040-000"
    ]
    
    @staticmethod
    def get_tracks() -> List[str]:
        """Get list of available tracks."""
        return MockDataService.TRACKS
    
    @staticmethod
    def get_sessions(track: str) -> List[str]:
        """Get sessions for a track."""
        return MockDataService.SESSIONS
    
    @staticmethod
    def get_drivers(track: str, session: str) -> List[str]:
        """Get drivers for a session."""
        return MockDataService.DRIVERS
    
    @staticmethod
    def get_best_lap(track: str, session: str) -> Dict[str, Any]:
        """Get best lap for a session."""
        return {
            "best_lap_time": round(random.uniform(85.0, 95.0), 3),
            "driver_id": random.choice(MockDataService.DRIVERS),
            "lap_number": random.randint(5, 15),
            "track": track,
            "session": session
        }
    
    @staticmethod
    def get_driver_performance(track: str, session: str, driver_id: str) -> Dict[str, Any]:
        """Get driver performance data."""
        best_lap = random.uniform(85.0, 95.0)
        avg_lap = best_lap + random.uniform(0.5, 2.0)
        std_dev = random.uniform(0.3, 1.0)
        
        lap_times = [best_lap + random.uniform(0, 2.5) for _ in range(20)]
        
        return {
            "driver_id": driver_id,
            "best_lap": round(best_lap, 3),
            "average_lap": round(avg_lap, 3),
            "std_deviation": round(std_dev, 3),
            "consistency_score": round(95.0 - (std_dev / avg_lap * 100), 1),
            "total_laps": len(lap_times),
            "lap_times": [round(t, 3) for t in lap_times]
        }
    
    @staticmethod
    def get_consistency(track: str, session: str, driver_id: str) -> Dict[str, Any]:
        """Get driver consistency metrics."""
        best_lap = random.uniform(85.0, 95.0)
        avg_lap = best_lap + random.uniform(0.5, 2.0)
        std_dev = random.uniform(0.3, 1.0)
        cv = (std_dev / avg_lap) * 100
        
        return {
            "driver_id": driver_id,
            "consistency_score": round(95.0 - cv, 1),
            "coefficient_of_variation": round(cv, 2),
            "best_lap": round(best_lap, 3),
            "average_lap": round(avg_lap, 3),
            "std_deviation": round(std_dev, 3),
            "laps_within_05s": random.randint(15, 20),
            "total_laps": 20
        }
