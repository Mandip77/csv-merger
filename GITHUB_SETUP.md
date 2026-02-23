# GitHub Setup Guide for CSV Merger

Follow these steps to publish your CSV Merger open-source project to GitHub.

## Step 1: Create a GitHub Account (if needed)
1. Go to https://github.com
2. Sign up or log in

## Step 2: Create a New Repository

1. Click **+ New** (top-left corner, or go to https://github.com/new)
2. Fill in details:
   - **Repository name**: `csv-merger`
   - **Description**: `A modern desktop app for merging and transforming CSV files`
   - **Visibility**: Select **Public** (for open-source)
   - **Initialize repository**: DO NOT check "Initialize with README" (we'll push our own)
3. Click **Create repository**

## Step 3: Push Your Local Code to GitHub

### On Windows (PowerShell):
```powershell
# Navigate to the project root (the parent of practise/)
cd C:\Users\mandi\Desktop\Develop\PythonProject

# Initialize git (if not already initialized)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: CSV Merger open-source release"

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/csv-merger.git

# Push to main branch
git branch -M main
git push -u origin main
```

### On macOS / Linux:
```bash
# Same commands as above (bash shell)
cd path/to/PythonProject
git init
git add .
git commit -m "Initial commit: CSV Merger open-source release"
git remote add origin https://github.com/YOUR_USERNAME/csv-merger.git
git branch -M main
git push -u origin main
```

**Note**: You'll be prompted for authentication. Use:
- **Option 1**: GitHub username + **personal access token** (recommended)
  - Create token: https://github.com/settings/tokens
  - Select scopes: `repo` (full control)
- **Option 2**: GitHub CLI: `gh auth login`

## Step 4: Verify on GitHub

1. Go to https://github.com/YOUR_USERNAME/csv-merger
2. Verify your code is visible:
   - README.md is displayed
   - LICENSE shown
   - All files present

## Step 5: Create a Release

To make the installer downloadable from GitHub:

1. Go to **Releases** (right sidebar of your repo)
2. Click **Draft a new release**
3. Fill in:
   - **Tag**: `v1.0.0`
   - **Release title**: `CSV Merger v1.0.0 - Initial Release`
   - **Description**: 
     ```
     Initial open-source release of CSV Merger!
     
     **Features:**
     - Multi-file CSV merging
     - Advanced filtering and transformations
     - Multiple export formats
     - Modern desktop UI
     
     **Download:**
     - Windows installer (.exe)
     - Source code (zip/tar)
     ```
4. Upload attachments:
   - Drag `installer/Output/CSV_Merger_Installer.exe` into the release
   - Optionally add screenshot of the app
5. Click **Publish release**

## Step 6: Add Topics (for Discoverability)

From your repo page, click the **About** gear icon (right side):

1. Add **topics**: `csv`, `data-processing`, `desktop-app`, `python`, `gui`
2. Add **description**: "A modern desktop application for merging and transforming CSV files"
3. Set **homepage URL**: Your portfolio site (optional)

## Step 7: Add GitHub Social Links (Optional)

Enable **Discussions** for community:
1. Go to **Settings** → **Features**
2. Check **Discussions**

## Step 8: Update Your README on GitHub

If you need to make changes:
```bash
# Edit README.md or any file
# Then:
git add README.md
git commit -m "Update README with better instructions"
git push origin main
```

## Common Next Steps

### Add GitHub Actions CI/CD (Optional)
Auto-build installers on each release:
1. Create `.github/workflows/build.yml`
2. Set up PyInstaller + Inno Setup compilation
3. Auto-upload artifacts to releases

### Add a GitHub Pages Site (Optional)
Host a landing page:
1. Create `docs/index.html` in repo
2. Enable **Settings** → **Pages** → Source: `/docs`
3. Access your site at `https://YOUR_USERNAME.github.io/csv-merger`

### Badges in README
Add badges to your README for a professional look:
```markdown
[![GitHub release](https://img.shields.io/github/v/release/YOUR_USERNAME/csv-merger)](https://github.com/YOUR_USERNAME/csv-merger/releases)
[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/csv-merger)](https://github.com/YOUR_USERNAME/csv-merger)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
```

## Security & Maintenance Tips

- **Never commit sensitive data** (API keys, passwords) — use environment variables
- **Keep dependencies updated**: Periodically run `pip list --outdated`
- **Review PR security**: Check new dependencies for vulnerabilities
- **Back up releases**: GitHub stores releases indefinitely, but back up locally too

## Troubleshooting

### "fatal: not a git repository"
```bash
cd path/to/PythonProject
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### "Permission denied (publickey)"
Use HTTPS instead of SSH, or set up SSH keys:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/csv-merger.git
```

### Files not appearing on GitHub
Make sure they're **not in `.gitignore`**:
```bash
git check-ignore -v filename.py
```

---

**You're all set!** Your CSV Merger is now open-source and public. Share the link! 🎉
