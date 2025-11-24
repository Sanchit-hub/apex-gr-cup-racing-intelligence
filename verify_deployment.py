"""Verify APEX deployment with S3 data."""
import requests
import sys

# Configuration
BACKEND_URL = "https://apex-backend-7orz.onrender.com"
EXPECTED_TRACKS = [
    "barber_motorsports_park",
    "COTA",
    "indianapolis", 
    "road-america",
    "sebring",
    "Sonoma",
    "virginia-international-raceway"
]

def test_health():
    """Test health endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_tracks():
    """Test tracks endpoint."""
    print("\n🔍 Testing tracks endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/analytics/tracks", timeout=10)
        if response.status_code == 200:
            tracks = response.json()
            print(f"✅ Tracks endpoint returned {len(tracks)} tracks")
            
            # Check if all expected tracks are present
            missing = []
            for track in EXPECTED_TRACKS:
                if track not in tracks:
                    missing.append(track)
            
            if missing:
                print(f"⚠️  Missing tracks: {missing}")
                return False
            else:
                print("✅ All 7 tracks present")
                return True
        else:
            print(f"❌ Tracks endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Tracks endpoint error: {e}")
        return False

def test_track_sessions(track_name):
    """Test sessions for a specific track."""
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/analytics/track/{track_name}/sessions",
            timeout=10
        )
        if response.status_code == 200:
            sessions = response.json()
            print(f"  ✅ {track_name}: {len(sessions)} sessions")
            return True
        else:
            print(f"  ❌ {track_name}: Failed ({response.status_code})")
            return False
    except Exception as e:
        print(f"  ❌ {track_name}: Error - {e}")
        return False

def test_all_tracks():
    """Test all tracks."""
    print("\n🔍 Testing individual tracks...")
    results = []
    for track in EXPECTED_TRACKS:
        result = test_track_sessions(track)
        results.append(result)
    
    success_count = sum(results)
    print(f"\n📊 Track Results: {success_count}/{len(EXPECTED_TRACKS)} successful")
    return all(results)

def test_best_lap(track_name, session):
    """Test best lap endpoint."""
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/analytics/track/{track_name}/session/{session}/best-lap",
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            if "best_lap_time" in data or "error" not in data:
                return True
        return False
    except:
        return False

def main():
    """Run all verification tests."""
    print("=" * 60)
    print("🏁 APEX Deployment Verification")
    print("=" * 60)
    
    results = []
    
    # Test 1: Health
    results.append(test_health())
    
    # Test 2: Tracks list
    results.append(test_tracks())
    
    # Test 3: Individual tracks
    results.append(test_all_tracks())
    
    # Test 4: Sample best lap query
    print("\n🔍 Testing sample data query...")
    if test_best_lap("barber_motorsports_park", "R1"):
        print("✅ Best lap query successful")
        results.append(True)
    else:
        print("❌ Best lap query failed")
        results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Verification Summary")
    print("=" * 60)
    success_count = sum(results)
    total_tests = len(results)
    
    if all(results):
        print(f"✅ All tests passed ({success_count}/{total_tests})")
        print("\n🎉 Deployment successful! APEX is ready for production!")
        return 0
    else:
        print(f"⚠️  Some tests failed ({success_count}/{total_tests})")
        print("\n❌ Deployment needs attention. Check Render logs and S3 bucket.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
