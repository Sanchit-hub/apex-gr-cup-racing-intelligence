"""FastAPI backend for GR Cup Analytics."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Use mock data if data directory doesn't exist (for deployment)
USE_MOCK_DATA = not os.path.exists("data") or len(os.listdir("data")) == 0

if USE_MOCK_DATA:
    from backend.routers import mock_analytics as analytics
    from backend.routers import mock_strategy as strategy
    from backend.routers import telemetry  # Keep telemetry as is
else:
    from backend.routers import analytics, telemetry, strategy

app = FastAPI(
    title="GR Cup Racing Intelligence API",
    description="Real-time analytics and strategy engine for Toyota GR Cup",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(telemetry.router, prefix="/api/telemetry", tags=["telemetry"])
app.include_router(strategy.router, prefix="/api/strategy", tags=["strategy"])

@app.get("/")
async def root():
    return {
        "message": "GR Cup Racing Intelligence API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
