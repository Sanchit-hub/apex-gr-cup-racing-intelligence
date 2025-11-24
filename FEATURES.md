# Feature Documentation

## Core Analytics Features

### 1. Lap Time & Sector Analysis

#### Theoretical Best Lap
- Combines best sector times from all drivers
- Calculates the theoretical fastest possible lap
- Shows which driver achieved each best sector

#### Real-Time Delta
- Compares current lap to theoretical best
- Shows time gained/lost per sector
- Color-coded heatmap (green = faster, red = slower)

#### Sector Breakdown
- Analyzes performance in each track section
- Identifies consistent weak points
- Tracks improvement over session

**API Endpoint**: `GET /api/analytics/track/{track}/session/{session}/best-lap`

**Use Case**: Driver sees they're losing 0.3s in sector 2 every lap → Focus practice on that section

---

### 2. Braking & Acceleration Intelligence

#### Optimal Braking Point Detection
- Identifies where drivers brake for each corner
- Compares to fastest lap braking points
- Detects late/early braking patterns

#### Braking Efficiency
- Measures brake pressure application
- Calculates braking efficiency score
- Identifies over-braking or under-braking

#### Speed Analysis (vMin/vMax)
- **vMax**: Maximum speed on straights
- **vMin**: Minimum speed in corners (corner entry speed)
- Acceleration profile analysis

**API Endpoints**: 
- `GET /api/telemetry/.../braking-analysis`
- `GET /api/telemetry/.../speed-analysis`

**Use Case**: Driver braking 50m too early in Turn 1 → Gain 0.2s per lap by braking later

---

### 3. Racing Line Evaluation

#### Line Deviation Tracking
- Compares driver's line to optimal racing line
- Measures lateral deviation in corners
- Identifies line consistency issues

#### Corner-by-Corner Analysis
- Entry speed, apex speed, exit speed
- Racing line through each corner
- Comparison to fastest drivers

**Use Case**: Driver taking wider line in Turn 5 → Tighter line could improve exit speed

---

### 4. Tire Degradation Modeling

#### Lap-by-Lap Performance
- Tracks lap time degradation over stint
- Calculates degradation rate (seconds per lap)
- Predicts remaining tire life

#### Wear Rate Analysis
- Correlates driving style with tire wear
- Aggressive vs smooth driving impact
- Temperature and pressure effects

#### Pit Window Recommendations
- Calculates optimal pit stop lap
- Compares pit loss vs tire degradation
- Alternative strategy simulations

**API Endpoints**:
- `GET /api/strategy/.../tire-degradation`
- `POST /api/strategy/.../pit-strategy`

**Use Case**: Tires degrading at 0.15s/lap → Optimal pit window is laps 18-22

---

### 5. Real-Time Strategy Engine

#### Pit Stop Calculator
- Calculates time lost in pit stop
- Compares to track position changes
- Simulates alternative strategies

#### Race Simulation
- Predicts race outcome with different strategies
- Accounts for tire degradation
- Fuel consumption modeling

#### Performance Alerts
- **Overheating**: Engine/brake temps too high
- **Pace Drop**: Lap times falling off
- **Consistency Issues**: High lap time variation
- **Tire Cliff**: Sudden performance drop

**API Endpoint**: `POST /api/strategy/.../pit-strategy`

**Request Body**:
```json
{
  "current_lap": 15,
  "total_laps": 30,
  "tire_age": 15,
  "fuel_level": 50.0
}
```

**Use Case**: System alerts engineer that driver should pit on lap 19 instead of 22 to avoid tire cliff

---

### 6. Driver Consistency Metrics

#### Consistency Score
- Percentage of laps within 0.5s of best lap
- Lower coefficient of variation = more consistent
- Elite drivers: 95%+ consistency

#### Lap Time Distribution
- Standard deviation of lap times
- Identifies outlier laps
- Tracks improvement over time

#### Sector Consistency
- Consistency in each track section
- Identifies inconsistent corners
- Helps focus practice sessions

**API Endpoint**: `GET /api/strategy/.../consistency`

**Response**:
```json
{
  "consistency_score": 94.2,
  "coefficient_of_variation": 1.8,
  "laps_within_05s": 28,
  "total_laps": 30
}
```

**Use Case**: Driver has 94% consistency → Top 10% of field, ready for race

---

## Dashboard Features

### Track & Session Selector
- Dropdown for all 7 tracks
- Session selector (R1, R2, etc.)
- Automatic data loading

### Best Lap Card
- Displays fastest lap of session
- Shows driver ID and lap number
- Formatted time display (MM:SS.mmm)

### Driver Performance Panel
- Input field for driver ID
- Real-time performance metrics
- Lap time progression chart

### Analytics Overview
- Summary of available features
- Quick access to different analysis types
- Visual indicators for data availability

---

## API Architecture

### Analytics Router (`/api/analytics`)
- Track and session management
- Lap time analysis
- Sector performance
- Driver comparisons

### Telemetry Router (`/api/telemetry`)
- Raw telemetry data access
- Braking analysis
- Speed profiling
- Acceleration metrics

### Strategy Router (`/api/strategy`)
- Pit stop optimization
- Tire degradation prediction
- Consistency analysis
- Race simulation

---

## Data Processing Pipeline

1. **Data Extraction**: ZIP files → CSV files
2. **Data Loading**: CSV → Pandas DataFrames
3. **Data Cleaning**: Remove invalid laps, outliers
4. **Analysis**: Statistical calculations, ML predictions
5. **API Response**: JSON formatted results
6. **Visualization**: React components render charts

---

## Performance Optimizations

- **Lazy Loading**: Only load data when requested
- **Caching**: Cache frequently accessed data
- **Sampling**: Limit telemetry to 100k rows for speed
- **Indexing**: Fast lookups by driver/lap/session
- **Async Processing**: Non-blocking API calls

---

## Future Feature Roadmap

### Phase 2 (ML Models)
- LSTM lap time prediction
- Reinforcement learning racing lines
- Anomaly detection for mechanical issues

### Phase 3 (Advanced Analytics)
- Weather impact analysis
- Multi-car race simulation
- Predictive maintenance
- Driver comparison heatmaps

### Phase 4 (Real-Time)
- Live race data streaming
- WebSocket connections
- Mobile app companion
- Team radio integration

---

## Research References

1. **Lap Time Prediction**: ML models with 97% accuracy using speed, acceleration, steering
2. **Racing Line Optimization**: Bayesian optimization and RL for optimal lines
3. **Tire Degradation**: Linear and polynomial models for wear prediction
4. **Consistency Metrics**: Coefficient of variation, sector-by-sector analysis
5. **Real-Time Telemetry**: FSAE/F1 architectures with millisecond latency
