# Portfolio Page Customization Guide

The `portfolio_page.html` file is a ready-to-use landing page for CSV Merger that you can add to your portfolio website.

## Quick Setup

### Option 1: Host on GitHub Pages (Free)
1. Create a `docs/` folder in your repository root
2. Copy `portfolio_page.html` → `docs/index.html`
3. Commit and push:
   ```bash
   git add docs/index.html
   git commit -m "Add portfolio landing page"
   git push origin main
   ```
4. Enable GitHub Pages:
   - Go to repo **Settings** → **Pages**
   - Source: `/docs` folder
   - Your site will be at: `https://yourusername.github.io/csv-merger`

### Option 2: Add to Your Existing Portfolio
1. Copy `portfolio_page.html` into your portfolio website's project folder
2. Update the filename to match your site structure (e.g., `projects/csv-merger.html`)
3. Update navigation links to match your site

### Option 3: Deploy to a Web Server
- Upload `portfolio_page.html` to your hosting (Netlify, Vercel, etc.)
- Rename to `index.html` if you want it as the main page

## Customization

### Update Your Information
Search and replace these placeholders:

| Placeholder | Replace With |
|----------|----------|
| `YOUR_USERNAME` | Your GitHub username (5 places) |
| `yourportfolio.com` | Your portfolio website URL |
| `Your Portfolio` | Link text for your portfolio|
| `v1.0.0` | Current app version |

### Change Colors
Modify the gradient colors in `<style>`:
```css
/* Current: Purple gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Try: Blue to cyan */
background: linear-gradient(135deg, #0066ff 0%, #00d4ff 100%);

/* Try: Green to teal */
background: linear-gradient(135deg, #00b894 0%, #00d2d3 100%);
```

### Add Screenshots
1. Take screenshots of your app
2. Save them locally (e.g., `screenshots/app-main.png`)
3. Add to gallery section (around line 400):
```html
<div class="gallery-item">
    <img src="screenshots/main-window.png" alt="Main window" style="width: 100%; border-radius: 6px; margin-bottom: 10px;">
    <h3>Main Interface</h3>
    <p>Intuitive multi-tab interface for CSV merging and transformation.</p>
</div>
```

### Update Feature List
Edit the features section (around line 280):
```html
<div class="feature">
    <div class="feature-icon">🆕</div>
    <h3>Your New Feature</h3>
    <p>Description of your new feature.</p>
</div>
```

### Change Download Links
Update the download button to point to your latest release:
```html
<a href="https://github.com/YOUR_USERNAME/csv-merger/releases/download/v1.0.0/CSV_Merger_Installer.exe" class="btn btn-primary">
    📥 Download Windows Installer
</a>
```

### Add More Download Options
Add buttons for macOS and Linux:
```html
<div class="download-buttons">
    <a href="..." class="btn btn-primary">📥 Windows Installer</a>
    <a href="..." class="btn btn-primary">🍎 macOS App</a>
    <a href="..." class="btn btn-primary">🐧 Linux AppImage</a>
    <a href="..." class="btn btn-secondary">💻 Source Code</a>
</div>
```

## SEO & Metadata

Update the page for better search visibility:

### Meta Tags
```html
<meta name="description" content="Download CSV Merger - a modern desktop app for merging and transforming CSV files with advanced filtering and batch processing.">
<meta name="keywords" content="csv, merge, desktop app, data processing, python">
<meta name="author" content="Your Name">
```

### Open Graph (Social Media Previews)
```html
<meta property="og:title" content="CSV Merger - Desktop Application">
<meta property="og:description" content="Modern desktop app for merging and transforming CSV files">
<meta property="og:image" content="https://yoursite.com/screenshot.png">
<meta property="og:url" content="https://yoursite.com/csv-merger">
```

## Analytics

Add Google Analytics (optional):
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_GA_ID');
</script>
```

Insert before `</head>` tag.

## Mobile Optimization

The page is already responsive! Test on mobile:
- Open in Chrome DevTools (F12)
- Click device toggle (mobile icon)
- Test on different screen sizes

## Testing

Before publishing:
1. Open in different browsers (Chrome, Firefox, Safari, Edge)
2. Test all links work (especially Download and GitHub links)
3. Verify on mobile devices
4. Check that opening the app works from links

## Common Issues

### Links are broken
- Ensure GitHub username is correct
- Ensure release tag matches in URL (e.g., `v1.0.0`)
- Test links directly: https://github.com/YOUR_USERNAME/csv-merger

### Page looks wrong
- Clear browser cache (Ctrl+Shift+Del)
- Try a different browser
- Check browser console for errors (F12)

### Visitors can't download
- Verify installer is uploaded to GitHub Releases
- Check file permissions on host
- Test download link in incognito mode

## Next Steps

1. ✅ Customize the HTML with your info
2. ✅ Add screenshots from your app
3. ✅ Test all links work
4. ✅ Deploy to GitHub Pages or your site
5. ✅ Share on social media!

---

Need help? Open an issue on GitHub! 🚀
