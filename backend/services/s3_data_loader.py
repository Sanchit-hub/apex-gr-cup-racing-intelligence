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
        
    def _get_s3_key(self, track_name: str, filename: str) -> str:
        """Generate S3 key for a file.
        
        Args:
            track_name: Name of the track (e.g., 'barber_motorsports_park')
            filename: Name of the file (e.g., 'practice_lap_start.csv')
            
        Returns:
            S3 key in format 'data/{track_name}/{filename}'
        """
        return f"data/{track_name}/{filename}"
    
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
    
    def load_lap_times(self, track_name: str, session: str) -> Optional[pd.DataFrame]:
        """Load lap times from S3 with pattern matching.
        
        Tries multiple naming patterns to handle variations in file naming.
        
        Args:
            track_name: Name of the track
            session: Session name (e.g., 'practice', 'qualifying', 'race')
            
        Returns:
            DataFrame with lap times if found, None otherwise
        """
        # Try different naming patterns
        patterns = [
            f"{session}_{track_name}_lap_start.csv",
            f"{session}_{track_name.replace('_', '-')}_lap_start.csv",
            f"{session}_lap_start.csv"
        ]
        
        for pattern in patterns:
            s3_key = self._get_s3_key(track_name, pattern)
            df = self._download_csv_from_s3(s3_key)
            if df is not None:
                return df
        
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
                if '_lap_start.csv' in filename:
                    session = filename.split('_')[0]
                    sessions.add(session)
            
            return list(sessions)
        except Exception as e:
            print(f"Error listing sessions: {e}")
            return []
