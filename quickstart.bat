@echo off
echo ========================================
echo GR Cup Racing Intelligence System
echo Quick Start Script
echo ========================================
echo.

echo Step 1: Extracting race data...
python scripts/extract_data.py
if errorlevel 1 (
    echo ERROR: Failed to extract data
    pause
    exit /b 1
)
echo.

echo Step 2: Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo.

echo Step 3: Installing frontend dependencies...
cd frontend
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)
cd ..
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo.
echo 1. Start backend (in this window):
echo    python -m uvicorn backend.main:app --reload
echo.
echo 2. Start frontend (in new window):
echo    cd frontend
echo    npm run dev
echo.
echo Then open http://localhost:3000 in your browser
echo.
pause
