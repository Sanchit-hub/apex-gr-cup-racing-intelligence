# How to Push to GitHub - Simple Instructions

## Step 1: Double-Click This File
```
INITIALIZE_AND_PUSH.bat
```

This will initialize Git and prepare everything.

## Step 2: Create GitHub Repository

1. Go to **https://github.com**
2. Click **"+"** (top right) → **"New repository"**
3. Settings:
   - **Name**: `apex-gr-cup-racing-intelligence`
   - **Description**: `APEX - Real-time racing intelligence for Toyota GR Cup`
   - **Visibility**: **PUBLIC** ✅ (MUST be public!)
   - **Do NOT** check "Initialize with README"
4. Click **"Create repository"**
5. **Copy the repository URL** (looks like):
   ```
   https://github.com/YOUR_USERNAME/apex-gr-cup-racing-intelligence.git
   ```

## Step 3: Push to GitHub

Open Command Prompt in this folder and run:

```bash
git remote add origin YOUR_REPO_URL
git push -u origin main
```

**Replace YOUR_REPO_URL** with the URL you copied!

**Example:**
```bash
git remote add origin https://github.com/john/apex-gr-cup-racing-intelligence.git
git push -u origin main
```

## Step 4: Add Topics

On your GitHub repository page:
1. Click **"⚙️"** next to "About"
2. Add these topics:
   - `toyota-gr-cup`
   - `racing-analytics`
   - `motorsports`
   - `telemetry`
   - `fastapi`
   - `react`
   - `typescript`
   - `hackathon`

## Step 5: Submit to Hackathon

Use information from **HACKATHON_SUBMISSION_FINAL.md** to fill out the submission form!

---

## ✅ Essential Files for Hackathon

These files WILL be pushed to GitHub:
- ✅ README.md
- ✅ PROJECT_STORY.md (your hackathon narrative)
- ✅ HACKATHON_SUBMISSION_FINAL.md (submission info)
- ✅ ARCHITECTURE.md
- ✅ API_DOCUMENTATION.md
- ✅ FEATURES.md
- ✅ SETUP.md
- ✅ VIDEO_SCRIPT.md
- ✅ LICENSE
- ✅ backend/ folder
- ✅ frontend/ folder
- ✅ scripts/ folder
- ✅ requirements.txt
- ✅ .gitignore

## ❌ Files NOT Pushed (Too Large)

These are automatically excluded by .gitignore:
- ❌ data/ folder
- ❌ .zip files (track data)
- ❌ .pdf files (circuit maps)
- ❌ node_modules/
- ❌ __pycache__/

---

**That's it! Total time: ~10 minutes**
