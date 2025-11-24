@echo off
cd /d "C:\TOYOTA TRACKS DATA"
echo ========================================
echo APEX - Initializing Git and Pushing
echo ========================================
echo.
echo Working in: C:\TOYOTA TRACKS DATA
echo.

echo Step 1: Initializing Git...
git init
echo.

echo Step 2: Adding all important files...
git add .
echo.

echo Step 3: Creating commit...
git commit -m "Initial commit: APEX - Toyota GR Cup Racing Intelligence System"
echo.

echo Step 4: Setting branch to main...
git branch -M main
echo.

echo ========================================
echo GIT INITIALIZED SUCCESSFULLY!
echo ========================================
echo.
echo Now you need to:
echo.
echo 1. Create a repository on GitHub:
echo    - Go to https://github.com
echo    - Click + (top right) then "New repository"
echo    - Name: apex-gr-cup-racing-intelligence
echo    - Make it PUBLIC
echo    - Do NOT initialize with README
echo    - Click "Create repository"
echo.
echo 2. Copy your repository URL from GitHub
echo.
echo 3. Run these commands (replace YOUR_REPO_URL):
echo.
echo    git remote add origin YOUR_REPO_URL
echo    git push -u origin main
echo.
echo Example:
echo    git remote add origin https://github.com/username/apex-gr-cup-racing-intelligence.git
echo    git push -u origin main
echo.
echo ========================================
pause
