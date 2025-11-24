"""Create sampled data for deployment."""
import pandas as pd
from pathlib import Path
import shutil

def sample_telemetry(input_file, output_file, sample_rate=10):
    """Sample telemetry data to reduce size."""
    print(f"📊 Sampling {input_file.name}...")
    
    # Read and sample every Nth row
    df = pd.read_csv(input_file)
    original_size = len(df)
    
    # Keep every Nth row
    sampled_df = df.iloc[::sample_rate]
    
    # Save sampled data
    sampled_df.to_csv(output_file, index=False)
    
    new_size = len(sampled_df)
    reduction = (1 - new_size/original_size) * 100
    
    print(f"✅ Reduced from {original_size:,} to {new_size:,} rows ({reduction:.1f}% reduction)")
    return output_file.stat().st_size

def prepare_sampled_data():
    """Prepare sampled data for deployment."""
    
    deploy_data = Path("data_sampled")
    deploy_data.mkdir(exist_ok=True)
    
    # Just use one track for demo
    track = "barber_motorsports_park"
    track_src = Path("data") / track
    
    if not track_src.exists():
        print(f"❌ {track} not found!")
        return
    
    # Find actual data directory
    for subdir in track_src.iterdir():
        if subdir.is_dir() and not subdir.name.startswith("__"):
            track_data = subdir
            break
    
    # Create destination
    track_dest = deploy_data / track / track_data.name
    track_dest.mkdir(parents=True, exist_ok=True)
    
    total_size = 0
    
    # Copy lap files (small)
    for pattern in ["*_lap_start.csv", "*_lap_end.csv"]:
        for file in track_data.glob(pattern):
            dest = track_dest / file.name
            shutil.copy2(file, dest)
            size = dest.stat().st_size
            total_size += size
            print(f"✅ Copied {file.name} ({size/1024/1024:.2f} MB)")
    
    # Sample telemetry files (huge)
    for file in track_data.glob("*_telemetry_data.csv"):
        dest = track_dest / file.name
        size = sample_telemetry(file, dest, sample_rate=100)  # Keep 1% of data
        total_size += size
        print(f"✅ Sampled {file.name} ({size/1024/1024:.2f} MB)")
    
    print(f"\n📊 Total size: {total_size/1024/1024:.2f} MB")
    print(f"📁 Sampled data ready in: {deploy_data}")

if __name__ == "__main__":
    prepare_sampled_data()
