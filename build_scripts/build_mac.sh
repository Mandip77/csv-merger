#!/usr/bin/env bash
set -e
APP_NAME="CSV Merger"
SRC="mergecsvfiles_advanced.py"
DMG_NAME="CSV_Merger_Installer.dmg"

echo "Building macOS app with PyInstaller..."
pyinstaller --noconfirm --windowed --clean --name "$APP_NAME" "$SRC" --add-data "batch_configs.json:." --add-data "settings.json:." --add-data "recent_merges.json:."

echo "Creating DMG Installer..."
# Create a staging directory
mkdir -p "dist/dmg_staging"
# Copy the app to the staging directory
cp -R "dist/$APP_NAME.app" "dist/dmg_staging/"
# Create a symlink to Applications
ln -s /Applications "dist/dmg_staging/Applications"

# Create the DMG
hdiutil create -volname "$APP_NAME" -srcfolder "dist/dmg_staging" -ov -format UDZO "dist/$DMG_NAME"

# Clean up staging directory
rm -rf "dist/dmg_staging"

echo "DMG successfully created at dist/$DMG_NAME"
