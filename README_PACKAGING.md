CSV Merger — Packaging & Installer Guide
======================================

This document outlines steps to package `mergecsvfiles_advanced.py` into standalone desktop applications and installers for Windows, macOS, and Linux.

Prerequisites
- Python 3.8+ installed
- Install project dependencies in a virtualenv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Windows (recommended flow)
1. Install `Inno Setup` (https://jrsoftware.org/isinfo.php) to build an installer.
2. From the project `csvmerger` folder run:

```powershell
cd practise\csvmerger\build_scripts
..\..\venv\Scripts\Activate.ps1   # or activate your venv
build_windows.bat
```

If Inno Setup is installed in a non-standard location, you can use the helper script:

```powershell
cd practise\csvmerger\build_scripts
.\run_inno.ps1 -ISCCPath 'C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe'
```

Or allow the script to auto-detect ISCC (if installed in a standard path):

```powershell
.\run_inno.ps1
```

This script runs `pyinstaller` to produce `dist\CSV Merger.exe`. If Inno Setup is installed it will call `ISCC.exe` to build the installer from `installer\csv_merger_installer.iss`.

macOS
- Use PyInstaller to create a .app bundle (`build_mac.sh` uses PyInstaller). To make a DMG, use `create-dmg` or similar tools.

Linux
- Use PyInstaller to create a bundled executable and optionally produce an AppImage using `linuxdeploy` or `appimagetool`.

Notes / Next steps
- Code signing: Acquire a code-signing certificate and add signing steps (signtool for Windows, codesign for macOS).
- Auto-update: Consider implementing an auto-update channel or using services like Sparkle (macOS) or an update server.
- Testing: Build on target OSes (use CI runners or local VMs) to verify packaging.

If you want, I can: 
- Run the PyInstaller build here for Windows now and produce a test `dist` executable, or
- Generate an automated GitHub Actions workflow that builds artifacts on release.
