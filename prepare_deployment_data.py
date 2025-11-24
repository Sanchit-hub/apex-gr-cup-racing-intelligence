"""Prepare minimal data for deployment."""
import os
import shutil
from pathlib import Path

def prepare_deployment_data():
    """Copy only essential CSV files for deployment."""
    
    # Create deployment data directory
    deploy_data = Path("deploy_data")
    deploy_data.mkdir(exist_ok=True)
    
    # Tracks to include
    tracks = [
        "barber_motorsports_park",
        "circuit_of_the_americas",
        "indianapolis"
    ]
    
    # Essential file patterns
    essential_patterns = [
        "*_lap_start.csv",
        "*_lap_end.csv",
        "*_telemetry_data.csv"
    ]
    
    total_size = 0
    
    for track in tracks:
        track_src = Path("data") / track
        if not track_src.exists():
            print(f"⚠️  {track} not found, skipping...")
            continue
        
        # Find the actual data directory
        for subdir in track_src.iterdir():
            if subdir.is_dir() and not subdir.name.startswith("__"):
                track_data = subdir
                break
        else:
            continue
        
        # Create track directory in deployment data
        track_dest = deploy_data / track / track_data.name
        track_dest.mkdir(parents=True, exist_ok=True)
        
        # Copy essential files
        for pattern in essential_patterns:
            for file in track_data.glob(pattern):
                dest_file = track_dest / file.name
                shutil.copy2(file, dest_file)
                size = dest_file.stat().st_size
                total_size += size
                print(f"✅ Copied {file.name} ({size / 1024 / 1024:.2f} MB)")
    
    print(f"\n📊 Total size: {total_size / 1024 / 1024:.2f} MB")
    print(f"📁 Deployment data ready in: {deploy_data}")

if __name__ == "__main__":
    prepare_deployment_data()
