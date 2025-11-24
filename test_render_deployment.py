"""Test Render deployment with S3 integration."""
import requests
import json

BACKEND_URL = "https://apex-backend-7orz.onrender.com"

def test_endpoint(endpoint, description):
    """Test an API endpoint."""
    url = f"{BACKEND_URL}{endpoint}"
    print(f"\n🔍 Testing: {description}")
    print(f"   URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {json.dumps(data, indent=2)[:200]}")
            return True, data
        else:
            print(f"   ❌ Failed: {response.text[:200]}")
            return False, None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False, None

def main():
    """Run deployment tests."""
    print("="*60)
    print("🚀 APEX Render Deployment Test")
    print("="*60)
    
    # Test 1: Health check
    test_endpoint("/health", "Health Check")
    
    # Test 2: List tracks
    success, tracks = test_endpoint("/api/analytics/tracks", "List Tracks")
    
    if success and tracks:
        print(f"\n📊 Found {len(tracks)} tracks")
        
        # Test 3: Get sessions for first track
        if len(tracks) > 0:
            track = tracks[0]
            test_endpoint(f"/api/analytics/track/{track}/sessions", f"Sessions for {track}")
            
            # Test 4: Get best lap
            success, sessions = test_endpoint(f"/api/analytics/track/{track}/sessions", f"Sessions for {track}")
            if success and sessions and len(sessions) > 0:
                session = sessions[0]
                if session != ".":  # Skip "." directory
                    test_endpoint(f"/api/analytics/track/{track}/session/{session}/best-lap", f"Best lap for {track}/{session}")
    
    print("\n" + "="*60)
    print("✅ Test Complete")
    print("="*60)

if __name__ == "__main__":
    main()
