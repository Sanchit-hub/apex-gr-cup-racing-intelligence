"""Race strategy and prediction engine."""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any

class StrategyEngine:
    """Calculates race strategy and predictions."""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.pit_loss_time = 25.0  # Average pit stop time loss in seconds
    
    def calculate_pit_window(
        self, 
        track_name: str, 
        session: str, 
        driver_id: str,
        current_lap: int,
        total_laps: int,
        tire_age: int,
        fuel_level: float
    ) -> Dict[str, Any]:
        """Calculate optimal pit stop window."""
        lap_times = self._load_lap_times(track_name, session)
        
        if lap_times.empty:
            return {"error": "No lap time data available"}
        
        driver_laps = lap_times[lap_times['vehicle_id'] == driver_id]
        avg_lap_time = driver_laps['lap_time'].mean() if not driver_laps.empty else 90.0
        
        # Simple tire degradation model: 0.1s per lap after lap 10
        tire_deg_rate = 0.1 if tire_age > 10 else 0.05
        projected_time_loss = tire_deg_rate * (total_laps - current_lap)
        
        # Calculate optimal pit lap
        if projected_time_loss > self.pit_loss_time:
            optimal_pit_lap = current_lap + int((self.pit_loss_time / tire_deg_rate))
        else:
            optimal_pit_lap = None
        
        return {
            "current_lap": current_lap,
            "total_laps": total_laps,
            "tire_age": tire_age,
            "optimal_pit_lap": optimal_pit_lap,
            "projected_time_loss_no_pit": float(projected_time_loss),
            "pit_stop_time_loss": self.pit_loss_time,
            "recommendation": "Pit now" if optimal_pit_lap and optimal_pit_lap <= current_lap + 2 else "Stay out",
            "avg_lap_time": float(avg_lap_time)
        }
    
    def predict_tire_degradation(self, track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
        """Predict tire degradation over race distance."""
        lap_times = self._load_lap_times(track_name, session)
        
        if lap_times.empty:
            return {"error": "No lap time data available"}
        
        driver_laps = lap_times[lap_times['vehicle_id'] == driver_id].sort_values('lap')
        
        if len(driver_laps) < 5:
            return {"message": "Insufficient data for tire degradation analysis"}
        
        # Calculate lap-by-lap delta from best lap
        best_lap = driver_laps['lap_time'].min()
        driver_laps['delta'] = driver_laps['lap_time'] - best_lap
        
        # Simple linear regression for degradation rate
        laps = driver_laps['lap'].values
        deltas = driver_laps['delta'].values
        
        if len(laps) > 1:
            deg_rate = np.polyfit(laps, deltas, 1)[0]
        else:
            deg_rate = 0.0
        
        return {
            "driver_id": driver_id,
            "degradation_rate_per_lap": float(deg_rate),
            "best_lap": float(best_lap),
            "current_delta": float(driver_laps['delta'].iloc[-1]) if len(driver_laps) > 0 else 0,
            "laps_analyzed": len(driver_laps),
            "lap_deltas": driver_laps[['lap', 'delta']].to_dict('records')
        }
    
    def analyze_consistency(self, track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
        """Calculate driver consistency metrics."""
        lap_times = self._load_lap_times(track_name, session)
        
        if lap_times.empty:
            return {"error": "No lap time data available"}
        
        driver_laps = lap_times[lap_times['vehicle_id'] == driver_id]
        
        if driver_laps.empty:
            return {"error": f"No data for driver {driver_id}"}
        
        lap_times_array = driver_laps['lap_time'].values
        best_lap = lap_times_array.min()
        avg_lap = lap_times_array.mean()
        std_dev = lap_times_array.std()
        
        # Consistency score: percentage of laps within 0.5s of best
        within_threshold = np.sum(lap_times_array <= (best_lap + 0.5))
        consistency_pct = (within_threshold / len(lap_times_array)) * 100
        
        # Calculate coefficient of variation
        cv = (std_dev / avg_lap) * 100 if avg_lap > 0 else 0
        
        return {
            "driver_id": driver_id,
            "consistency_score": float(consistency_pct),
            "coefficient_of_variation": float(cv),
            "best_lap": float(best_lap),
            "average_lap": float(avg_lap),
            "std_deviation": float(std_dev),
            "laps_within_05s": int(within_threshold),
            "total_laps": len(lap_times_array)
        }
    
    def _load_lap_times(self, track_name: str, session: str) -> pd.DataFrame:
        """Load lap time data."""
        # Try multiple directory patterns
        track_base = track_name.split("_")[0]
        possible_dirs = [
            self.data_dir / track_name / track_name.replace("_", "-"),
            self.data_dir / track_name / track_name,
            self.data_dir / track_name / track_base,
        ]
        
        for track_dir in possible_dirs:
            if track_dir.exists():
                # Try to load lap start and end files to calculate lap times
                lap_start_files = list(track_dir.glob(f"{session}_*_lap_start.csv"))
                lap_end_files = list(track_dir.glob(f"{session}_*_lap_end.csv"))
                
                if lap_start_files and lap_end_files:
                    start_df = pd.read_csv(lap_start_files[0])
                    end_df = pd.read_csv(lap_end_files[0])
                    
                    # Merge on vehicle_id and lap
                    start_df['start_time'] = pd.to_datetime(start_df['timestamp'])
                    end_df['end_time'] = pd.to_datetime(end_df['timestamp'])
                    
                    merged = pd.merge(
                        start_df[['vehicle_id', 'lap', 'start_time']],
                        end_df[['vehicle_id', 'lap', 'end_time']],
                        on=['vehicle_id', 'lap'],
                        how='inner'
                    )
                    
                    merged['lap_time'] = (merged['end_time'] - merged['start_time']).dt.total_seconds()
                    # Filter out invalid times (lap time should be at least 60 seconds for a race track)
                    return merged[(merged['lap_time'] > 60) & (merged['lap_time'] < 300)]
        
        return pd.DataFrame()
