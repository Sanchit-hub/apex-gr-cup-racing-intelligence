# Toyota GR Cup Hackathon Submission

## Project Title
**GR Cup Real-Time Racing Intelligence System**

## Category
- **Primary**: Real-Time Analytics
- **Secondary**: Driver Training & Insights

## Datasets Used
All 7 Toyota GR Cup race tracks:
1. Barber Motorsports Park
2. Circuit of the Americas (COTA)
3. Indianapolis Motor Speedway
4. Road America
5. Sebring International Raceway
6. Sonoma Raceway
7. Virginia International Raceway (VIR)

## Project Description

A comprehensive real-time analytics and strategy engine for Toyota GR Cup racing that transforms raw telemetry data into actionable insights for drivers and race engineers.

### Core Features

#### 1. Lap-Time & Sector Analysis
- Calculates theoretical best lap from combined best sectors
- Real-time delta comparison vs optimal lap
- Identifies time loss/gain per sector
- Lap-by-lap performance tracking

#### 2. Braking & Acceleration Intelligence
- Detects optimal braking points
- Identifies late/early braking patterns
- Analyzes vMin (corner entry speed) and vMax (straight-line speed)
- Throttle application optimization recommendations

#### 3. Racing Line Evaluation
- Compares driver's line to optimal racing line
- Tracks position deviation metrics
- Corner-by-corner performance breakdown

#### 4. Tire Degradation Modeling
- Predicts lap-by-lap tire performance
- Recommends optimal pit windows
- Analyzes wear rate based on driving style
- Real-time degradation tracking

#### 5. Real-Time Strategy Engine
- Live race position simulation
- Pit stop delta calculator
- Alternative strategy outcome predictions
- Performance alerts (overheating, pace drop, consistency issues)

#### 6. Interactive Dashboard
- Live telemetry visualization
- Multi-driver comparison
- Session replay with insights
- Exportable performance reports

### Technical Implementation

**Backend (Python + FastAPI)**
- RESTful API with 15+ endpoints
- Pandas/NumPy for high-performance data processing
- Modular service architecture (analytics, telemetry, strategy)
- Real-time data streaming capabilities

**Frontend (React + TypeScript)**
- Modern, responsive dashboard
- Real-time data visualization with Recharts
- Track and session selector
- Driver performance analytics
- Lap time progression charts

**Analytics Engine**
- Lap time prediction models
- Statistical consistency analysis
- Tire degradation algorithms
- Pit strategy optimization

### Research Foundation

This project is built on peer-reviewed motorsports research:
- ML-based lap time prediction (97% accuracy)
- Reinforcement learning for optimal racing lines
- Real-time telemetry pipeline architectures from FSAE/F1
- Tire strategy optimization models
- Driver coaching AI systems

### Impact & Value

**For Drivers:**
- Immediate feedback on performance
- Clear identification of improvement areas
- Data-driven coaching insights
- Consistency tracking

**For Race Engineers:**
- Real-time strategy decisions
- Tire management optimization
- Pit window calculations
- Multi-driver comparison

**For Teams:**
- Historical performance analysis
- Setup optimization data
- Driver development tracking
- Race strategy planning

## Installation & Usage

### Quick Start
```bash
# Extract race data
python scripts/extract_data.py

# Start backend
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload

# Start frontend (in new terminal)
cd frontend
npm install
npm run dev
```

Access dashboard at `http://localhost:3000`

### API Documentation
Interactive API docs available at `http://localhost:8000/docs`

## Technical Stack

- **Backend**: Python 3.11, FastAPI, Pandas, NumPy, Scikit-learn
- **Frontend**: React 18, TypeScript, Recharts, TailwindCSS, Vite
- **Data Processing**: CSV parsing, statistical analysis, ML predictions
- **Deployment Ready**: Docker support, production build scripts

## Project Links

- **GitHub Repository**: [Your repo URL]
- **Live Demo**: [Deployment URL if available]
- **Demo Video**: [3-minute video link]
- **Documentation**: See SETUP.md and README.md

## Future Enhancements

1. **Machine Learning Models**
   - LSTM for lap time prediction
   - Reinforcement learning for optimal racing lines
   - Computer vision for racing line detection

2. **Advanced Features**
   - Weather impact analysis
   - Multi-car race simulation
   - Predictive maintenance alerts
   - Driver comparison heatmaps

3. **Real-Time Integration**
   - Live race data streaming
   - WebSocket connections
   - Mobile app companion
   - Team radio integration

## Team Information

Built for the Toyota GR Cup "Hack the Track" Hackathon 2025

## License

MIT License - Open source for the motorsports community

---

**Submission Date**: November 25, 2025
**Hackathon**: Toyota GR Cup - Hack the Track
**Prize Pool**: $20,000
