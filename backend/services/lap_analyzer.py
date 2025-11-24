"""Lap time and sector analysis service."""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
import os

class LapAnalyzer:
    """Analyzes lap times and sector performance."""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.use_s3 = os.getenv('USE_S3_DATA', 'false').lower() == 'true'
        
        if self.use_s3:
            from backend.services.s3_data_loader import S3DataLoader
            self.s3_loader = S3DataLoader()
    
    def get_available_tracks(self) -> List[str]:
        """Get list of available tracks."""
        if self.use_s3:
            return sorted(self.s3_loader.get_available_tracks())
        
        if not self.data_dir.exists():
            return []
        
        tracks = []
        for d in self.data_dir.iterdir():
            if d.is_dir() and not d.name.startswith("_"):
                # Skip duplicate "barber" if "barber_motorsports_park" exists
                if d.name == "barber" and (self.data_dir / "barber_motorsports_park").exists():
                    continue
                tracks.append(d.name)
        
        return sorted(tracks)
    
    def get_sessions(self, track_name: str) -> List[str]:
        """Get available sessions for a track."""
        if self.use_s3:
            sessions = self.s3_loader.get_available_sessions(track_name)
            if not sessions:
                raise ValueError(f"Track {track_name} not found")
            return sorted(sessions)
        
        # Try multiple directory patterns
        track_base = track_name.split("_")[0]  # e.g., "barber" from "barber_motorsports_park"
        possible_dirs = [
            self.data_dir / track_name / track_name.replace("_", "-"),
            self.data_dir / track_name / track_name,
            self.data_dir / track_name / track_base,  # e.g., data/barber_motorsports_park/barber
        ]
        
        track_dir = None
        for d in possible_dirs:
            if d.exists():
                track_dir = d
                break
        
        if not track_dir:
            raise ValueError(f"Track {track_name} not found")
        
        sessions = set()
        # Look for lap_start files (more reliable than lap_time)
        for file in track_dir.glob("R*_lap_start.csv"):
            session = file.stem.split("_")[0]
            sessions.add(session)
        
        # Fallback to lap_time if no lap_start found
        if not sessions:
            for file in track_dir.glob("R*_lap_time.csv"):
                session = file.stem.split("_")[0]
                sessions.add(session)
        
        return sorted(list(sessions))
    
    def get_drivers(self, track_name: str, session: str) -> List[str]:
        """Get list of drivers for a session."""
        lap_times = self._load_lap_times(track_name, session)
        
        if lap_times.empty:
            return []
        
        drivers = sorted(lap_times['vehicle_id'].unique().tolist())
        return drivers
    
    def calculate_best_lap(self, track_name: str, session: str) -> Dict[str, Any]:
        """Calculate theoretical best lap from combined best sectors."""
        lap_times = self._load_lap_times(track_name, session)
        
        if lap_times.empty:
            return {"error": "No lap time data available"}
        
        # Calculate lap times from timestamps if not present
        if 'lap_time' not in lap_times.columns:
            lap_times['timestamp'] = pd.to_datetime(lap_times['timestamp'])
            lap_times = lap_times.sort_values(['vehicle_id', 'lap'])
            lap_times['lap_time'] = lap_times.groupby('vehicle_id')['timestamp'].diff().dt.total_seconds()
        
        # Remove invalid lap times
        lap_times = lap_times[lap_times['lap_time'] > 0]
        
        if lap_times.empty:
            return {"error": "No valid lap times found"}
        
        # Find best lap time
        best_lap = lap_times.nsmallest(1, 'lap_time')
        
        return {
            "best_lap_time": float(best_lap['lap_time'].iloc[0]),
            "driver_id": str(best_lap['vehicle_id'].iloc[0]),
            "lap_number": int(best_lap['lap'].iloc[0]),
            "track": track_name,
            "session": session
        }
    
    def analyze_driver_performance(self, track_name: str, session: str, driver_id: str) -> Dict[str, Any]:
        """Comprehensive driver performance analysis."""
        lap_times = self._load_lap_times(track_name, session)
        
        if lap_times.empty:
            return {"error": "No data available"}
        
        # Calculate lap times from timestamps if not present
        if 'lap_time' not in lap_times.columns:
            lap_times['timestamp'] = pd.to_datetime(lap_times['timestamp'])
            lap_times = lap_times.sort_values(['vehicle_id', 'lap'])
            lap_times['lap_time'] = lap_times.groupby('vehicle_id')['timestamp'].diff().dt.total_seconds()
        
        driver_laps = lap_times[lap_times['vehicle_id'] == driver_id]
        driver_laps = driver_laps[driver_laps['lap_time'] > 0]  # Remove invalid times
        
        if driver_laps.empty:
            return {"error": f"No data for driver {driver_id}"}
        
        best_lap = driver_laps['lap_time'].min()
        avg_lap = driver_laps['lap_time'].mean()
        std_lap = driver_laps['lap_time'].std()
        
        # Calculate consistency (lower is better)
        consistency = (std_lap / avg_lap) * 100 if avg_lap > 0 else 0
        
        return {
            "driver_id": driver_id,
            "best_lap": float(best_lap),
            "average_lap": float(avg_lap),
            "std_deviation": float(std_lap),
            "consistency_score": float(100 - consistency),
            "total_laps": len(driver_laps),
            "lap_times": driver_laps['lap_time'].tolist()
        }
    
    def analyze_sectors(self, track_name: str, session: str) -> Dict[str, Any]:
        """Sector-by-sector analysis."""
        sections = self._load_sections(track_name, session)
        
        if sections.empty:
            return {"message": "Sector data not available for this track"}
        
        # Group by driver and calculate sector performance
        sector_analysis = {}
        for driver in sections['vehicle_id'].unique():
            driver_sections = sections[sections['vehicle_id'] == driver]
            sector_analysis[driver] = {
                "avg_sector_time": float(driver_sections['section_time'].mean()),
                "best_sector": float(driver_sections['section_time'].min())
            }
        
        return {"sector_analysis": sector_analysis}
    
    def _load_lap_times(self, track_name: str, session: str) -> pd.DataFrame:
        """Load lap time data."""
        if self.use_s3:
            # Load from S3
            start_df = self.s3_loader.load_lap_times(track_name, session)
            if start_df is None:
                return pd.DataFrame()
            
            # Try to load lap end file
            end_df = self.s3_loader.load_lap_times(track_name, session.replace('_lap_start', '_lap_end'))
            
            if start_df is not None and end_df is not None:
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
        
        # Load from local files
        # Try multiple directory patterns
        track_base = track_name.split("_")[0]  # e.g., "barber" from "barber_motorsports_park"
        possible_dirs = [
            self.data_dir / track_name / track_name.replace("_", "-"),
            self.data_dir / track_name / track_name,
            self.data_dir / track_name / track_base,  # e.g., data/barber_motorsports_park/barber
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
    
    def _load_sections(self, track_name: str, session: str) -> pd.DataFrame:
        """Load section/sector data."""
        # Try multiple directory patterns
        track_base = track_name.split("_")[0]
        possible_dirs = [
            self.data_dir / track_name / track_name.replace("_", "-"),
            self.data_dir / track_name / track_name,
            self.data_dir / track_name / track_base,
        ]
        
        for track_dir in possible_dirs:
            if track_dir.exists():
                section_file = track_dir / f"23_AnalysisEnduranceWithSections_{session.replace('R', 'Race ')}_Anonymized.CSV"
                if section_file.exists():
                    return pd.read_csv(section_file)
        
        return pd.DataFrame()
