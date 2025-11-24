# Manual GitHub Upload Guide

Since Git is not installed on your system, here's how to upload your project to GitHub manually:

## Option 1: Install Git (Recommended)

1. Download Git for Windows: https://git-scm.com/download/win
2. Install with default settings
3. Restart your terminal
4. Run these commands:

```bash
cd "C:\TOYOTA TRACKS DATA"
git init
git add .
git commit -m "Initial commit: APEX - Toyota GR Cup Racing Intelligence"
git remote add origin YOUR_GITHUB_REPO_URL
git branch -M main
git push -u origin main
```

## Option 2: GitHub Desktop (Easiest)

1. Download GitHub Desktop: https://desktop.github.com/
2. Install and sign in to GitHub
3. Click "Add" → "Add Existing Repository"
4. Browse to: `C:\TOYOTA TRACKS DATA`
5. Click "Publish repository"
6. Make sure "Keep this code private" is UNCHECKED (must be public for hackathon)
7. Click "Publish Repository"

## Option 3: Manual Upload via GitHub Web Interface

### Step 1: Create Repository on GitHub
1. Go to https://github.com
2. Click "+" → "New repository"
3. Repository name: `apex-gr-cup-racing-intelligence`
4. Description: `APEX - Real-time racing intelligence for Toyota GR Cup`
5. Make sure it's **PUBLIC**
6. Don't initialize with README (we have one)
7. Click "Create repository"

### Step 2: Prepare Files for Upload

**IMPORTANT**: Before uploading, you need to exclude large files:

1. Open File Explorer
2. Navigate to: `C:\TOYOTA TRACKS DATA`
3. **DELETE or MOVE these folders/files** (they're too large for GitHub):
   - `data/` folder (all extracted race data)
   - All `.zip` files (barber-motorsports-park.zip, etc.)
   - All `.pdf` files (circuit maps)

4. Keep these files (they're documentation):
   - All `.md` files
   - `backend/` folder
   - `frontend/` folder
   - `scripts/` folder
   - `.gitignore`
   - `LICENSE`
   - `requirements.txt`
   - `quickstart.bat`

### Step 3: Upload Files

**Method A: Drag and Drop (for small projects)**
1. On your GitHub repository page, click "uploading an existing file"
2. Drag and drop all files/folders (except data, zips, pdfs)
3. Add commit message: "Initial commit: APEX - Toyota GR Cup Racing Intelligence"
4. Click "Commit changes"

**Method B: Upload Folder by Folder (recommended)**
1. Click "Add file" → "Upload files"
2. Upload `backend/` folder
3. Commit with message: "Add backend"
4. Repeat for `frontend/`, `scripts/`, and all `.md` files
5. Upload root files (README.md, LICENSE, etc.)

## Option 4: Use GitHub CLI

1. Download GitHub CLI: https://cli.github.com/
2. Install and run:

```bash
gh auth login
cd "C:\TOYOTA TRACKS DATA"
gh repo create apex-gr-cup-racing-intelligence --public --source=. --remote=origin --push
```

## After Upload: Verify

1. Go to your repository on GitHub
2. Check that these files are present:
   - ✅ README.md
   - ✅ PROJECT_STORY.md
   - ✅ HACKATHON_SUBMISSION_FINAL.md
   - ✅ backend/ folder
   - ✅ frontend/ folder
   - ✅ LICENSE
   - ✅ requirements.txt

3. Check that these are NOT present (too large):
   - ❌ data/ folder
   - ❌ .zip files
   - ❌ .pdf files

## Add Repository Topics

1. On your repository page, click "⚙️" next to "About"
2. Add topics:
   - `toyota-gr-cup`
   - `racing-analytics`
   - `motorsports`
   - `telemetry`
   - `fastapi`
   - `react`
   - `typescript`
   - `hackathon`
   - `real-time-analytics`

## Final Steps

1. Copy your repository URL (e.g., `https://github.com/username/apex-gr-cup-racing-intelligence`)
2. Go to hackathon submission page
3. Paste your repository URL
4. Copy information from `HACKATHON_SUBMISSION_FINAL.md` into submission form
5. Submit!

## Important Notes

- **Repository MUST be public** for hackathon submission
- **Don't upload data files** - they're too large and covered by .gitignore
- **Include all documentation** - README.md, PROJECT_STORY.md, etc.
- **Test your repository** - Make sure others can see it

## Need Help?

If you get stuck:
1. Try GitHub Desktop (easiest option)
2. Or install Git and use command line
3. Or contact me for assistance

---

**Recommended**: Use GitHub Desktop - it's the easiest way to upload your project without command line experience.
