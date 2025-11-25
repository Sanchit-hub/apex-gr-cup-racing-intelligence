# 📁 Repository Structure

## Overview
This document describes the organization of the APEX repository.

---

## 📂 Root Directory

### Core Documentation
| File | Purpose |
|------|---------|
| `README.md` | Main project overview, quick start, features |
| `HACKATHON_SUBMISSION.md` | Complete hackathon submission document |
| `PROJECT_STORY.md` | Hackathon narrative (inspiration, what, how, challenges) |
| `CONTRIBUTING.md` | Contribution guidelines for developers |
| `SUBMISSION_CHECKLIST.md` | Pre-submission verification checklist |
| `LICENSE` | MIT License |

### Technical Documentation
| File | Purpose |
|------|---------|
| `ARCHITECTURE.md` | System architecture and design decisions |
| `API_DOCUMENTATION.md` | Complete API reference with examples |
| `FEATURES.md` | Detailed feature documentation |
| `SETUP.md` | Local development setup guide |

### Deployment Guides
| File | Purpose |
|------|---------|
| `AWS_SETUP_GUIDE.md` | AWS S3 setup and configuration |
| `RENDER_DEPLOYMENT_GUIDE.md` | Backend deployment on Render |
| `LOCAL_DEMO_GUIDE.md` | Running the app locally |

### Configuration Files
| File | Purpose |
|------|---------|
| `.env.example` | Environment variable template |
| `.gitignore` | Git ignore rules |
| `requirements.txt` | Python dependencies |
| `runtime.txt` | Python version for deployment |
| `render.yaml` | Render deployment configuration |
| `netlify.toml` | Netlify deployment configuration |
| `railway.json` | Railway deployment configuration (backup) |

### Utility Scripts
| File | Purpose |
|------|---------|
| `upload_to_s3.py` | Upload race data to AWS S3 |
| `create_sampled_data.py` | Create sampled data for demo |
| `prepare_deployment_data.py` | Prepare data for deployment |

---

## 📂 Backend (`/backend`)

### Structure
```
backend/
├── main.py                 # FastAPI application entry point
├── __init__.py            # Package initialization
├── config/                # Configuration files
├── routers/               # API route handlers
│   ├── analytics.py       # Analytics endpoints
│   └── mock_analytics.py  # Mock data endpoints
└── services/              # Business logic
    ├── lap_analyzer.py    # Lap time analysis
    ├── s3_data_loader.py  # AWS S3 data loading
    └── mock_data.py       # Mock data generation
```

### Key Files
- **`main.py`**: FastAPI app with CORS, routes, and health check
- **`lap_analyzer.py`**: Core analytics engine for lap times
- **`s3_data_loader.py`**: Loads race data from AWS S3
- **`analytics.py`**: REST API endpoints for race analytics

---

## 📂 Frontend (`/frontend`)

### Structure
```
frontend/
├── src/
│   ├── main.tsx           # Application entry point
│   ├── App.tsx            # Main app component
│   ├── components/        # React components
│   │   ├── Dashboard.tsx  # Main dashboard
│   │   └── TrackSelector.tsx  # Track/session selector
│   └── index.css          # Global styles
├── public/                # Static assets
├── package.json           # Node dependencies
├── vite.config.ts         # Vite configuration
├── tsconfig.json          # TypeScript configuration
└── tailwind.config.js     # TailwindCSS configuration
```

### Key Files
- **`App.tsx`**: Main application with track/session management
- **`Dashboard.tsx`**: Analytics dashboard with data visualization
- **`TrackSelector.tsx`**: Track and session selection UI
- **`vite.config.ts`**: Dev server and API proxy configuration

---

## 📂 Scripts (`/scripts`)

Utility scripts for data processing and setup.

---

## 📂 Data (`/data`)

**Note**: Excluded from git (too large)

Contains race telemetry data for all 7 tracks:
- Barber Motorsports Park
- Circuit of the Americas (COTA)
- Indianapolis Motor Speedway
- Road America
- Sebring International Raceway
- Sonoma Raceway
- Virginia International Raceway (VIR)

---

## 📂 Specs (`.kiro/specs`)

Feature specifications following spec-driven development:
- `aws-s3-data-hosting/` - AWS S3 integration spec
  - `requirements.md` - Feature requirements
  - `design.md` - Technical design
  - `tasks.md` - Implementation tasks

---

## 🚫 Excluded from Git

### Via `.gitignore`
- `data/` - Race data (3GB+, hosted on S3)
- `deploy_data/` - Deployment data
- `venv/` - Python virtual environment
- `node_modules/` - Node dependencies
- `*.zip` - Data archives
- `*.pdf` - Track maps
- `*.log` - Log files
- `.env` - Environment variables
- `__pycache__/` - Python cache

---

## 📊 Repository Statistics

### File Counts
- **Python files**: ~10
- **TypeScript/React files**: ~5
- **Documentation files**: ~15
- **Configuration files**: ~10

### Lines of Code (Approximate)
- **Backend**: ~1,500 lines
- **Frontend**: ~800 lines
- **Documentation**: ~5,000 lines
- **Total**: ~7,300 lines

---

## 🎯 Key Directories

### For Development
- `/backend` - Backend API code
- `/frontend` - Frontend React app
- `/scripts` - Utility scripts

### For Documentation
- Root directory - All markdown docs
- `.kiro/specs` - Feature specifications

### For Deployment
- `render.yaml` - Backend deployment
- `netlify.toml` - Frontend deployment
- `requirements.txt` - Python dependencies

---

## 📝 Documentation Hierarchy

1. **Start Here**: `README.md`
2. **Hackathon Submission**: `HACKATHON_SUBMISSION.md`
3. **Technical Deep-Dive**: `ARCHITECTURE.md`
4. **API Reference**: `API_DOCUMENTATION.md`
5. **Setup Guide**: `SETUP.md`
6. **Deployment**: `AWS_SETUP_GUIDE.md`, `RENDER_DEPLOYMENT_GUIDE.md`
7. **Contributing**: `CONTRIBUTING.md`

---

## 🔄 Workflow

### Development
1. Clone repository
2. Follow `SETUP.md`
3. Run backend and frontend
4. Make changes
5. Test locally
6. Submit PR (see `CONTRIBUTING.md`)

### Deployment
1. Follow `AWS_SETUP_GUIDE.md` for S3
2. Follow `RENDER_DEPLOYMENT_GUIDE.md` for backend
3. Frontend auto-deploys via Netlify

---

## ✅ Repository Health

- ✅ Clean structure
- ✅ Comprehensive documentation
- ✅ No sensitive data
- ✅ Proper .gitignore
- ✅ MIT License
- ✅ Professional README
- ✅ Production-ready code

---

**Last Updated**: After cleanup  
**Status**: ✅ **SUBMISSION READY**
