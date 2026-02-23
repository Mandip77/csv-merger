@echo off
rem Build Windows executable and installer using PyInstaller and Inno Setup
setlocal enabledelayedexpansion

rem Change these values as needed
set APP_NAME=CSV Merger
set SRC=mergecsvfiles_advanced.py
set ICON=

echo Building %APP_NAME% with PyInstaller...
pyinstaller --noconfirm --windowed --clean --name "%APP_NAME%" %SRC% \
    --add-data "batch_configs.json;." --add-data "settings.json;." --add-data "recent_merges.json;." 

if errorlevel 1 (
    echo PyInstaller build failed.
    pause
    exit /b 1
)

echo Building Inno Setup installer (if Inno Setup is installed)...
rem Create installer using Inno Setup Command-Line Compiler (ISCC)
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" (
    "%ProgramFiles%\Inno Setup 6\ISCC.exe" ..\installer\csv_merger_installer.iss
    echo Inno Setup finished.
) else (
    echo Inno Setup not found in Program Files. Please run Inno Setup manually with installer\csv_merger_installer.iss
)

echo Build finished.
pause
