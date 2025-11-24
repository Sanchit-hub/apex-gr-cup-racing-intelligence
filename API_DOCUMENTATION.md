# API Documentation

## Base URL

**Development**: `http://localhost:8000`
**Production**: `https://your-backend.railway.app`

## Interactive Documentation

FastAPI provides automatic interactive API documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Authentication

Currently no authentication required (hackathon prototype).

## Response Format

### Success Response
```json
{
  "data": {...},
  "status": "success"
}
```

### Error Response
```json
{
  "error": "Error message",
  "status": "error"
}
```

## Endpoints

### Health Check

#### GET /health
Check if the API is running.

**Response**:
```json
{
  "status": "healthy"
}
```

---

## Analytics Endpoints

### GET /api/analytics/tracks

Get list of all available tracks.

**Response**:
```json
[
  "barber_motorsports_park",
  "circuit_of_the_americas",
  "indianapolis",
  "road_america",
  "sebring",
  "sonoma",
  "virginia_international_raceway"
]
```

**Example**:
```bash
curl http://localhost:8000/api/analytics/tracks
```

---

### GET /api/analytics/track/{track_name}/sessions

Get available sessions for a specific track.

**Parameters**:
- `track_name` (path): Track identifier (e.g., "barber_motorsports_park")

**Response**:
```json
["R1", "R2"]
```

**Example**:
```bash
curl http://localhost:8000/api/analytics/track/barber_motorsports_park/sessions
```

---

### GET /api/analytics/track/{track_name}/session/{session}/best-lap

Get the fastest lap time for a session.

**Parameters**:
- `track_name` (path): Track identifier
- `session` (path): Session identifier (e.g., "R1")

**Response**:
```json
{
  "best_lap_time": 129.456,
  "driver_id": "GR86-015-000",
  "lap_number": 12,
  "track": "barber_motorsports_park",
  "session": "R1"
}
```

**Example**:
```bash
curl http://localhost:8000/api/analytics/track/barber_motorsports_park/session/R1/best-lap
```

---

### GET /api/analytics/track/{track_name}/session/{session}/driver/{driver_id}/performance

Get comprehensive performance analysis for a driver.

**Parameters**:
- `track_name` (path): Track identifier
- `session` (path): Session identifier
- `driver_id` (path): Driver identifier (e.g., "GR86-015-000")

**Response**:
```json
{
  "driver_id": "GR86-015-000",
  "best_lap": 129.456,
  "average_lap": 130.234,
  "std_deviation": 0.523,
  "consistency_score": 94.2,
  "total_laps": 30,
  "lap_times": [129.456, 130.123, 129.987, ...]
}
```

**Example**:
```bash
curl http://localhost:8000/api/analytics/track/barber_motorsports_park/session/R1/driver/GR86-015-000/performance
```

---

### GET /api/analytics/track/{track_name}/session/{session}/sector-analysis

Get sector-by-sector analysis for all drivers.

**Parameters**:
- `track_name` (path): Track identifier
- `session` (path): Session identifier

**Response**:
```json
{
  "sector_analysis": {
    "GR86-015-000": {
      "avg_sector_time": 43.2,
      "best_sector": 42.8
    },
    "GR86-020-000": {
      "avg_sector_time": 43.5,
      "best_sector": 43.1
    }
  }
}
```

**Example**:
```bash
curl http://localhost:8000/api/analytics/track/barber_motorsports_park/session/R1/sector-analysis
```

---

## Telemetry Endpoints

### GET /api/telemetry/track/{track_name}/session/{session}/driver/{driver_id}/lap/{lap_number}

Get detailed telemetry data for a specific lap.

**Parameters**:
- `track_name` (path): Track identifier
- `session` (path): Session identifier
- `driver_id` (path): Driver identifier
- `lap_number` (path): Lap number (integer)

**Response**:
```json
{
  "lap_number": 12,
  "driver_id": "GR86-015-000",
  "speed": {
    "max": 185.3,
    "avg": 142.7,
    "min": 65.2
  },
  "throttle_avg": 78.5,
  "data_points": 1523
}
```

**Example**:
```bash
curl http://localhost:8000/api/telemetry/track/barber_motorsports_park/session/R1/driver/GR86-015-000/lap/12
```

---

### GET /api/telemetry/track/{track_name}/session/{session}/driver/{driver_id}/braking-analysis

Analyze braking performance for a driver.

**Parameters**:
- `track_name` (path): Track identifier
- `session` (path): Session identifier
- `driver_id` (path): Driver identifier

**Response**:
```json
{
  "driver_id": "GR86-015-000",
  "brake_applications": 156,
  "avg_brake_pressure": 65.3,
  "max_brake_pressure": 98.7,
  "braking_efficiency": 66.1
}
```

**Example**:
```bash
curl http://localhost:8000/api/telemetry/track/barber_motorsports_park/session/R1/driver/GR86-015-000/braking-analysis
```

---

### GET /api/telemetry/track/{track_name}/session/{session}/driver/{driver_id}/speed-analysis

Analyze speed profile (vMin, vMax, acceleration).

**Parameters**:
- `track_name` (path): Track identifier
- `session` (path): Session identifier
- `driver_id` (path): Driver identifier

**Response**:
```json
{
  "driver_id": "GR86-015-000",
  "vmax": 185.3,
  "vmin": 65.2,
  "vavg": 142.7,
  "speed_range": 120.1,
  "avg_acceleration": 0.45
}
```

**Example**:
```bash
curl http://localhost:8000/api/telemetry/track/barber_motorsports_park/session/R1/driver/GR86-015-000/speed-analysis
```

---

## Strategy Endpoints

### POST /api/strategy/track/{track_name}/session/{session}/driver/{driver_id}/pit-strategy

Calculate optimal pit stop strategy.

**Parameters**:
- `track_name` (path): Track identifier
- `session` (path): Session identifier
- `driver_id` (path): Driver identifier

**Request Body**:
```json
{
  "current_lap": 15,
  "total_laps": 30,
  "tire_age": 15,
  "fuel_level": 50.0
}
```

**Response**:
```json
{
  "current_lap": 15,
  "total_laps": 30,
  "tire_age": 15,
  "optimal_pit_lap": 19,
  "projected_time_loss_no_pit": 2.25,
  "pit_stop_time_loss": 25.0,
  "recommendation": "Stay out",
  "avg_lap_time": 130.234
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/api/strategy/track/barber_motorsports_park/session/R1/driver/GR86-015-000/pit-strategy \
  -H "Content-Type: application/json" \
  -d '{"current_lap": 15, "total_laps": 30, "tire_age": 15, "fuel_level": 50.0}'
```

---

### GET /api/strategy/track/{track_name}/session/{session}/driver/{driver_id}/tire-degradation

Predict tire degradation over race distance.

**Parameters**:
- `track_name` (path): Track identifier
- `session` (path): Session identifier
- `driver_id` (path): Driver identifier

**Response**:
```json
{
  "driver_id": "GR86-015-000",
  "degradation_rate_per_lap": 0.15,
  "best_lap": 129.456,
  "current_delta": 1.23,
  "laps_analyzed": 30,
  "lap_deltas": [
    {"lap": 1, "delta": 0.0},
    {"lap": 2, "delta": 0.12},
    {"lap": 3, "delta": 0.18},
    ...
  ]
}
```

**Example**:
```bash
curl http://localhost:8000/api/strategy/track/barber_motorsports_park/session/R1/driver/GR86-015-000/tire-degradation
```

---

### GET /api/strategy/track/{track_name}/session/{session}/driver/{driver_id}/consistency

Calculate driver consistency metrics.

**Parameters**:
- `track_name` (path): Track identifier
- `session` (path): Session identifier
- `driver_id` (path): Driver identifier

**Response**:
```json
{
  "driver_id": "GR86-015-000",
  "consistency_score": 94.2,
  "coefficient_of_variation": 1.8,
  "best_lap": 129.456,
  "average_lap": 130.234,
  "std_deviation": 0.523,
  "laps_within_05s": 28,
  "total_laps": 30
}
```

**Example**:
```bash
curl http://localhost:8000/api/strategy/track/barber_motorsports_park/session/R1/driver/GR86-015-000/consistency
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 404 | Resource not found (track, session, or driver) |
| 422 | Validation error (invalid parameters) |
| 500 | Internal server error |

## Rate Limiting

Currently no rate limiting (hackathon prototype).

For production, recommended limits:
- 100 requests per minute per IP
- 1000 requests per hour per IP

## Data Types

### Track Names
- `barber_motorsports_park`
- `circuit_of_the_americas`
- `indianapolis`
- `road_america`
- `sebring`
- `sonoma`
- `virginia_international_raceway`

### Session Identifiers
- `R1` - Race 1
- `R2` - Race 2

### Driver IDs
Format: `GR86-XXX-000` (e.g., `GR86-015-000`)

## Usage Examples

### Python

```python
import requests

# Get best lap
response = requests.get(
    "http://localhost:8000/api/analytics/track/barber_motorsports_park/session/R1/best-lap"
)
data = response.json()
print(f"Best lap: {data['best_lap_time']}s by {data['driver_id']}")

# Get driver performance
response = requests.get(
    "http://localhost:8000/api/analytics/track/barber_motorsports_park/session/R1/driver/GR86-015-000/performance"
)
performance = response.json()
print(f"Consistency: {performance['consistency_score']}%")

# Calculate pit strategy
response = requests.post(
    "http://localhost:8000/api/strategy/track/barber_motorsports_park/session/R1/driver/GR86-015-000/pit-strategy",
    json={
        "current_lap": 15,
        "total_laps": 30,
        "tire_age": 15,
        "fuel_level": 50.0
    }
)
strategy = response.json()
print(f"Recommendation: {strategy['recommendation']}")
```

### JavaScript

```javascript
// Get best lap
const response = await fetch(
  'http://localhost:8000/api/analytics/track/barber_motorsports_park/session/R1/best-lap'
);
const data = await response.json();
console.log(`Best lap: ${data.best_lap_time}s by ${data.driver_id}`);

// Get driver performance
const perfResponse = await fetch(
  'http://localhost:8000/api/analytics/track/barber_motorsports_park/session/R1/driver/GR86-015-000/performance'
);
const performance = await perfResponse.json();
console.log(`Consistency: ${performance.consistency_score}%`);

// Calculate pit strategy
const strategyResponse = await fetch(
  'http://localhost:8000/api/strategy/track/barber_motorsports_park/session/R1/driver/GR86-015-000/pit-strategy',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      current_lap: 15,
      total_laps: 30,
      tire_age: 15,
      fuel_level: 50.0
    })
  }
);
const strategy = await strategyResponse.json();
console.log(`Recommendation: ${strategy.recommendation}`);
```

### cURL

```bash
# Get all tracks
curl http://localhost:8000/api/analytics/tracks

# Get best lap
curl http://localhost:8000/api/analytics/track/barber_motorsports_park/session/R1/best-lap

# Get driver performance
curl http://localhost:8000/api/analytics/track/barber_motorsports_park/session/R1/driver/GR86-015-000/performance

# Calculate pit strategy
curl -X POST http://localhost:8000/api/strategy/track/barber_motorsports_park/session/R1/driver/GR86-015-000/pit-strategy \
  -H "Content-Type: application/json" \
  -d '{"current_lap": 15, "total_laps": 30, "tire_age": 15, "fuel_level": 50.0}'
```

## Postman Collection

Import this collection to test all endpoints:

```json
{
  "info": {
    "name": "GR Cup Racing Intelligence API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Get Tracks",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/api/analytics/tracks"
      }
    },
    {
      "name": "Get Best Lap",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/api/analytics/track/barber_motorsports_park/session/R1/best-lap"
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000"
    }
  ]
}
```

## WebSocket Support (Future)

For real-time updates, WebSocket support planned:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/live-telemetry');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Live telemetry:', data);
};
```

## Versioning

Current version: `v1.0.0`

Future versions will use URL versioning:
- `/api/v1/analytics/...`
- `/api/v2/analytics/...`

## Support

For API issues:
- Check interactive docs at `/docs`
- Review this documentation
- Check backend logs
- Open GitHub issue

---

**Last Updated**: November 2025
**API Version**: 1.0.0
**Status**: Production Ready
