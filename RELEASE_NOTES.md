# CSV Merger v1.0.0 - Release Notes

**Release Date**: February 23, 2026

## 🎉 Initial Open-Source Release

Proud to announce the open-source release of CSV Merger, a modern desktop application for merging and transforming CSV files!

## ✨ Features

### Core Functionality
- ✅ Multi-file CSV merging (concatenate or join modes)
- ✅ Intelligent column selection and mapping
- ✅ Advanced row filtering with custom conditions
- ✅ Missing data handling (drop, forward-fill, interpolate)
- ✅ Duplicate removal (rows and columns with multiple strategies)
- ✅ Data preview and statistics before export
- ✅ Multiple export formats (CSV, TSV, Excel, JSON)
- ✅ Batch configuration save and reuse

### User Experience
- ✅ Modern desktop GUI with tkinter and ttk
- ✅ Optional dark theme support via ttkbootstrap
- ✅ Keyboard shortcuts for enhanced productivity
- ✅ Tooltips and help documentation
- ✅ Onboarding guide for first-time users
- ✅ File browser with Treeview and context menus
- ✅ Status bar and logging for transparency
- ✅ Settings persistence across sessions

### Technical
- ✅ Automatic file encoding detection (chardet)
- ✅ Cross-platform compatibility (Windows, macOS, Linux)
- ✅ PyInstaller packaging for standalone distribution
- ✅ Inno Setup installer for Windows (one-click install)
- ✅ Non-blocking merge operations via threading

## 🐛 Known Limitations

- macOS and Linux distributions not yet available (scripts provided for building)
- Code signing not yet implemented (add for production releases)
- Auto-update functionality not yet implemented

## 📦 Installation

### Windows
Download and run `CSV_Merger_Installer.exe` from the releases page.

### From Source (All Platforms)
```bash
git clone https://github.com/yourusername/csv-merger
cd csv-merger/practise/csvmerger
pip install -r requirements.txt
python mergecsvfiles_advanced.py
```

## 🔧 Dependencies

- Python 3.8 or higher
- pandas
- chardet
- tkinter (included with Python)
- openpyxl (for Excel export)
- Optional: ttkbootstrap (modern themes)

## 📝 What's Next?

### In Development
- Auto-update mechanism
- Plugin system for custom transformations
- Cloud storage integration (Google Drive, OneDrive)
- Internationalization (i18n) support
- Advanced data validation rules
- More export format options (Parquet, SQLite)

### Community Contributions Welcome
See [CONTRIBUTING.md](CONTRIBUTING.md) for how to report bugs, suggest features, or submit code improvements.

## 🙏 Thank You

This project was built with care using Python, pandas, tkinter, and the amazing open-source community. Special thanks to:
- The pandas team for data manipulation
- PyInstaller for making distribution simple
- Inno Setup for Windows installer support

## 📄 License

Licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🚀 How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📞 Support

- **Bugs**: Report on [GitHub Issues](https://github.com/yourusername/csv-merger/issues)
- **Questions**: Use [GitHub Discussions](https://github.com/yourusername/csv-merger/discussions)
- **Feature Requests**: Open an issue with `[FEATURE]` prefix

---

**Happy merging!** 📊 If you find CSV Merger useful, please consider starring the repository to show your support. ⭐
