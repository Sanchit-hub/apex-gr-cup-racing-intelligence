"""S3 Data Loader for cloud-hosted race data."""
import boto3
import pandas as pd
from io import StringIO
import os
from typing import Optional
from pathlib import Path

class S3DataLoader:
    """Load race data from AWS S3."""
    
    def __init__(self):
        """Initialize S3 client with AWS credentials from environment."""
        self.s3_client = boto3.client('s3')
        self.bucket_name = os.getenv('S3_BUCKET_NAME', 'apex-racing-data')
        self.base_url = f"https://{self.bucket_name}.s3.amazonaws.com"
        
    def _get_s3_key(self, track_name: str, filename: str) -> list:
        """Generate S3 keys for a file.
        
        Args:
            track_name: Name of the track (e.g., 'barber_motorsports_park')
            filename: Name of the file (e.g., 'R1_barber_lap_start.csv')
            
        Returns:
            List of possible S3 keys to try
        """
        # Handle different track structures
        track_base = track_name.split("_")[0]  # e.g., "barber" from "barber_motorsports_park"
        
        # Extract session from filename if present (e.g., "R1" from "R1_barber_lap_start.csv")
        session = None
        if filename.startswith("R1") or filename.startswith("R2"):
            session = filename[:2]
        
        # Try multiple subdirectory patterns
        possible_keys = [
            f"data/{track_name}/{track_base}/{filename}",  # data/barber_motorsports_park/barber/file.csv
            f"data/{track_name}/{filename}",  # data/indianapolis/file.csv
        ]
        
        # Add Race 1/Race 2 patterns for COTA-style structure
        if session:
            race_num = session[1]  # "1" or "2"
            possible_keys.extend([
                f"data/{track_name}/Race {race_num}/{filename}",  # data/COTA/Race 1/file.csv
                f"data/{track_name}/race {race_num}/{filename}",  # data/COTA/race 1/file.csv (lowercase)
            ])
        
        return possible_keys
    
    def _download_csv_from_s3(self, s3_key: str) -> Optional[pd.DataFrame]:
        """Download and parse CSV from S3.
        
        Args:
            s3_key: S3 object key
            
        Returns:
            DataFrame if successful, None if error occurs
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
            csv_content = response['Body'].read().decode('utf-8')
            return pd.read_csv(StringIO(csv_content))
        except self.s3_client.exceptions.NoSuchKey:
            # File not found - this is expected when trying patterns
            return None
        except Exception as e:
            print(f"Error loading {s3_key}: {e}")
            return None
    
    def load_lap_times(self, track_name: str, session: str, file_type: str = "lap_start") -> Optional[pd.DataFrame]:
        """Load lap times from S3 with pattern matching.
        
        Tries multiple naming patterns to handle variations in file naming.
        
        Args:
            track_name: Name of the track
            session: Session name (e.g., 'R1', 'R2')
            file_type: Type of file to load ('lap_start' or 'lap_end')
            
        Returns:
            DataFrame with lap times if found, None otherwise
        """
        track_base = track_name.split("_")[0]
        track_upper = track_name.upper()
        
        # Map file_type to various naming conventions
        file_type_variants = {
            "lap_start": ["lap_start", "lap_start_time"],
            "lap_end": ["lap_end", "lap_end_time"]
        }
        
        variants = file_type_variants.get(file_type, [file_type])
        
        # Try different naming patterns for each variant
        patterns = []
        for variant in variants:
            patterns.extend([
                # Standard patterns
                f"{session}_{track_base}_{variant}.csv",  # R1_barber_lap_start.csv
                f"{session}_{track_name}_{variant}.csv",  # R1_indianapolis_lap_start.csv
                f"{session}_{track_name.replace('_', '-')}_{variant}.csv",  # R1_road-america_lap_start.csv
                
                # Full track name patterns
                f"{session}_indianapolis_motor_speedway_{variant}.csv",
                f"{session}_circuit_of_the_americas_{variant}.csv",
                f"{session}_virginia_international_raceway_{variant}.csv",
                
                # COTA special pattern (reversed order)
                f"{track_upper}_{variant}_{session}.csv",  # COTA_lap_start_time_R1.csv
                f"{track_base.upper()}_{variant}_{session}.csv",  # COTA_lap_start_R1.csv
                
                # Generic patterns
                f"{session}_{variant}.csv",  # R1_lap_start.csv
            ])
        
        for pattern in patterns:
            # Try all possible S3 key locations
            possible_keys = self._get_s3_key(track_name, pattern)
            for s3_key in possible_keys:
                df = self._download_csv_from_s3(s3_key)
                if df is not None:
                    return df
        
        # Only print warning for lap_start files (lap_end is optional)
        if file_type == "lap_start":
            print(f"Warning: Could not find lap times for {track_name}/{session}")
        return None
    
    def load_telemetry(self, track_name: str, session: str) -> Optional[pd.DataFrame]:
        """Load telemetry data from S3 with pattern matching.
        
        Tries multiple naming patterns to handle variations in file naming.
        
        Args:
            track_name: Name of the track
            session: Session name (e.g., 'practice', 'qualifying', 'race')
            
        Returns:
            DataFrame with telemetry data if found, None otherwise
        """
        patterns = [
            f"{session}_{track_name}_telemetry_data.csv",
            f"{session}_{track_name.replace('_', '-')}_telemetry_data.csv",
            f"{session}_telemetry_data.csv"
        ]
        
        for pattern in patterns:
            s3_key = self._get_s3_key(track_name, pattern)
            df = self._download_csv_from_s3(s3_key)
            if df is not None:
                return df
        
        print(f"Warning: Could not find telemetry for {track_name}/{session}")
        return None
    
    def get_available_tracks(self) -> list:
        """Get list of available tracks from S3.
        
        Returns:
            List of track names (subdirectories under 'data/')
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix='data/',
                Delimiter='/'
            )
            
            tracks = []
            for prefix in response.get('CommonPrefixes', []):
                track_name = prefix['Prefix'].replace('data/', '').rstrip('/')
                tracks.append(track_name)
            
            return tracks
        except Exception as e:
            print(f"Error listing tracks: {e}")
            return []
    
    def get_available_sessions(self, track_name: str) -> list:
        """Get available sessions for a track.
        
        Args:
            track_name: Name of the track
            
        Returns:
            List of session names extracted from filenames
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=f'data/{track_name}/'
            )
            
            sessions = set()
            for obj in response.get('Contents', []):
                filename = obj['Key'].split('/')[-1]
                # Skip directory markers and non-CSV files
                if not filename or filename == '.' or not filename.endswith('.csv'):
                    continue
                    
                if '_lap_start.csv' in filename or 'lap_start_time' in filename:
                    session = filename.split('_')[0]
                    # Only add valid session names (R1, R2, etc.)
                    if session and session.startswith('R') and len(session) == 2:
                        sessions.add(session)
                    # Handle COTA pattern: COTA_lap_start_time_R1.csv
                    elif '_R' in filename:
                        parts = filename.split('_R')
                        if len(parts) > 1:
                            session_num = parts[1].split('.')[0]
                            sessions.add(f'R{session_num}')
            
            return sorted(list(sessions))
        except Exception as e:
            print(f"Error listing sessions: {e}")
            return []
