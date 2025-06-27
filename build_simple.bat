@echo off
REM Simple build script without Tesseract auto-detection

if "%1"=="" (
    cmd /k "%~f0" RUN
    exit /b
)

setlocal
title PoE Craft Helper - Simple Build
cd /d "%~dp0"

echo =========================================
echo    PoE Craft Helper - Simple Build
echo =========================================
echo.
echo NOTE: This script assumes Tesseract is already installed
echo and available in your system PATH.
echo.

REM Check Python
echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo.

REM Install dependencies
echo Installing dependencies...
pip install pyinstaller opencv-python pytesseract Pillow numpy requests psutil
echo.

REM Prepare directories
echo Preparing directories...
if not exist "data" mkdir "data"
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo.

REM Check launcher.py
if not exist "launcher.py" (
    echo ERROR: launcher.py not found!
    pause
    exit /b 1
)

REM Build
echo Building executable...
python -m PyInstaller --onefile --windowed --name "PoE_Craft_Helper" launcher.py
if errorlevel 1 (
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build complete! Check the dist folder.
pause
exit /b 0