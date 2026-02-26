#!/usr/bin/env bash
set -e
APP_NAME="CSV Merger"
SRC="mergecsvfiles_advanced.py"
TAR_NAME="CSV_Merger_Installer_Linux.tar.gz"

echo "Building Linux executable with PyInstaller..."
pyinstaller --noconfirm --windowed --clean --name "$APP_NAME" "$SRC" --add-data "batch_configs.json:." --add-data "settings.json:." --add-data "recent_merges.json:."

echo "Creating Linux Installation Package..."
# Create a staging directory
mkdir -p "dist/linux_staging/$APP_NAME"
cp -R "dist/$APP_NAME/"* "dist/linux_staging/$APP_NAME/"

# Create desktop file
cat << 'EOF' > "dist/linux_staging/$APP_NAME.desktop"
[Desktop Entry]
Type=Application
Name=CSV Merger
Comment=Tool for merging CSV files
Exec=/opt/CSV Merger/CSV Merger
Icon=/opt/CSV Merger/_internal/icon.png
Terminal=false
Categories=Utility;
EOF

# Create install script
cat << 'EOF' > "dist/linux_staging/install.sh"
#!/usr/bin/env bash

# Require root
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root (e.g., sudo ./install.sh)"
  exit 1
fi

APP_DIR="/opt/CSV Merger"
DESKTOP_ENTRY_DIR="/usr/share/applications"

echo "Installing CSV Merger to $APP_DIR..."
# Remove old install if exists
rm -rf "$APP_DIR"
# Copy app
cp -R "CSV Merger" "$APP_DIR"
# Set permissions
chmod -R 755 "$APP_DIR"
chmod +x "$APP_DIR/CSV Merger"

echo "Installing desktop entry..."
cp "CSV Merger.desktop" "$DESKTOP_ENTRY_DIR/"
chmod 644 "$DESKTOP_ENTRY_DIR/CSV Merger.desktop"

echo "Installation complete! You can now launch CSV Merger from your applications menu."
EOF
chmod +x "dist/linux_staging/install.sh"

# Create the tar.gz archive
cd dist/linux_staging
tar -czvf "../$TAR_NAME" *
cd ../..

# Clean up staging directory
rm -rf "dist/linux_staging"

echo "Linux Installer package successfully created at dist/$TAR_NAME"
