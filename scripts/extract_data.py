"""Extract all race data from ZIP files."""
import zipfile
import os
from pathlib import Path

TRACKS = [
    "barber-motorsports-park",
    "circuit-of-the-americas",
    "indianapolis",
    "road-america",
    "sebring",
    "sonoma",
    "virginia-international-raceway"
]

def extract_all_data():
    """Extract all track data from ZIP files."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    for track in TRACKS:
        zip_path = Path(f"{track}.zip")
        if not zip_path.exists():
            print(f"⚠️  {track}.zip not found, skipping...")
            continue
            
        track_dir = data_dir / track.replace("-", "_")
        track_dir.mkdir(exist_ok=True)
        
        print(f"📦 Extracting {track}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(track_dir)
        
        print(f"✅ Extracted to {track_dir}")
    
    print("\n🏁 All data extracted successfully!")

if __name__ == "__main__":
    extract_all_data()
