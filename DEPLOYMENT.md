# Deployment Guide

## Overview

This guide covers deploying the GR Cup Racing Intelligence System to production. We'll use free/low-cost services suitable for a hackathon demo.

## Recommended Stack

- **Frontend**: Vercel (free tier)
- **Backend**: Railway or Render (free tier)
- **Database**: Not required (file-based for now)

## Option 1: Vercel + Railway (Recommended)

### Step 1: Deploy Backend to Railway

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository

3. **Configure Backend**
   - Railway will auto-detect Python
   - Add environment variables if needed
   - Set start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

4. **Add Procfile** (optional)
   ```
   web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Deploy**
   - Railway will automatically deploy
   - Note your backend URL: `https://your-app.railway.app`

### Step 2: Deploy Frontend to Vercel

1. **Update API URL**
   - Edit `frontend/vite.config.ts`
   - Update proxy target to Railway URL:
   ```typescript
   export default defineConfig({
     plugins: [react()],
     server: {
       proxy: {
         '/api': {
           target: 'https://your-app.railway.app',
           changeOrigin: true
         }
       }
     }
   })
   ```

2. **Create Vercel Account**
   - Go to https://vercel.com
   - Sign up with GitHub

3. **Import Project**
   - Click "New Project"
   - Import your GitHub repository
   - Select `frontend` as root directory

4. **Configure Build**
   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

5. **Environment Variables**
   - Add `VITE_API_URL=https://your-app.railway.app`

6. **Deploy**
   - Click "Deploy"
   - Your site will be live at `https://your-app.vercel.app`

### Step 3: Update CORS

Update `backend/main.py` to allow your Vercel domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://your-app.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Option 2: Render (All-in-One)

### Deploy Backend

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Name: `gr-cup-backend`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

3. **Deploy**
   - Render will build and deploy
   - Note your URL: `https://gr-cup-backend.onrender.com`

### Deploy Frontend

1. **Create Static Site**
   - Click "New +" → "Static Site"
   - Connect GitHub repository
   - Name: `gr-cup-frontend`
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`

2. **Environment Variables**
   - Add `VITE_API_URL=https://gr-cup-backend.onrender.com`

3. **Deploy**
   - Your site will be live at `https://gr-cup-frontend.onrender.com`

## Option 3: Docker Deployment

### Create Dockerfiles

**Backend Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY data/ ./data/

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile**:
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

### Deploy to Any Cloud

1. **Build Images**
   ```bash
   docker-compose build
   ```

2. **Push to Registry**
   ```bash
   docker tag gr-cup-backend:latest your-registry/gr-cup-backend
   docker push your-registry/gr-cup-backend
   ```

3. **Deploy to Cloud**
   - AWS ECS
   - Google Cloud Run
   - Azure Container Instances
   - DigitalOcean App Platform

## Data Handling in Production

### Option A: Include Data in Deployment

**Pros**: Simple, no external dependencies
**Cons**: Large deployment size

1. Extract data locally
2. Include `data/` directory in deployment
3. Update `.gitignore` to allow data files (temporarily)

### Option B: Cloud Storage

**Pros**: Smaller deployments, easier updates
**Cons**: More complex setup

1. Upload data to S3/GCS/Azure Blob
2. Update services to load from cloud storage
3. Add cloud SDK dependencies

**Example for S3**:
```python
import boto3
import pandas as pd
from io import StringIO

s3 = boto3.client('s3')
obj = s3.get_object(Bucket='gr-cup-data', Key='barber/R1_lap_time.csv')
df = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
```

## Environment Variables

Create `.env` file for production:

```env
# Backend
PORT=8000
ENVIRONMENT=production
CORS_ORIGINS=https://your-frontend.vercel.app

# Frontend
VITE_API_URL=https://your-backend.railway.app
```

## Performance Optimization

### Backend

1. **Enable Caching**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def get_lap_times(track, session):
       # Cached for repeated calls
       pass
   ```

2. **Add Compression**
   ```python
   from fastapi.middleware.gzip import GZipMiddleware
   app.add_middleware(GZipMiddleware, minimum_size=1000)
   ```

3. **Database Migration** (future)
   - Move from CSV to PostgreSQL
   - Use connection pooling
   - Add indexes

### Frontend

1. **Enable Production Build**
   ```bash
   npm run build
   ```

2. **Add CDN** (Vercel does this automatically)

3. **Lazy Loading**
   ```typescript
   const Dashboard = lazy(() => import('./components/Dashboard'))
   ```

## Monitoring

### Backend Monitoring

1. **Add Health Check**
   ```python
   @app.get("/health")
   async def health():
       return {"status": "healthy", "timestamp": datetime.now()}
   ```

2. **Error Tracking** (Sentry)
   ```python
   import sentry_sdk
   sentry_sdk.init(dsn="your-dsn")
   ```

3. **Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

### Frontend Monitoring

1. **Error Boundary**
   ```typescript
   class ErrorBoundary extends React.Component {
     componentDidCatch(error, errorInfo) {
       console.error('Error:', error, errorInfo)
     }
   }
   ```

2. **Analytics** (Google Analytics)
   ```typescript
   import ReactGA from 'react-ga4'
   ReactGA.initialize('G-XXXXXXXXXX')
   ```

## SSL/HTTPS

Both Vercel and Railway provide automatic HTTPS. No configuration needed!

## Custom Domain (Optional)

### Vercel
1. Go to Project Settings → Domains
2. Add your domain
3. Update DNS records as instructed

### Railway
1. Go to Settings → Domains
2. Add custom domain
3. Update DNS CNAME record

## Deployment Checklist

- [ ] Extract all race data
- [ ] Test locally (backend + frontend)
- [ ] Update CORS origins
- [ ] Set environment variables
- [ ] Deploy backend
- [ ] Update frontend API URL
- [ ] Deploy frontend
- [ ] Test production deployment
- [ ] Check all API endpoints
- [ ] Verify data loading
- [ ] Test on mobile devices
- [ ] Add custom domain (optional)
- [ ] Set up monitoring
- [ ] Update README with live URLs

## Troubleshooting

### Backend Won't Start
- Check Python version (3.11+)
- Verify requirements.txt installed
- Check PORT environment variable
- Review logs for errors

### Frontend Can't Connect to Backend
- Verify CORS settings
- Check API URL in frontend config
- Test backend health endpoint directly
- Check browser console for errors

### Data Not Loading
- Verify data directory exists
- Check file paths in services
- Ensure CSV files are included in deployment
- Review backend logs

### Slow Performance
- Enable caching
- Add compression
- Optimize database queries
- Use CDN for frontend assets

## Cost Estimates

### Free Tier (Recommended for Hackathon)
- Vercel: Free (hobby plan)
- Railway: $5/month credit (free trial)
- Render: Free tier available
- **Total**: $0-5/month

### Production Scale
- Vercel Pro: $20/month
- Railway: ~$10-20/month
- Database: $10-25/month
- **Total**: $40-65/month

## Post-Deployment

1. **Update README**
   - Add live demo URL
   - Update installation instructions
   - Add deployment badge

2. **Share Links**
   - Update hackathon submission
   - Share on social media
   - Add to portfolio

3. **Monitor Performance**
   - Check error rates
   - Monitor response times
   - Review user feedback

## Support

For deployment issues:
- Check service status pages
- Review deployment logs
- Consult platform documentation
- Open GitHub issue

---

**Recommended for Hackathon**: Vercel (frontend) + Railway (backend)
**Deployment Time**: ~30 minutes
**Cost**: Free tier sufficient for demo
