@echo off
if "%1"=="" (
    cmd /k "%~f0" RUN
    exit /b
)

title PoE Craft Helper - Direct Build
cd /d "%~dp0"

echo PoE Craft Helper - Direct Build
echo ===============================
echo.

echo Installing dependencies...
pip install pyinstaller opencv-python pytesseract Pillow numpy requests psutil
echo.

echo Building with PyInstaller...
python -m PyInstaller --onefile --windowed --add-data "data;data" --hidden-import cv2 --hidden-import numpy --hidden-import PIL --hidden-import pytesseract --hidden-import psutil --hidden-import tkinter --hidden-import requests --name PoE_Craft_Helper launcher.py

echo.
if exist "dist\PoE_Craft_Helper.exe" (
    echo Build successful!
    echo Executable: dist\PoE_Craft_Helper.exe
) else (
    echo Build failed!
)

pause