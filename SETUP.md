# Setup Guide - GR Cup Racing Intelligence System

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

## Installation Steps

### 1. Extract Race Data

First, extract all the race data from the ZIP files:

```bash
python scripts/extract_data.py
```

This will create a `data/` directory with all track data organized by track name.

### 2. Backend Setup

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI backend server:

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### 3. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install
```

Start the development server:

```bash
npm run dev
```

The dashboard will be available at `http://localhost:3000`

## API Endpoints

### Analytics
- `GET /api/analytics/tracks` - List all available tracks
- `GET /api/analytics/track/{track}/sessions` - Get sessions for a track
- `GET /api/analytics/track/{track}/session/{session}/best-lap` - Get best lap
- `GET /api/analytics/track/{track}/session/{session}/driver/{driver_id}/performance` - Driver performance
- `GET /api/analytics/track/{track}/session/{session}/sector-analysis` - Sector analysis

### Telemetry
- `GET /api/telemetry/track/{track}/session/{session}/driver/{driver_id}/lap/{lap}` - Lap telemetry
- `GET /api/telemetry/track/{track}/session/{session}/driver/{driver_id}/braking-analysis` - Braking analysis
- `GET /api/telemetry/track/{track}/session/{session}/driver/{driver_id}/speed-analysis` - Speed analysis

### Strategy
- `POST /api/strategy/track/{track}/session/{session}/driver/{driver_id}/pit-strategy` - Pit strategy
- `GET /api/strategy/track/{track}/session/{session}/driver/{driver_id}/tire-degradation` - Tire degradation
- `GET /api/strategy/track/{track}/session/{session}/driver/{driver_id}/consistency` - Consistency metrics

## Project Structure

```
.
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── routers/                # API endpoints
│   │   ├── analytics.py
│   │   ├── telemetry.py
│   │   └── strategy.py
│   └── services/               # Business logic
│       ├── lap_analyzer.py
│       ├── telemetry_analyzer.py
│       └── strategy_engine.py
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── App.tsx
│   │   └── main.tsx
│   └── package.json
├── scripts/
│   └── extract_data.py         # Data extraction script
├── data/                       # Extracted race data (gitignored)
└── requirements.txt
```

## Troubleshooting

### Data Not Found
If you see "No Data Found" in the dashboard:
1. Make sure you ran `python scripts/extract_data.py`
2. Check that ZIP files are in the root directory
3. Verify the `data/` directory was created

### API Connection Issues
If the frontend can't connect to the backend:
1. Ensure the backend is running on port 8000
2. Check the Vite proxy configuration in `frontend/vite.config.ts`
3. Try accessing `http://localhost:8000/health` directly

### Missing Dependencies
If you get import errors:
- Backend: `pip install -r requirements.txt`
- Frontend: `cd frontend && npm install`

## Next Steps

1. Extract all track data
2. Start both backend and frontend servers
3. Select a track and session in the dashboard
4. Enter a driver ID to see performance analytics
5. Explore the API documentation at `/docs`

## Development

To build for production:

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm run build
```

The frontend build will be in `frontend/dist/`
