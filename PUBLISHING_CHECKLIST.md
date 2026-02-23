# CSV Merger — Publishing Checklist

Quick reference checklist for publishing your app to GitHub and portfolio.

## Pre-Flight Check

- [ ] Installer created: `installer/Output/CSV_Merger_Installer.exe`
- [ ] Portable EXE created: `dist/CSV Merger/CSV Merger.exe`
- [ ] Code clean and organized
- [ ] README.md updated with correct info
- [ ] LICENSE file in place
- [ ] .gitignore configured
- [ ] All documentation files present

## GitHub Publishing (40 minutes)

### Setup (5 min)
- [ ] GitHub account created/verified
- [ ] GitHub username ready
- [ ] Personal access token generated (https://github.com/settings/tokens)

### Push Code (10 min)
- [ ] `git init` executed
- [ ] `git add .` completed
- [ ] `git commit -m "Initial commit..."` done
- [ ] `git remote add origin` set correctly
- [ ] `git push origin main` successful
- [ ] Code visible on GitHub.com

### Create Release (10 min)
- [ ] Navigated to GitHub Releases
- [ ] Created new release (tag: `v1.0.0`)
- [ ] Added release description
- [ ] Uploaded `CSV_Merger_Installer.exe`
- [ ] Clicked "Publish release"
- [ ] Download link tested and works

### Manage Repository (15 min)
- [ ] Added topics: csv, data-processing, python, desktop-app
- [ ] Added description: "Modern desktop app for merging CSV files"
- [ ] Enabled Discussions (Settings > Features)
- [ ] Enabled GitHub Pages (Settings > Pages) — optional
- [ ] Added GitHub link to portfolio

## Portfolio Page (25 minutes)

### Customize HTML (10 min)
- [ ] `portfolio_page.html` opened in text editor
- [ ] `YOUR_USERNAME` replaced with actual GitHub username (5 places)
- [ ] `yourportfolio.com` replaced with portfolio URL
- [ ] Release version correct (v1.0.0)
- [ ] Download link updated
- [ ] Colors customized (optional)
- [ ] Features reviewed and accurate

### Deploy (15 min)

**Option A — GitHub Pages:**
- [ ] Created `docs/` folder
- [ ] Copied `portfolio_page.html` → `docs/index.html`
- [ ] `git add docs/index.html` committed
- [ ] `git push origin main` successful
- [ ] GitHub Pages enabled (Settings > Pages > `/docs`)
- [ ] Site accessible at `yourusername.github.io/csv-merger`

**Option B — Personal Website:**
- [ ] `portfolio_page.html` copied to portfolio folder
- [ ] HTML updated with custom paths
- [ ] Uploaded to web host
- [ ] Links tested and working
- [ ] Mobile view tested

## Marketing & Sharing

- [ ] LinkedIn post created with project link
- [ ] GitHub shared with network
- [ ] Twitter post with project link
- [ ] Reddit post to relevant subreddits (r/Python, etc.)
- [ ] Personal portfolio updated with project
- [ ] Portfolio page linked from main portfolio

## Ongoing Maintenance

- [ ] GitHub watching enabled (notifications)
- [ ] Issues template added (optional)
- [ ] PR template added (optional)
- [ ] README pinned or featured
- [ ] First issue or PR acknowledged
- [ ] Contributors thanked

## Success Milestones

- [ ] **5 stars** ⭐ — Share with friends
- [ ] **10 stars** ⭐⭐ — Consider promoting more
- [ ] **25 stars** ⭐⭐⭐ — Great open-source project!
- [ ] **50 stars** ⭐⭐⭐⭐ — Trending potential!
- [ ] **First PR** — Welcome contribution!

---

## Troubleshooting During Publishing

### "Git not found"
```bash
# Install Git from https://git-scm.com
# (Windows: choose "Use Git Bash")
```

### "Permission denied (publickey)"
```bash
# Use HTTPS instead of SSH
git remote set-url origin https://github.com/YOUR_USERNAME/csv-merger.git
```

### "fatal: not a git repository"
```bash
git init
git config user.name "Your Name"
git config user.email "your@email.com"
```

### Installer won't download from GitHub
- Check file size is reasonable
- Ensure `.exe` file actually exists
- Test download in incognito/private mode

### Portfolio page looks broken
- Clear browser cache (Ctrl+Shift+Del)
- Check all image/link paths
- Test in different browser
- Open browser console (F12) for errors

---

## Time Estimates

| Task | Time |
|------|------|
| Push to GitHub | 10 min |
| Create release | 5 min |
| Customize portfolio page | 10 min |
| Deploy portfolio page | 10 min |
| Share on social media | 15 min |
| **Total** | **~50 minutes** |

---

## Quick Commands Reference

```bash
# Initialize and push code
git init
git add .
git commit -m "Initial commit: CSV Merger v1.0.0"
git remote add origin https://github.com/YOUR_USERNAME/csv-merger.git
git branch -M main
git push -u origin main

# Check git status
git status

# Update after changes
git add .
git commit -m "Description of changes"
git push origin main
```

---

## Important Links to Have Ready

- GitHub repo: `https://github.com/YOUR_USERNAME/csv-merger`
- Releases page: `https://github.com/YOUR_USERNAME/csv-merger/releases`
- Portfolio page (GitHub Pages): `https://YOUR_USERNAME.github.io/csv-merger`
- Your portfolio: `yourportfolio.com`

---

**Good luck pushing CSV Merger to the world!** 🚀

Print this checklist, check items as you go, and celebrate when you're done! 🎉
