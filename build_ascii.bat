@echo off
title PoE Craft Helper Build
echo =========================================
echo    PoE Craft Helper - Build Script
echo =========================================
echo.

echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8 or later
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install pyinstaller opencv-python pytesseract Pillow numpy requests psutil

echo.
echo Checking for launcher.py...
if not exist launcher.py (
    echo ERROR: launcher.py not found!
    pause
    exit /b 1
)

echo.
echo Building executable...
python -m PyInstaller --onefile --windowed --name PoE_Craft_Helper launcher.py

echo.
echo Build complete!
pause