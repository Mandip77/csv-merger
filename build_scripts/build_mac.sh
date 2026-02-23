#!/usr/bin/env bash
set -e
APP_NAME="CSV Merger"
SRC="mergecsvfiles_advanced.py"

echo "Building macOS app with PyInstaller..."
pyinstaller --noconfirm --windowed --clean --name "$APP_NAME" "$SRC" --add-data "batch_configs.json:." --add-data "settings.json:." --add-data "recent_merges.json:."

echo "Note: To create a DMG, use create-dmg or macdeployqt after building the .app."
echo "Example (install create-dmg via npm): create-dmg --overwrite dist/$APP_NAME.app"
