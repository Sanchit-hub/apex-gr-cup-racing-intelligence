# System Architecture

## Overview

The GR Cup Racing Intelligence System is a full-stack web application that processes motorsports telemetry data and provides real-time analytics through a REST API and interactive dashboard.

## High-Level Architecture

```
┌─────────────────┐
│   ZIP Files     │
│  (7 Tracks)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Extraction │
│   (Python)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CSV Files      │
│  (data/)        │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│         Backend (FastAPI)           │
│  ┌─────────────────────────────┐   │
│  │  Routers (API Endpoints)    │   │
│  │  - Analytics                │   │
│  │  - Telemetry                │   │
│  │  - Strategy                 │   │
│  └──────────┬──────────────────┘   │
│             │                       │
│  ┌──────────▼──────────────────┐   │
│  │  Services (Business Logic)  │   │
│  │  - LapAnalyzer              │   │
│  │  - TelemetryAnalyzer        │   │
│  │  - StrategyEngine           │   │
│  └──────────┬──────────────────┘   │
│             │                       │
│  ┌──────────▼──────────────────┐   │
│  │  Data Layer (Pandas)        │   │
│  │  - CSV Loading              │   │
│  │  - Data Processing          │   │
│  │  - Statistical Analysis     │   │
│  └─────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │ REST API (JSON)
               │
┌──────────────▼──────────────────────┐
│      Frontend (React + Vite)        │
│  ┌─────────────────────────────┐   │
│  │  Components                 │   │
│  │  - Dashboard                │   │
│  │  - TrackSelector            │   │
│  │  - DriverPerformance        │   │
│  │  - BestLapCard              │   │
│  └──────────┬──────────────────┘   │
│             │                       │
│  ┌──────────▼──────────────────┐   │
│  │  API Client (Axios)         │   │
│  └──────────┬──────────────────┘   │
│             │                       │
│  ┌──────────▼──────────────────┐   │
│  │  Visualization (Recharts)   │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

## Backend Architecture

### Layer 1: API Routers

**Purpose**: Handle HTTP requests and responses

**Files**:
- `backend/routers/analytics.py`
- `backend/routers/telemetry.py`
- `backend/routers/strategy.py`

**Responsibilities**:
- Route definition and URL mapping
- Request validation (Pydantic models)
- Response formatting
- Error handling
- HTTP status codes

**Example**:
```python
@router.get("/track/{track_name}/session/{session}/best-lap")
async def get_best_lap(track_name: str, session: str):
    return analyzer.calculate_best_lap(track_name, session)
```

### Layer 2: Service Layer

**Purpose**: Business logic and data processing

**Files**:
- `backend/services/lap_analyzer.py`
- `backend/services/telemetry_analyzer.py`
- `backend/services/strategy_engine.py`

**Responsibilities**:
- Data loading from CSV files
- Statistical calculations
- Algorithm implementation
- Business rule enforcement
- Data transformation

**Key Classes**:

#### LapAnalyzer
- `get_available_tracks()`: List all tracks
- `calculate_best_lap()`: Find fastest lap
- `analyze_driver_performance()`: Driver metrics
- `analyze_sectors()`: Sector-by-sector analysis

#### TelemetryAnalyzer
- `get_lap_data()`: Detailed lap telemetry
- `analyze_braking()`: Braking metrics
- `analyze_speed()`: Speed profile (vMin/vMax)

#### StrategyEngine
- `calculate_pit_window()`: Optimal pit timing
- `predict_tire_degradation()`: Tire wear model
- `analyze_consistency()`: Consistency metrics

### Layer 3: Data Layer

**Purpose**: Data access and manipulation

**Technology**: Pandas DataFrames

**Operations**:
- CSV file loading
- Data filtering and grouping
- Statistical aggregations
- Time series analysis
- Missing data handling

**Example**:
```python
def _load_lap_times(self, track_name: str, session: str):
    lap_file = self.data_dir / track_name / f"{session}_lap_time.csv"
    return pd.read_csv(lap_file)
```

## Frontend Architecture

### Component Hierarchy

```
App
├── TrackSelector
│   ├── Track Dropdown
│   └── Session Dropdown
└── Dashboard
    ├── BestLapCard
    └── DriverPerformance
        ├── Performance Metrics
        └── Lap Time Chart (Recharts)
```

### State Management

**Technology**: React useState + useEffect hooks

**State Flow**:
1. User selects track → `setSelectedTrack()`
2. Load sessions for track → `setSessions()`
3. User selects session → `setSelectedSession()`
4. Load analytics data → `setBestLap()`, `setPerformance()`
5. Render visualizations

### API Communication

**Technology**: Axios

**Pattern**: Async/await with error handling

**Example**:
```typescript
const loadBestLap = async () => {
  try {
    const response = await axios.get(`/api/analytics/track/${track}/session/${session}/best-lap`)
    setBestLap(response.data)
  } catch (error) {
    console.error('Failed to load best lap:', error)
  }
}
```

### Visualization

**Technology**: Recharts

**Charts**:
- Line Chart: Lap time progression
- Bar Chart: Sector comparison (future)
- Scatter Plot: Speed vs time (future)

## Data Flow

### 1. Data Extraction Flow

```
ZIP Files → extract_data.py → CSV Files → data/ directory
```

**Process**:
1. Script reads ZIP files from root directory
2. Extracts to `data/{track_name}/`
3. Organizes by track and session

### 2. API Request Flow

```
User Action → Frontend → HTTP Request → Backend Router → Service → Data Layer → Response
```

**Example: Get Best Lap**
1. User selects track "barber" and session "R1"
2. Frontend calls `GET /api/analytics/track/barber/session/R1/best-lap`
3. Router receives request, calls `analyzer.calculate_best_lap()`
4. Service loads CSV, finds minimum lap time
5. Returns JSON: `{"best_lap_time": 129.456, "driver_id": "GR86-015"}`
6. Frontend displays in BestLapCard component

### 3. Real-Time Update Flow

```
User Input → State Change → useEffect Trigger → API Call → State Update → Re-render
```

**Example: Driver Performance**
1. User enters driver ID "GR86-015"
2. `setDriverId("GR86-015")` triggers useEffect
3. useEffect calls performance and consistency APIs
4. Responses update state
5. Component re-renders with new data

## Data Models

### Lap Time Data
```python
{
    "lap": int,
    "vehicle_id": str,
    "lap_time": float,
    "timestamp": str
}
```

### Telemetry Data
```python
{
    "lap": int,
    "vehicle_id": str,
    "telemetry_name": str,  # "vehspd_can", "aps", "pbrake_r"
    "telemetry_value": float,
    "timestamp": str
}
```

### Performance Response
```json
{
    "driver_id": "GR86-015",
    "best_lap": 129.456,
    "average_lap": 130.234,
    "consistency_score": 94.2,
    "total_laps": 30,
    "lap_times": [129.456, 130.123, ...]
}
```

## API Design Principles

### RESTful Conventions
- `GET` for data retrieval
- `POST` for calculations requiring body data
- Resource-based URLs: `/track/{track}/session/{session}/driver/{driver}`

### Response Format
```json
{
    "data": {...},
    "error": null
}
```

Or on error:
```json
{
    "error": "Driver not found"
}
```

### Status Codes
- `200`: Success
- `404`: Resource not found
- `500`: Server error

## Performance Considerations

### Backend Optimizations
1. **Lazy Loading**: Only load data when requested
2. **Row Limiting**: Telemetry limited to 100k rows
3. **Caching**: Future implementation for frequently accessed data
4. **Async Operations**: FastAPI async endpoints

### Frontend Optimizations
1. **Code Splitting**: Vite automatic code splitting
2. **Lazy Components**: React.lazy for large components (future)
3. **Memoization**: useMemo for expensive calculations (future)
4. **Debouncing**: Input debouncing for search (future)

## Security Considerations

### Current Implementation
- CORS enabled for localhost development
- No authentication (hackathon prototype)
- Input validation via Pydantic

### Production Recommendations
1. **Authentication**: JWT tokens or OAuth
2. **Rate Limiting**: Prevent API abuse
3. **Input Sanitization**: Prevent injection attacks
4. **HTTPS**: Encrypted communication
5. **API Keys**: Track usage per user

## Deployment Architecture

### Development
```
Backend: localhost:8000
Frontend: localhost:3000 (Vite dev server)
```

### Production (Recommended)
```
Backend: Deployed on AWS/GCP/Azure
Frontend: Static files on CDN (Vercel/Netlify)
Database: PostgreSQL for persistent storage
Cache: Redis for performance
```

## Scalability Considerations

### Current Limitations
- File-based storage (CSV)
- Single-threaded processing
- No caching layer

### Scaling Strategy
1. **Database**: Migrate CSV to PostgreSQL/TimescaleDB
2. **Caching**: Add Redis for frequently accessed data
3. **Load Balancing**: Multiple backend instances
4. **CDN**: Serve frontend from edge locations
5. **Async Processing**: Celery for heavy computations
6. **Microservices**: Split analytics/telemetry/strategy into separate services

## Technology Choices

### Why FastAPI?
- Fast performance (async support)
- Automatic API documentation
- Type hints and validation
- Modern Python framework

### Why React?
- Component-based architecture
- Large ecosystem
- Excellent developer experience
- TypeScript support

### Why Pandas?
- Optimized for tabular data
- Rich statistical functions
- CSV handling built-in
- NumPy integration

### Why Recharts?
- React-native charts
- Responsive design
- Customizable
- Good documentation

## Testing Strategy (Future)

### Backend Tests
- Unit tests for services
- Integration tests for API endpoints
- Load tests for performance

### Frontend Tests
- Component tests (React Testing Library)
- E2E tests (Playwright/Cypress)
- Visual regression tests

## Monitoring & Logging (Future)

### Backend
- Request logging
- Error tracking (Sentry)
- Performance monitoring (New Relic)

### Frontend
- Error boundary
- Analytics (Google Analytics)
- Performance monitoring (Web Vitals)

## Documentation

### API Documentation
- Automatic via FastAPI Swagger UI
- Available at `/docs`

### Code Documentation
- Docstrings for all functions
- Type hints throughout
- README files in each directory

## Development Workflow

1. **Data Extraction**: `python scripts/extract_data.py`
2. **Backend Development**: Edit services, test with `/docs`
3. **Frontend Development**: Edit components, see live updates
4. **Testing**: Manual testing via dashboard
5. **Deployment**: Build frontend, deploy both services

## Future Architecture Enhancements

1. **WebSocket Support**: Real-time data streaming
2. **GraphQL API**: More flexible data queries
3. **Machine Learning Pipeline**: Separate ML service
4. **Mobile App**: React Native companion app
5. **Data Lake**: Store historical data for ML training
