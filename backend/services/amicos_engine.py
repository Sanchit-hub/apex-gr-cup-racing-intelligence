"""
AMICOS - Adaptive Momentum-Inertia Cornering Optimization System
Physics-based cornering analysis using vehicle dynamics and sensor fusion
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Tuple
from scipy.signal import find_peaks
from backend.config.vehicle_specs import GR86_CUP_SPECS, TRACK_DATA


class AMICOSEngine:
    """Advanced physics-based cornering optimization system."""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.vehicle_specs = GR86_CUP_SPECS
        self.track_data = TRACK_DATA
        
        # GR86 Cup physical constants
        self.mass_kg = 1270  # kg
        self.wheelbase_m = 2.575  # meters
        self.cg_height_m = 0.48  # estimated center of gravity height
        self.track_width_m = 1.52  # meters
        self.moment_of_inertia = 1800  # kg⋅m² (estimated yaw inertia)
        
        # Tire physics
        self.mu_dry = 1.1  # coefficient of friction (Michelin Cup 2)
        self.g = 9.81  # m/s²
        
    def analyze_cornering_performance(self, track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
        """Complete cornering analysis with momentum optimization."""
        telemetry = self._load_telemetry(track_name, session)
        
        if telemetry.empty:
            return {"error": "No telemetry data available"}
        
        driver_data = telemetry[telemetry['vehicle_id'] == driver_id]
        
        if driver_data.empty:
            return {"error": f"No data for driver {driver_id}"}
        
        # Extract sensor data
        speed_data = self._extract_channel(driver_data, 'speed')  # km/h
        accx_data = self._extract_channel(driver_data, 'accx_can')  # longitudinal G
        accy_data = self._extract_channel(driver_data, 'accy_can')  # lateral G
        steering_data = self._extract_channel(driver_data, 'Steering_Angle')
        
        # Detect corners
        corners = self._detect_corners(speed_data, accy_data, steering_data)
        
        # Analyze each corner
        corner_analysis = []
        for corner in corners:
            analysis = self._analyze_single_corner(
                corner, speed_data, accx_data, accy_data, steering_data
            )
            corner_analysis.append(analysis)
        
        # Calculate driver DNA
        driver_dna = self._calculate_driver_dna(corner_analysis, driver_data)
        
        # Grip utilization analysis
        grip_analysis = self._analyze_grip_utilization(accx_data, accy_data)
        
        # Momentum efficiency
        momentum_efficiency = self._calculate_momentum_efficiency(corner_analysis)
        
        return {
            "driver_id": driver_id,
            "corners_detected": len(corners),
            "corner_analysis": corner_analysis[:5],  # Top 5 corners
            "driver_dna": driver_dna,
            "grip_utilization": grip_analysis,
            "momentum_efficiency": momentum_efficiency,
            "recommendations": self._generate_recommendations(corner_analysis, driver_dna)
        }
    
    def _detect_corners(self, speed_data: pd.Series, accy_data: pd.Series, 
                       steering_data: pd.Series) -> List[Dict]:
        """Detect corners using lateral G-force and steering angle."""
        if accy_data.empty:
            return []
        
        # Corner = high lateral G (>0.4G) + significant steering input
        lateral_g_threshold = 0.4
        corner_mask = abs(accy_data) > lateral_g_threshold
        
        # Find corner regions
        corners = []
        in_corner = False
        corner_start = 0
        
        for idx, is_cornering in enumerate(corner_mask):
            if is_cornering and not in_corner:
                corner_start = idx
                in_corner = True
            elif not is_cornering and in_corner:
                corner_end = idx
                if corner_end - corner_start > 10:  # Minimum 10 data points
                    corners.append({
                        'start_idx': corner_start,
                        'end_idx': corner_end,
                        'apex_idx': corner_start + (corner_end - corner_start) // 2
                    })
                in_corner = False
        
        return corners
    
    def _analyze_single_corner(self, corner: Dict, speed_data: pd.Series,
                               accx_data: pd.Series, accy_data: pd.Series,
                               steering_data: pd.Series) -> Dict[str, Any]:
        """Analyze a single corner with physics-based metrics."""
        start_idx = corner['start_idx']
        end_idx = corner['end_idx']
        apex_idx = corner['apex_idx']
        
        # Extract corner data
        corner_speed = speed_data.iloc[start_idx:end_idx]
        corner_accx = accx_data.iloc[start_idx:end_idx]
        corner_accy = accy_data.iloc[start_idx:end_idx]
        corner_steering = steering_data.iloc[start_idx:end_idx]
        
        # Entry, apex, exit speeds (km/h)
        entry_speed = corner_speed.iloc[0] if len(corner_speed) > 0 else 0
        apex_speed = corner_speed.iloc[len(corner_speed)//2] if len(corner_speed) > 0 else 0
        exit_speed = corner_speed.iloc[-1] if len(corner_speed) > 0 else 0
        
        # Convert to m/s for physics calculations
        entry_speed_ms = entry_speed / 3.6
        apex_speed_ms = apex_speed / 3.6
        exit_speed_ms = exit_speed / 3.6
        
        # Maximum lateral G in corner
        max_lateral_g = abs(corner_accy).max() if not corner_accy.empty else 0
        
        # Calculate corner radius from speed and lateral acceleration
        # a_lateral = v² / r  →  r = v² / a_lateral
        if max_lateral_g > 0.1:
            corner_radius = (apex_speed_ms ** 2) / (max_lateral_g * self.g)
        else:
            corner_radius = 100  # default
        
        # Theoretical maximum speed for this corner
        # V_max = sqrt(μ × g × R)
        theoretical_max_speed_ms = np.sqrt(self.mu_dry * self.g * corner_radius)
        theoretical_max_speed_kmh = theoretical_max_speed_ms * 3.6
        
        # Momentum analysis
        # Linear momentum: p = m × v
        entry_momentum = self.mass_kg * entry_speed_ms
        apex_momentum = self.mass_kg * apex_speed_ms
        exit_momentum = self.mass_kg * exit_speed_ms
        
        # Angular momentum (simplified): L = I × ω
        # ω (yaw rate) ≈ v / r
        if corner_radius > 0:
            apex_yaw_rate = apex_speed_ms / corner_radius
            angular_momentum = self.moment_of_inertia * apex_yaw_rate
        else:
            apex_yaw_rate = 0
            angular_momentum = 0
        
        # Weight transfer calculation
        # Lateral load transfer: ΔF = (m × a_y × h) / t
        # where h = CG height, t = track width
        if max_lateral_g > 0:
            lateral_load_transfer = (self.mass_kg * max_lateral_g * self.g * self.cg_height_m) / self.track_width_m
        else:
            lateral_load_transfer = 0
        
        # Grip utilization (% of traction circle)
        # Combined acceleration: a_total = sqrt(a_x² + a_y²)
        if not corner_accx.empty and not corner_accy.empty:
            combined_g = np.sqrt(corner_accx**2 + corner_accy**2)
            max_combined_g = combined_g.max()
            grip_utilization = (max_combined_g / self.mu_dry) * 100
        else:
            max_combined_g = 0
            grip_utilization = 0
        
        # Speed efficiency (% of theoretical max)
        speed_efficiency = (apex_speed / theoretical_max_speed_kmh * 100) if theoretical_max_speed_kmh > 0 else 0
        
        # Momentum efficiency (exit vs entry)
        momentum_gain = ((exit_momentum - entry_momentum) / entry_momentum * 100) if entry_momentum > 0 else 0
        
        # Helper to safely round and handle NaN
        def safe_round(value, decimals=1):
            return round(float(value), decimals) if not np.isnan(value) and not np.isinf(value) else 0.0
        
        return {
            "corner_number": len(corner_speed),
            "entry_speed_kmh": safe_round(entry_speed, 1),
            "apex_speed_kmh": safe_round(apex_speed, 1),
            "exit_speed_kmh": safe_round(exit_speed, 1),
            "theoretical_max_speed_kmh": safe_round(theoretical_max_speed_kmh, 1),
            "speed_efficiency_pct": safe_round(speed_efficiency, 1),
            "corner_radius_m": safe_round(corner_radius, 1),
            "max_lateral_g": safe_round(max_lateral_g, 2),
            "max_combined_g": safe_round(max_combined_g, 2),
            "grip_utilization_pct": safe_round(grip_utilization, 1),
            "angular_momentum": safe_round(angular_momentum, 1),
            "yaw_rate_rad_s": safe_round(apex_yaw_rate, 3),
            "lateral_load_transfer_n": safe_round(lateral_load_transfer, 1),
            "momentum_gain_pct": safe_round(momentum_gain, 1)
        }
    
    def _calculate_driver_dna(self, corner_analysis: List[Dict], driver_data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate unique driver fingerprint/DNA."""
        if not corner_analysis:
            return {"message": "Insufficient corner data"}
        
        # Braking signature
        brake_data = self._extract_channel(driver_data, 'pbrake_f')
        if not brake_data.empty and len(brake_data) > 0:
            avg_brake_pressure = brake_data[brake_data > 2].mean()
            max_brake_pressure = brake_data.quantile(0.99)
            brake_aggression = (avg_brake_pressure / max_brake_pressure * 100) if max_brake_pressure > 0 and not np.isnan(avg_brake_pressure) else 50
        else:
            brake_aggression = 50
        
        # Throttle signature
        throttle_data = self._extract_channel(driver_data, 'aps')
        if not throttle_data.empty and len(throttle_data) > 0:
            avg_throttle = throttle_data[throttle_data > 10].mean()
            throttle_std = throttle_data.std()
            throttle_smoothness = max(0, 100 - throttle_std) if not np.isnan(throttle_std) else 50
        else:
            avg_throttle = 0
            throttle_smoothness = 50
        
        # Cornering style
        avg_grip_utilization = np.mean([c['grip_utilization_pct'] for c in corner_analysis]) if corner_analysis else 50
        avg_speed_efficiency = np.mean([c['speed_efficiency_pct'] for c in corner_analysis]) if corner_analysis else 50
        
        # Classify driving style
        if avg_grip_utilization > 85 and brake_aggression > 70:
            style = "Aggressive"
        elif avg_speed_efficiency > 90 and throttle_smoothness > 80:
            style = "Smooth & Fast"
        elif avg_grip_utilization < 75:
            style = "Conservative"
        else:
            style = "Balanced"
        
        return {
            "driving_style": style,
            "brake_aggression_pct": round(brake_aggression, 1),
            "throttle_smoothness_pct": round(throttle_smoothness, 1),
            "avg_grip_utilization_pct": round(avg_grip_utilization, 1),
            "avg_speed_efficiency_pct": round(avg_speed_efficiency, 1),
            "signature": f"{style} - {int(avg_grip_utilization)}% grip, {int(brake_aggression)}% brake"
        }
    
    def _analyze_grip_utilization(self, accx_data: pd.Series, accy_data: pd.Series) -> Dict[str, Any]:
        """Analyze grip utilization using traction circle."""
        if accx_data.empty or accy_data.empty:
            return {"message": "No acceleration data"}
        
        # Calculate combined G-force
        combined_g = np.sqrt(accx_data**2 + accy_data**2)
        
        # Traction circle analysis
        max_combined_g = combined_g.max()
        avg_combined_g = combined_g.mean()
        
        # Time spent in different grip zones
        total_points = len(combined_g)
        high_grip = len(combined_g[combined_g > 0.8]) / total_points * 100  # >0.8G
        mid_grip = len(combined_g[(combined_g > 0.4) & (combined_g <= 0.8)]) / total_points * 100
        low_grip = len(combined_g[combined_g <= 0.4]) / total_points * 100
        
        # Grip efficiency (how close to theoretical limit)
        grip_efficiency = (max_combined_g / self.mu_dry) * 100
        
        return {
            "max_combined_g": round(max_combined_g, 2),
            "avg_combined_g": round(avg_combined_g, 2),
            "grip_efficiency_pct": round(grip_efficiency, 1),
            "time_in_high_grip_pct": round(high_grip, 1),
            "time_in_mid_grip_pct": round(mid_grip, 1),
            "time_in_low_grip_pct": round(low_grip, 1),
            "theoretical_limit_g": self.mu_dry
        }
    
    def _calculate_momentum_efficiency(self, corner_analysis: List[Dict]) -> Dict[str, Any]:
        """Calculate overall momentum management efficiency."""
        if not corner_analysis:
            return {"message": "No corner data"}
        
        # Average momentum gain across all corners
        momentum_gains = [c['momentum_gain_pct'] for c in corner_analysis]
        avg_momentum_gain = np.mean(momentum_gains)
        
        # Speed efficiency across corners
        speed_efficiencies = [c['speed_efficiency_pct'] for c in corner_analysis]
        avg_speed_efficiency = np.mean(speed_efficiencies)
        
        # Overall momentum efficiency score
        momentum_score = (avg_momentum_gain + avg_speed_efficiency) / 2
        
        return {
            "avg_momentum_gain_pct": round(avg_momentum_gain, 1),
            "avg_speed_efficiency_pct": round(avg_speed_efficiency, 1),
            "momentum_efficiency_score": round(momentum_score, 1),
            "rating": "Excellent" if momentum_score > 80 else "Good" if momentum_score > 60 else "Needs Improvement"
        }
    
    def _generate_recommendations(self, corner_analysis: List[Dict], driver_dna: Dict) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []
        
        if not corner_analysis:
            return ["Insufficient data for recommendations"]
        
        # Speed efficiency recommendations
        avg_speed_eff = np.mean([c['speed_efficiency_pct'] for c in corner_analysis])
        if avg_speed_eff < 85:
            recommendations.append(f"⚡ Carry {round(100-avg_speed_eff, 1)}% more speed through corners - you're leaving time on the table")
        
        # Grip utilization recommendations
        avg_grip = np.mean([c['grip_utilization_pct'] for c in corner_analysis])
        if avg_grip < 80:
            recommendations.append(f"🎯 Push harder! Using only {round(avg_grip, 1)}% of available grip - aim for 90%+")
        elif avg_grip > 95:
            recommendations.append("⚠️ Very aggressive! Consider slight margin for safety")
        
        # Momentum recommendations
        low_momentum_corners = [c for c in corner_analysis if c['momentum_gain_pct'] < 0]
        if len(low_momentum_corners) > len(corner_analysis) * 0.3:
            recommendations.append("📉 Losing momentum in 30%+ of corners - focus on exit speed over entry speed")
        
        # Driving style recommendations
        if driver_dna.get('driving_style') == 'Conservative':
            recommendations.append("🏁 Be more aggressive with throttle application - you have grip available")
        elif driver_dna.get('driving_style') == 'Aggressive':
            recommendations.append("🎨 Smooth inputs will improve consistency and tire life")
        
        return recommendations[:5]  # Top 5 recommendations
    
    def _extract_channel(self, driver_data: pd.DataFrame, channel_name: str) -> pd.Series:
        """Extract a specific telemetry channel."""
        channel_data = driver_data[driver_data['telemetry_name'] == channel_name]
        return channel_data['telemetry_value'] if not channel_data.empty else pd.Series()
    
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
                # Try both naming patterns
                for pattern in [f"{session}_*_telemetry_data.csv", f"{session}_*_telemetry.csv"]:
                    for telemetry_file in track_dir.glob(pattern):
                        return pd.read_csv(telemetry_file, nrows=200000)  # Increased for corner detection
        
        return pd.DataFrame()
