# Publishing to GitHub — Step-by-Step Instructions

Your CSV Merger code is ready! Follow these steps to publish to GitHub.

## Step 1: Create a GitHub Repository (Web Browser)

1. **Go to**: https://github.com/new
2. **Sign in** with your GitHub account (Mandip77)

3. **Fill in repository details:**
   ```
   Repository name: csv-merger
   Description: A modern desktop app for merging, transforming, and exporting CSV files
   Public: ✓ (selected)
   Initialize: ☐ (LEAVE UNCHECKED - we'll push existing code)
   ```

4. **Click "Create repository"**

5. **You'll see a page with commands** — copy the URL that looks like:
   ```
   https://github.com/Mandip77/csv-merger.git
   ```
   (This is your repository URL)

---

## Step 2: Connect Local Code to GitHub (PowerShell)

Run these commands in PowerShell:

```powershell
# Navigate to project root
cd C:\Users\mandi\Desktop\Develop\PythonProject

# Add GitHub as remote
git remote add origin https://github.com/Mandip77/csv-merger.git

# Rename main branch to main (GitHub standard)
git branch -M main

# Push code to GitHub
git push -u origin main
```

**When prompted:**
- **Username**: `Mandip77`
- **Password**: Use a GitHub Personal Access Token (see below)

### Getting a GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. **Fill in:**
   - Token name: `CSV Merger Release`
   - Expiration: 90 days (or longer)
   - Scopes: Check **`repo`** (full control of private/public repos)
4. Click **"Generate token"**
5. **Copy the token** (appears once)
6. Use this token as your **password** when git prompts

---

## Step 3: Verify on GitHub

1. Go to: https://github.com/Mandip77/csv-merger
2. Verify you see:
   - ✅ All your files
   - ✅ README.md displayed
   - ✅ LICENSE visible
   - ✅ Green "Code" button

---

## Step 4: Create GitHub Release

1. **Go to**: https://github.com/Mandip77/csv-merger/releases

2. **Click "Draft a new release"** (or "Create a new release")

3. **Fill in release information:**
   ```
   Tag version: v1.0.0
   
   Release title: 
   CSV Merger v1.0.0 - Initial Release
   
   Description:
   # CSV Merger v1.0.0 🎉
   
   The open-source desktop app for merging and transforming CSV files is now available!
   
   ## Key Features ✨
   - 📁 Multi-file CSV merging (concatenate or join)
   - 🎯 Column selection and mapping
   - 🔍 Advanced filtering
   - 📊 Data preview before export
   - 💾 Multiple export formats (CSV, TSV, XLSX, JSON)
   - ⚙️ Batch processing with saved configurations
   - 🎨 Modern desktop UI with optional dark theme
   
   ## Download 📥
   - **Windows**: Download `CSV_Merger_Installer.exe` below
   - **Source Code**: Clone from this repo
   
   ## What's Included
   - Standalone Windows installer (one-click install)
   - Portable executable (no installation needed)
   - Full source code (Python)
   - Comprehensive user guides and documentation
   
   ## Getting Started
   1. Download `CSV_Merger_Installer.exe`
   2. Run installer
   3. Launch from Start Menu
   
   Or clone and run from source:
   ```bash
   git clone https://github.com/Mandip77/csv-merger
   cd csv-merger/practise/csvmerger
   pip install -r requirements.txt
   python mergecsvfiles_advanced.py
   ```
   
   ## Documentation 📚
   - **User Guide**: Read USER_GUIDE.md for detailed how-to
   - **FAQ**: Check FAQ.md for common questions
   - **Contributing**: See CONTRIBUTING.md to help improve
   
   ## System Requirements
   - Windows 10+ (macOS/Linux compatible with source)
   - Python 3.8+ (for source installation)
   - 2GB RAM minimum
   
   ## License
   MIT License - Free to use and modify
   
   ## Support & Feedback
   - 🐛 **Report bugs**: [GitHub Issues](https://github.com/Mandip77/csv-merger/issues)
   - 💬 **Ask questions**: [GitHub Discussions](https://github.com/Mandip77/csv-merger/discussions)
   - ⭐ **Star the repo** if you find it useful!
   
   ---
   
   Built with ❤️ using Python, pandas, and tkinter.
   ```

4. **Upload the installer file:**
   - Click **"Attach binaries"** or drag-drop zone
   - Find and select: `practise\csvmerger\installer\Output\CSV_Merger_Installer.exe`
   - Attach!

5. **Click "Publish release"**

---

## Step 5: Verify Release

1. Go to: https://github.com/Mandip77/csv-merger/releases

2. You should see:
   - ✅ v1.0.0 listed
   - ✅ Release description visible
   - ✅ Download button for `CSV_Merger_Installer.exe`
   - ✅ Source code downloads (auto-generated)

3. **Test the download:**
   - Click the installer file
   - Verify it downloads successfully

---

## Step 6: Configure Repository Settings

### Add Repository Topics

1. Go to: https://github.com/Mandip77/csv-merger
2. Click the **gear icon** next to "About" (right side)
3. Add topics (comma-separated or one-by-one):
   ```
   csv
   data-processing
   python
   desktop-app
   gui
   open-source
   ```
4. Click "Save"

### Enable Discussions

1. Go to **Settings** (top right)
2. Under **Features**, check **Discussions**
3. Click "Save"
4. Users can now ask questions in **Discussions** tab

### Add Homepage

1. In the same **About** section
2. Set homepage URL: `https://man-dip.dev`

---

## Step 7: Share Your Release! 🚀

### Copy release URL:
```
https://github.com/Mandip77/csv-merger
```

### Share on:
- **LinkedIn**: "Excited to share CSV Merger, an open-source desktop app for CSV data transformation! Built with Python & tkinter. Download: [link]"
- **Twitter**: "Just released CSV Merger - modern desktop app for merging CSVs with advanced filtering & batch processing. Open-source & free! Check it out 👇 [link]"
- **Reddit**: Post to r/Python, r/programming, r/opensource
- **Dev.to**: Write a quick blog post about the release
- **Your portfolio**: Add link to man-dip.dev

---

## Troubleshooting GitHub Push

### "fatal: not a git repository"
```powershell
cd C:\Users\mandi\Desktop\Develop\PythonProject
git status  # Should show master branch
```

### "Permission denied" or "Authentication failed"
```
1. Use Personal Access Token (not password)
2. Go to https://github.com/settings/tokens
3. Create new token with 'repo' scope
4. Use token as password when prompted
```

### "The origin already exists"
```powershell
# If you get this error, the remote already exists
# Remove and re-add:
git remote remove origin
git remote add origin https://github.com/Mandip77/csv-merger.git
git push -u origin main
```

### Repository is empty on GitHub
```powershell
# Make sure code was pushed:
git push -u origin main

# Then check:
git log --oneline  # Should show commits

# Try pushing again with verbose:
git push -v origin main
```

---

## Next Steps After Publishing

✅ **What you've accomplished:**
- GitHub repository created
- Code pushed
- Release created with installer
- Ready to download and use

📌 **What's next:**
1. Share release link with friends/colleagues
2. Create release announcement email
3. Add to man-dip.dev portfolio
4. Monitor GitHub Issues for bug reports
5. Respond to Discussions and questions
6. Consider adding CI/CD workflows

---

## Quick Reference

| Task | URL |
|------|-----|
| View Repository | https://github.com/Mandip77/csv-merger |
| View Releases | https://github.com/Mandip77/csv-merger/releases |
| Create Issue | https://github.com/Mandip77/csv-merger/issues/new |
| View Discussions | https://github.com/Mandip77/csv-merger/discussions |
| Settings | https://github.com/Mandip77/csv-merger/settings |

---

**All done!** Your CSV Merger is now published on GitHub! 🎉

Next, integrate it into your portfolio at man-dip.dev with the links above.
