#!/usr/bin/env bash
set -e
APP_NAME="CSV Merger"
SRC="mergecsvfiles_advanced.py"

echo "Building Linux executable with PyInstaller..."
pyinstaller --noconfirm --windowed --clean --name "$APP_NAME" "$SRC" --add-data "batch_configs.json:." --add-data "settings.json:." --add-data "recent_merges.json:."

echo "To produce an AppImage, install linuxdeploy or appimagetool and follow their docs."
