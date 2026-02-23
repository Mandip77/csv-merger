# CSV Merger

A modern, feature-rich desktop application for merging, transforming, and exporting multiple CSV files with ease.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Features

✨ **Core Capabilities**
- 📁 **Multi-file selection** — Select CSV files from any folder, with recursive directory support
- 🔀 **Flexible merge modes** — Concatenate or join files on common columns
- 🎯 **Column management** — Select, rename, and map columns during merge
- 🔍 **Advanced filtering** — Apply row filters by column conditions before merge
- 📊 **Data cleaning** — Handle missing data (drop, forward-fill, interpolate), remove duplicates
- 📈 **Preview & statistics** — View merge preview before committing, inspect data types and stats
- 💾 **Multiple export formats** — Save to CSV, TSV, Excel (XLSX), or JSON
- ⚙️ **Batch mode** — Save and reuse merge configurations for repetitive tasks
- 🎨 **Modern UI** — Professional desktop interface with optional dark theme support via ttkbootstrap

## Quick Start

### Download Installer
- **Windows**: [CSV_Merger_Installer.exe](https://github.com/Mandip77/csv-merger/releases) — Download and run the installer

### Run from Source
Requires Python 3.8+

```bash
# Clone the repo
git clone https://github.com/Mandip77/csv-merger
cd csv-merger/practise/csvmerger

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python mergecsvfiles_advanced.py
```

## Installation From Source

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps
1. Clone this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python mergecsvfiles_advanced.py
   ```

## Usage

### GUI Application (Recommended)
Launch the app and follow the tabbed interface:

1. **File Selection** — Choose CSV files from your system
2. **Column Management** — Select and map columns
3. **Filtering** — Define row conditions to filter before merge
4. **Merge Options** — Set merge type, duplicate handling, sort order
5. **Preview** — Review data before export
6. **Export** — Save to your preferred format

### Command-Line Tool
For simple merges via CLI:
```bash
python mergecsvfiles.py --help
```

## Project Structure

```
csv-merger/
├── practise/
│   └── csvmerger/
│       ├── mergecsvfiles_advanced.py    # Main GUI app
│       ├── mergecsvfiles.py             # CLI tool
│       ├── mergecsvfiles_gui.py         # Alternative GUI
│       ├── requirements.txt             # Python dependencies
│       ├── build_scripts/               # PyInstaller build scripts
│       │   ├── build_windows.bat
│       │   ├── build_mac.sh
│       │   ├── build_linux.sh
│       │   └── run_inno.ps1            # Windows installer helper
│       ├── installer/                   # Inno Setup installer config
│       │   └── csv_merger_installer.iss
│       └── dist/                        # Packaged distributions (gitignored)
├── README.md                            # This file
├── LICENSE                              # MIT License
└── CONTRIBUTING.md                      # Contribution guidelines
```

## Dependencies

Core libraries:
- **pandas** — Data manipulation and analysis
- **chardet** — Automatic encoding detection
- **tkinter** — GUI framework (included with Python)

Optional:
- **ttkbootstrap** — Modern theme support (auto-detected at launch)
- **openpyxl** — Excel export support

See `requirements.txt` for full list.

## Building Installers

### Windows
Requires Inno Setup 6+ (https://jrsoftware.org/isinfo.php)

```bash
cd practise/csvmerger
python -m PyInstaller --noconfirm --windowed --clean --name "CSV Merger" \
  mergecsvfiles_advanced.py --add-data "settings.json;."

# Then run the installer compiler
powershell -ExecutionPolicy Bypass -File .\build_scripts\run_inno.ps1 \
  -ISCCPath "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
```

Output: `installer/Output/CSV_Merger_Installer.exe`

### macOS & Linux
See [PACKAGING_GUIDE.md](practise/csvmerger/README_PACKAGING.md) for detailed cross-platform build instructions.

## Configuration

On first launch, the app auto-creates:
- `settings.json` — UI preferences and theme selection
- `batch_configs.json` — Saved merge configurations
- `recent_merges.json` — Recent file history

These files persist in the app directory.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Suggesting features
- Submitting pull requests
- Code style and testing

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

## Roadmap

- [ ] Auto-update functionality
- [ ] Python 3.13+ support verification
- [ ] Internationalization (i18n) support
- [ ] Cloud storage integration (Google Drive, OneDrive)
- [ ] Advanced data validation rules
- [ ] Plugin system for custom transformations

## Support

- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/Mandip77/csv-merger/issues)
- **Discussions**: Ask questions in [GitHub Discussions](https://github.com/Mandip77/csv-merger/discussions)

## Acknowledgments

Built with ❤️ using tkinter, pandas, and the Python community.

---

**Ready to merge your CSVs?** Download the installer or run from source today! 🚀
