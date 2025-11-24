"""Advanced racing analytics with vehicle-specific insights."""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List
from backend.config.vehicle_specs import GR86_CUP_SPECS, TRACK_DATA, PERFORMANCE_THRESHOLDS


class AdvancedAnalytics:
    """Provides detailed racing analytics with GR86 Cup car specifications."""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.vehicle_specs = GR86_CUP_SPECS
        self.track_data = TRACK_DATA
    
    def get_detailed_performance(self, track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
        """Get comprehensive performance analysis with vehicle-specific insights."""
        # Load lap times
        lap_times = self._load_lap_times(track_name, session)
        
        if lap_times.empty:
            return {"error": "No data available"}
        
        driver_laps = lap_times[lap_times['vehicle_id'] == driver_id]
        
        if driver_laps.empty:
            return {"error": f"No data for driver {driver_id}"}
        
        # Basic stats
        best_lap = driver_laps['lap_time'].min()
        avg_lap = driver_laps['lap_time'].mean()
        std_lap = driver_laps['lap_time'].std()
        
        # Track info
        track_info = self.track_data.get(track_name, {})
        track_record = track_info.get('track_record', {}).get('time', 0)
        
        # Calculate delta to track record
        delta_to_record = best_lap - track_record if track_record > 0 else 0
        
        # Consistency analysis
        laps_within_05s = len(driver_laps[driver_laps['lap_time'] <= (best_lap + 0.5)])
        laps_within_1s = len(driver_laps[driver_laps['lap_time'] <= (best_lap + 1.0)])
        consistency_pct = (laps_within_05s / len(driver_laps)) * 100
        
        # Performance rating
        if consistency_pct >= 80:
            rating = "Elite"
        elif consistency_pct >= 60:
            rating = "Professional"
        elif consistency_pct >= 40:
            rating = "Advanced"
        else:
            rating = "Developing"
        
        # Theoretical best lap (if we had sector data)
        theoretical_best = best_lap * 0.98  # Estimate 2% improvement potential
        
        # Pace analysis
        pace_analysis = self._analyze_pace(driver_laps)
        
        return {
            "driver_id": driver_id,
            "track": track_info.get('name', track_name),
            "session": session,
            "vehicle": "Toyota GR86 Cup",
            "performance": {
                "best_lap": float(best_lap),
                "average_lap": float(avg_lap),
                "theoretical_best": float(theoretical_best),
                "delta_to_record": float(delta_to_record),
                "std_deviation": float(std_lap)
            },
            "consistency": {
                "score": float(consistency_pct),
                "rating": rating,
                "laps_within_05s": int(laps_within_05s),
                "laps_within_1s": int(laps_within_1s),
                "total_laps": len(driver_laps)
            },
            "pace_analysis": pace_analysis,
            "vehicle_specs": {
                "horsepower": self.vehicle_specs['engine']['horsepower'],
                "weight_kg": self.vehicle_specs['performance']['weight_kg'],
                "top_speed_kmh": self.vehicle_specs['performance']['top_speed_kmh']
            },
            "track_info": {
                "length_km": track_info.get('length_km', 0),
                "turns": track_info.get('turns', 0),
                "elevation_change_m": track_info.get('elevation_change_m', 0),
                "track_record": track_record
            }
        }
    
    def get_speed_analysis(self, track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
        """Analyze speed data with GR86 Cup car limits."""
        telemetry = self._load_telemetry(track_name, session)
        
        if telemetry.empty:
            return {"error": "No telemetry data available"}
        
        driver_data = telemetry[telemetry['vehicle_id'] == driver_id]
        speed_data = driver_data[driver_data['telemetry_name'] == 'vehspd_can']
        
        if speed_data.empty:
            return {"message": "No speed data available"}
        
        vmax = float(speed_data['telemetry_value'].max())
        vmin = float(speed_data['telemetry_value'].min())
        vavg = float(speed_data['telemetry_value'].mean())
        
        # Calculate percentage of theoretical max
        theoretical_max = self.vehicle_specs['performance']['top_speed_kmh']
        speed_utilization = (vmax / theoretical_max) * 100
        
        # Speed zones
        high_speed_time = len(speed_data[speed_data['telemetry_value'] > 150]) / len(speed_data) * 100
        mid_speed_time = len(speed_data[(speed_data['telemetry_value'] > 100) & (speed_data['telemetry_value'] <= 150)]) / len(speed_data) * 100
        low_speed_time = len(speed_data[speed_data['telemetry_value'] <= 100]) / len(speed_data) * 100
        
        return {
            "driver_id": driver_id,
            "speed_metrics": {
                "vmax_kmh": vmax,
                "vmin_kmh": vmin,
                "vavg_kmh": vavg,
                "speed_range_kmh": vmax - vmin
            },
            "vehicle_comparison": {
                "theoretical_max_kmh": theoretical_max,
                "speed_utilization_pct": float(speed_utilization),
                "gap_to_max_kmh": float(theoretical_max - vmax)
            },
            "speed_distribution": {
                "high_speed_pct": float(high_speed_time),
                "mid_speed_pct": float(mid_speed_time),
                "low_speed_pct": float(low_speed_time)
            }
        }
    
    def get_braking_analysis(self, track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
        """Analyze braking with real physics and Brembo brake specs."""
        telemetry = self._load_telemetry(track_name, session)
        
        if telemetry.empty:
            return {"error": "No telemetry data available"}
        
        driver_data = telemetry[telemetry['vehicle_id'] == driver_id]
        
        # Get brake pressure data (in bar)
        brake_front = driver_data[driver_data['telemetry_name'] == 'pbrake_f']['telemetry_value']
        brake_rear = driver_data[driver_data['telemetry_name'] == 'pbrake_r']['telemetry_value']
        
        # Get longitudinal acceleration (G-forces)
        accx = driver_data[driver_data['telemetry_name'] == 'accx_can']['telemetry_value']
        
        # Get speed data
        speed = driver_data[driver_data['telemetry_name'] == 'speed']['telemetry_value']
        
        if brake_front.empty and brake_rear.empty:
            return {"message": "No braking data available"}
        
        # Combine front and rear brake pressure
        all_brake_data = pd.concat([brake_front, brake_rear])
        
        # Braking zones detection (pressure > 2 bar = braking)
        braking_threshold = 2.0  # bar
        brake_applications = 0
        in_braking_zone = False
        
        for pressure in all_brake_data:
            if pressure > braking_threshold and not in_braking_zone:
                brake_applications += 1
                in_braking_zone = True
            elif pressure <= braking_threshold:
                in_braking_zone = False
        
        # Brake pressure statistics (in bar) - filter outliers
        # Use 99th percentile as max to avoid sensor spikes
        max_front_pressure = float(brake_front.quantile(0.99)) if not brake_front.empty else 0
        max_rear_pressure = float(brake_rear.quantile(0.99)) if not brake_rear.empty else 0
        avg_front_pressure = float(brake_front[brake_front > braking_threshold].mean()) if not brake_front.empty else 0
        avg_rear_pressure = float(brake_rear[brake_rear > braking_threshold].mean()) if not brake_rear.empty else 0
        
        # Typical GR86 Cup max brake pressure: ~14 bar front, ~10 bar rear
        max_theoretical_front = 14.0  # bar
        max_theoretical_rear = 10.0   # bar
        
        # Cap values at theoretical max (sensor spikes can exceed physical limits)
        max_front_pressure = min(max_front_pressure, max_theoretical_front * 1.1)
        max_rear_pressure = min(max_rear_pressure, max_theoretical_rear * 1.1)
        
        # Brake bias (front vs rear distribution)
        if max_front_pressure > 0 and max_rear_pressure > 0:
            brake_bias_front = (max_front_pressure / (max_front_pressure + max_rear_pressure)) * 100
        else:
            brake_bias_front = 70.0  # Default GR86 bias
        
        # G-force analysis from actual acceleration data
        if not accx.empty:
            # Negative accx = braking (deceleration)
            braking_g_forces = accx[accx < -0.1]  # Filter for actual braking
            max_braking_g = float(abs(braking_g_forces.min())) if not braking_g_forces.empty else 0
            avg_braking_g = float(abs(braking_g_forces.mean())) if not braking_g_forces.empty else 0
        else:
            # Estimate from brake pressure (14 bar ≈ 1.2G for GR86)
            max_braking_g = (max_front_pressure / max_theoretical_front) * 1.2
            avg_braking_g = (avg_front_pressure / max_theoretical_front) * 1.2
        
        # Braking efficiency (how close to theoretical max)
        front_efficiency = (max_front_pressure / max_theoretical_front) * 100
        rear_efficiency = (max_rear_pressure / max_theoretical_rear) * 100
        
        # Braking consistency (std dev of brake pressure during braking)
        braking_consistency = float(brake_front[brake_front > braking_threshold].std()) if not brake_front.empty else 0
        
        # Trail braking detection (braking while turning)
        # Get lateral G data
        accy_data = driver_data[driver_data['telemetry_name'] == 'accy_can']['telemetry_value']
        if not accy_data.empty and not brake_front.empty:
            # Align data by index
            combined = pd.DataFrame({
                'brake': brake_front.values[:min(len(brake_front), len(accy_data))],
                'lateral_g': accy_data.values[:min(len(brake_front), len(accy_data))]
            })
            # Trail braking = braking (>2 bar) + lateral load (>0.3G)
            trail_braking_points = combined[(combined['brake'] > 2.0) & (abs(combined['lateral_g']) > 0.3)]
            trail_braking_pct = (len(trail_braking_points) / len(combined[combined['brake'] > 2.0]) * 100) if len(combined[combined['brake'] > 2.0]) > 0 else 0
        else:
            trail_braking_pct = 0
        
        # Braking zones per lap (typical for Barber: 8-10 heavy braking zones)
        track_info = self.track_data.get(track_name, {})
        expected_brake_zones = track_info.get('turns', 17) * 0.6  # ~60% of turns are braking zones
        
        return {
            "driver_id": driver_id,
            "braking_metrics": {
                "brake_applications": int(brake_applications / 2),  # Divide by 2 since we counted front+rear
                "expected_per_lap": int(expected_brake_zones),
                "max_front_pressure_bar": round(max_front_pressure, 2),
                "max_rear_pressure_bar": round(max_rear_pressure, 2),
                "avg_front_pressure_bar": round(avg_front_pressure, 2),
                "avg_rear_pressure_bar": round(avg_rear_pressure, 2),
                "brake_bias_front_pct": round(brake_bias_front, 1),
                "consistency_bar": round(braking_consistency, 2)
            },
            "g_forces": {
                "max_braking_g": round(max_braking_g, 2),
                "avg_braking_g": round(avg_braking_g, 2),
                "vehicle_limit_g": 1.2,  # GR86 Cup typical max
                "utilization_pct": round((max_braking_g / 1.2) * 100, 1)
            },
            "efficiency": {
                "front_brake_efficiency_pct": round(front_efficiency, 1),
                "rear_brake_efficiency_pct": round(rear_efficiency, 1),
                "overall_efficiency_pct": round((front_efficiency + rear_efficiency) / 2, 1)
            },
            "technique": {
                "trail_braking_pct": round(trail_braking_pct, 1),
                "rating": "Advanced" if trail_braking_pct > 30 else "Intermediate" if trail_braking_pct > 15 else "Basic"
            },
            "brake_system": {
                "front": self.vehicle_specs['brakes']['front'],
                "rear": self.vehicle_specs['brakes']['rear'],
                "abs": self.vehicle_specs['brakes']['abs'],
                "max_pressure_front_bar": max_theoretical_front,
                "max_pressure_rear_bar": max_theoretical_rear
            }
        }
    
    def _analyze_pace(self, driver_laps: pd.DataFrame) -> Dict[str, Any]:
        """Analyze pace evolution over stint."""
        if len(driver_laps) < 5:
            return {"message": "Insufficient laps for pace analysis"}
        
        # Split into thirds
        total_laps = len(driver_laps)
        third = total_laps // 3
        
        early_laps = driver_laps.iloc[:third]
        mid_laps = driver_laps.iloc[third:2*third]
        late_laps = driver_laps.iloc[2*third:]
        
        return {
            "early_stint": {
                "avg_lap_time": float(early_laps['lap_time'].mean()),
                "best_lap": float(early_laps['lap_time'].min())
            },
            "mid_stint": {
                "avg_lap_time": float(mid_laps['lap_time'].mean()),
                "best_lap": float(mid_laps['lap_time'].min())
            },
            "late_stint": {
                "avg_lap_time": float(late_laps['lap_time'].mean()),
                "best_lap": float(late_laps['lap_time'].min())
            },
            "degradation": {
                "early_to_late_delta": float(late_laps['lap_time'].mean() - early_laps['lap_time'].mean())
            }
        }
    
    def _load_lap_times(self, track_name: str, session: str) -> pd.DataFrame:
        """Load lap time data."""
        track_base = track_name.split("_")[0]
        possible_dirs = [
            self.data_dir / track_name / track_name.replace("_", "-"),
            self.data_dir / track_name / track_name,
            self.data_dir / track_name / track_base,
        ]
        
        for track_dir in possible_dirs:
            if track_dir.exists():
                lap_start_files = list(track_dir.glob(f"{session}_*_lap_start.csv"))
                lap_end_files = list(track_dir.glob(f"{session}_*_lap_end.csv"))
                
                if lap_start_files and lap_end_files:
                    start_df = pd.read_csv(lap_start_files[0])
                    end_df = pd.read_csv(lap_end_files[0])
                    
                    start_df['start_time'] = pd.to_datetime(start_df['timestamp'])
                    end_df['end_time'] = pd.to_datetime(end_df['timestamp'])
                    
                    merged = pd.merge(
                        start_df[['vehicle_id', 'lap', 'start_time']],
                        end_df[['vehicle_id', 'lap', 'end_time']],
                        on=['vehicle_id', 'lap'],
                        how='inner'
                    )
                    
                    merged['lap_time'] = (merged['end_time'] - merged['start_time']).dt.total_seconds()
                    return merged[(merged['lap_time'] > 60) & (merged['lap_time'] < 300)]
        
        return pd.DataFrame()
    
    def _load_telemetry(self, track_name: str, session: str) -> pd.DataFrame:
        """Load telemetry data."""
        track_base = track_name.split("_")[0]
        possible_dirs = [
            self.data_dir / track_name / track_name.replace("_", "-"),
            self.data_dir / track_name / track_name,
            self.data_dir / track_name / track_base,
        ]
        
        for track_dir in possible_dirs:
            if track_dir.exists():
                for telemetry_file in track_dir.glob(f"{session}_*_telemetry_data.csv"):
                    return pd.read_csv(telemetry_file, nrows=100000)
        
        return pd.DataFrame()
