# Quick Reference Guide

## 🚀 Getting Started (5 Minutes)

```bash
# 1. Extract data
python scripts/extract_data.py

# 2. Start backend (Terminal 1)
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload

# 3. Start frontend (Terminal 2)
cd frontend
npm install
npm run dev

# 4. Open browser
http://localhost:3000
```

## 📁 Project Structure

```
├── backend/              # Python FastAPI backend
│   ├── main.py          # Entry point
│   ├── routers/         # API endpoints
│   └── services/        # Business logic
├── frontend/            # React TypeScript frontend
│   └── src/
│       ├── App.tsx      # Main app
│       └── components/  # UI components
├── scripts/             # Utility scripts
└── data/               # Extracted race data
```

## 🔗 Key URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

## 📊 Available Tracks

1. `barber_motorsports_park`
2. `circuit_of_the_americas`
3. `indianapolis`
4. `road_america`
5. `sebring`
6. `sonoma`
7. `virginia_international_raceway`

## 🎯 Core Features

| Feature | Endpoint | Description |
|---------|----------|-------------|
| Best Lap | `/api/analytics/.../best-lap` | Fastest lap time |
| Driver Performance | `/api/analytics/.../performance` | Comprehensive metrics |
| Braking Analysis | `/api/telemetry/.../braking-analysis` | Braking efficiency |
| Speed Analysis | `/api/telemetry/.../speed-analysis` | vMin/vMax/acceleration |
| Tire Degradation | `/api/strategy/.../tire-degradation` | Wear prediction |
| Pit Strategy | `/api/strategy/.../pit-strategy` | Optimal pit timing |
| Consistency | `/api/strategy/.../consistency` | Driver consistency |

## 🛠️ Common Commands

### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python -m uvicorn backend.main:app --reload

# Run on different port
python -m uvicorn backend.main:app --reload --port 8080

# Check Python version
python --version
```

### Frontend
```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Data
```bash
# Extract all data
python scripts/extract_data.py

# Check extracted data
dir data
```

## 📝 API Quick Examples

### Get Best Lap
```bash
curl http://localhost:8000/api/analytics/track/barber_motorsports_park/session/R1/best-lap
```

### Get Driver Performance
```bash
curl http://localhost:8000/api/analytics/track/barber_motorsports_park/session/R1/driver/GR86-015-000/performance
```

### Calculate Pit Strategy
```bash
curl -X POST http://localhost:8000/api/strategy/track/barber_motorsports_park/session/R1/driver/GR86-015-000/pit-strategy \
  -H "Content-Type: application/json" \
  -d '{"current_lap": 15, "total_laps": 30, "tire_age": 15, "fuel_level": 50.0}'
```

## 🐛 Troubleshooting

### "No Data Found"
```bash
# Solution: Extract data first
python scripts/extract_data.py
```

### "Port already in use"
```bash
# Backend: Use different port
python -m uvicorn backend.main:app --reload --port 8080

# Frontend: Vite will auto-increment port
```

### "Module not found"
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

### "CORS error"
```bash
# Check backend/main.py CORS settings
# Ensure frontend URL is in allow_origins
```

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Project overview |
| SETUP.md | Installation guide |
| FEATURES.md | Feature details |
| ARCHITECTURE.md | Technical architecture |
| API_DOCUMENTATION.md | API reference |
| DEPLOYMENT.md | Production deployment |
| HACKATHON_SUBMISSION.md | Submission info |
| VIDEO_SCRIPT.md | Demo video script |
| PROJECT_SUMMARY.md | Complete summary |
| CHECKLIST.md | Submission checklist |
| GITHUB_SETUP.md | GitHub setup guide |
| QUICK_REFERENCE.md | This file |

## 🎬 Demo Flow

1. **Show Dashboard** → Select track and session
2. **Best Lap Card** → Display fastest lap
3. **Driver Analysis** → Enter driver ID
4. **Performance Metrics** → Show consistency, lap times
5. **Lap Time Chart** → Visualize progression
6. **API Docs** → Show Swagger UI at /docs

## 🔑 Key Metrics

### Performance Metrics
- **Best Lap**: Fastest single lap time
- **Average Lap**: Mean lap time
- **Consistency Score**: % of laps within 0.5s of best
- **Coefficient of Variation**: Std dev / mean * 100

### Telemetry Metrics
- **vMax**: Maximum speed (straights)
- **vMin**: Minimum speed (corners)
- **Brake Efficiency**: Avg / max brake pressure * 100
- **Throttle Average**: Mean throttle position

### Strategy Metrics
- **Degradation Rate**: Seconds lost per lap
- **Optimal Pit Lap**: Best lap to pit
- **Tire Age**: Laps on current tires
- **Projected Time Loss**: Without pit stop

## 🎯 Hackathon Submission

### Required Items
- [x] Code complete
- [x] Documentation complete
- [ ] Demo video (3 minutes)
- [ ] GitHub repository (public)
- [ ] Live deployment
- [ ] Submission form

### Submission Links
- **Category**: Real-Time Analytics
- **GitHub**: [Your repo URL]
- **Demo**: [Your Vercel URL]
- **Video**: [Your YouTube URL]
- **Deadline**: November 25, 2025

## 💡 Tips

### Development
- Use `/docs` for API testing
- Check browser console for errors
- Use React DevTools for debugging
- Monitor backend logs

### Demo
- Have data pre-extracted
- Use a known good driver ID
- Show multiple features
- Keep it under 3 minutes
- Practice beforehand

### Deployment
- Test locally first
- Use free tiers (Vercel + Railway)
- Update CORS for production
- Test live deployment thoroughly

## 🔗 Useful Links

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev
- **Pandas Docs**: https://pandas.pydata.org
- **Recharts Docs**: https://recharts.org
- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app

## 📞 Support

### Documentation
1. Check SETUP.md for installation issues
2. Review FEATURES.md for feature details
3. See API_DOCUMENTATION.md for API help
4. Read DEPLOYMENT.md for deployment issues

### Common Issues
- Data not loading → Run extract_data.py
- API errors → Check /docs endpoint
- Frontend errors → Check browser console
- CORS errors → Update backend CORS settings

## ⚡ Performance Tips

### Backend
- Limit telemetry to 100k rows
- Use caching for repeated queries
- Enable gzip compression
- Use async endpoints

### Frontend
- Use production build for deployment
- Lazy load large components
- Debounce user inputs
- Optimize chart rendering

## 🎉 Success Checklist

- [ ] Data extracted successfully
- [ ] Backend running without errors
- [ ] Frontend displays correctly
- [ ] Can select track and session
- [ ] Best lap displays
- [ ] Driver performance works
- [ ] Charts render properly
- [ ] API docs accessible
- [ ] No console errors
- [ ] Ready for demo!

---

**Quick Start Time**: ~5 minutes
**Full Setup Time**: ~15 minutes
**Demo Preparation**: ~30 minutes

**You're ready to win! 🏁🏆**
