@echo off
cd /d "%~dp0"
echo ========================================
echo APEX - GitHub Push Script
echo ========================================
echo.
echo Current directory: %CD%
echo.

echo Checking Git installation...
git --version
if errorlevel 1 (
    echo.
    echo ERROR: Git is not found!
    echo Please close this window and open a NEW Command Prompt.
    echo Then navigate to this folder and run this script again.
    echo.
    pause
    exit /b 1
)

echo.
echo Git is installed! Proceeding...
echo.

echo Step 1: Initializing Git repository...
if exist ".git" (
    echo Git repository already initialized.
) else (
    git init
    if errorlevel 1 (
        echo Git init failed!
        pause
        exit /b 1
    )
    echo ✓ Git initialized
)
echo.

echo Step 2: Configuring Git (if needed)...
git config user.name >nul 2>&1
if errorlevel 1 (
    echo Please enter your name for Git commits:
    set /p username="Your Name: "
    git config user.name "!username!"
    
    echo Please enter your email for Git commits:
    set /p useremail="Your Email: "
    git config user.email "!useremail!"
)
echo ✓ Git configured
echo.

echo Step 3: Adding all files...
git add .
if errorlevel 1 (
    echo Git add failed!
    pause
    exit /b 1
)
echo ✓ Files added
echo.

echo Step 4: Creating initial commit...
git commit -m "Initial commit: APEX - Toyota GR Cup Racing Intelligence System"
if errorlevel 1 (
    echo Note: Commit may have failed if no changes detected
)
echo ✓ Commit created
echo.

echo Step 5: Setting default branch to main...
git branch -M main
echo ✓ Branch set to main
echo.

echo ========================================
echo READY TO PUSH!
echo ========================================
echo.
echo Your code is ready to push to GitHub!
echo.
echo NEXT STEPS:
echo.
echo 1. Go to https://github.com and sign in
echo 2. Click the "+" icon (top right) and select "New repository"
echo 3. Repository settings:
echo    - Name: apex-gr-cup-racing-intelligence
echo    - Description: APEX - Real-time racing intelligence for Toyota GR Cup
echo    - Visibility: PUBLIC (very important!)
echo    - Do NOT initialize with README
echo 4. Click "Create repository"
echo.
echo 5. Copy the repository URL (it will look like):
echo    https://github.com/YOUR_USERNAME/apex-gr-cup-racing-intelligence.git
echo.
echo 6. Run this command (replace YOUR_REPO_URL with your actual URL):
echo.
echo    git remote add origin YOUR_REPO_URL
echo    git push -u origin main
echo.
echo EXAMPLE:
echo    git remote add origin https://github.com/john/apex-gr-cup-racing-intelligence.git
echo    git push -u origin main
echo.
echo ========================================
echo.
pause
