"""Telemetry data analysis service."""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any

class TelemetryAnalyzer:
    """Analyzes telemetry data for performance insights."""
    
    def __init__(self):
        self.data_dir = Path("data")
    
    def get_lap_data(self, track_name: str, session: str, driver_id: str, lap_number: int) -> Dict[str, Any]:
        """Get detailed telemetry for a specific lap."""
        telemetry = self._load_telemetry(track_name, session)
        
        if telemetry.empty:
            return {"error": "No telemetry data available"}
        
        lap_data = telemetry[
            (telemetry['vehicle_id'] == driver_id) & 
            (telemetry['lap'] == lap_number)
        ]
        
        if lap_data.empty:
            return {"error": f"No data for lap {lap_number}"}
        
        # Extract key metrics
        speed_data = lap_data[lap_data['telemetry_name'] == 'vehspd_can']
        throttle_data = lap_data[lap_data['telemetry_name'] == 'aps']
        brake_data = lap_data[lap_data['telemetry_name'].str.contains('brake', case=False, na=False)]
        
        return {
            "lap_number": lap_number,
            "driver_id": driver_id,
            "speed": {
                "max": float(speed_data['telemetry_value'].max()) if not speed_data.empty else 0,
                "avg": float(speed_data['telemetry_value'].mean()) if not speed_data.empty else 0,
                "min": float(speed_data['telemetry_value'].min()) if not speed_data.empty else 0
            },
            "throttle_avg": float(throttle_data['telemetry_value'].mean()) if not throttle_data.empty else 0,
            "data_points": len(lap_data)
        }
    
    def analyze_braking(self, track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
        """Analyze braking points and efficiency."""
        telemetry = self._load_telemetry(track_name, session)
        
        if telemetry.empty:
            return {"error": "No telemetry data available"}
        
        driver_data = telemetry[telemetry['vehicle_id'] == driver_id]
        brake_data = driver_data[driver_data['telemetry_name'].str.contains('brake', case=False, na=False)]
        
        if brake_data.empty:
            return {"message": "No braking data available"}
        
        # Calculate braking metrics
        brake_applications = len(brake_data[brake_data['telemetry_value'] > 0])
        avg_brake_pressure = float(brake_data['telemetry_value'].mean())
        max_brake_pressure = float(brake_data['telemetry_value'].max())
        
        return {
            "driver_id": driver_id,
            "brake_applications": brake_applications,
            "avg_brake_pressure": avg_brake_pressure,
            "max_brake_pressure": max_brake_pressure,
            "braking_efficiency": float(avg_brake_pressure / max_brake_pressure * 100) if max_brake_pressure > 0 else 0
        }
    
    def analyze_speed(self, track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
        """Analyze speed profile (vMin, vMax, acceleration)."""
        telemetry = self._load_telemetry(track_name, session)
        
        if telemetry.empty:
            return {"error": "No telemetry data available"}
        
        driver_data = telemetry[telemetry['vehicle_id'] == driver_id]
        speed_data = driver_data[driver_data['telemetry_name'] == 'vehspd_can']
        accel_data = driver_data[driver_data['telemetry_name'].str.contains('acc', case=False, na=False)]
        
        if speed_data.empty:
            return {"message": "No speed data available"}
        
        vmax = float(speed_data['telemetry_value'].max())
        vmin = float(speed_data['telemetry_value'].min())
        vavg = float(speed_data['telemetry_value'].mean())
        
        return {
            "driver_id": driver_id,
            "vmax": vmax,
            "vmin": vmin,
            "vavg": vavg,
            "speed_range": vmax - vmin,
            "avg_acceleration": float(accel_data['telemetry_value'].mean()) if not accel_data.empty else 0
        }
    
    def _load_telemetry(self, track_name: str, session: str) -> pd.DataFrame:
        """Load telemetry data."""
        # Try multiple directory patterns
        track_base = track_name.split("_")[0]
        possible_dirs = [
            self.data_dir / track_name / track_name.replace("_", "-"),
            self.data_dir / track_name / track_name,
            self.data_dir / track_name / track_base,
        ]
        
        for track_dir in possible_dirs:
            if track_dir.exists():
                # Look for any telemetry_data.csv file that starts with the session
                for telemetry_file in track_dir.glob(f"{session}_*_telemetry_data.csv"):
                    # Load only first 100k rows for performance
                    return pd.read_csv(telemetry_file, nrows=100000)
        
        return pd.DataFrame()
