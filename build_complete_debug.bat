@echo off
setlocal enabledelayedexpansion
title PoE Craft Helper - Complete Build System (DEBUG)
echo =========================================
echo    PoE Craft Helper - Complete Build (DEBUG MODE)
echo =========================================
echo.
echo Debug: Current directory is %cd%
echo Debug: Script location is %~dp0
echo.

REM Change to script directory
cd /d "%~dp0"
echo Debug: Changed to directory %cd%
echo.

REM Check Python installation
echo Debug: Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or later
    pause
    exit /b 1
)
echo Debug: Python check passed
echo.

echo [0/7] Checking for Tesseract OCR...
echo ------------------------------------
where tesseract
if %errorlevel% neq 0 (
    echo Debug: Tesseract not found in PATH. Checking common locations...
    
    REM Check common Tesseract installation paths
    set "TESSERACT_PATH="
    if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
        echo Debug: Found at C:\Program Files\Tesseract-OCR
        set "TESSERACT_PATH=C:\Program Files\Tesseract-OCR"
    ) else if exist "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe" (
        echo Debug: Found at C:\Program Files (x86)\Tesseract-OCR
        set "TESSERACT_PATH=C:\Program Files (x86)\Tesseract-OCR"
    ) else if exist "%LOCALAPPDATA%\Tesseract-OCR\tesseract.exe" (
        echo Debug: Found at %LOCALAPPDATA%\Tesseract-OCR
        set "TESSERACT_PATH=%LOCALAPPDATA%\Tesseract-OCR"
    ) else if exist "%PROGRAMFILES%\Tesseract-OCR\tesseract.exe" (
        echo Debug: Found at %PROGRAMFILES%\Tesseract-OCR
        set "TESSERACT_PATH=%PROGRAMFILES%\Tesseract-OCR"
    )
    
    if defined TESSERACT_PATH (
        echo Found Tesseract at: !TESSERACT_PATH!
        echo Adding to PATH for this session...
        set "PATH=!TESSERACT_PATH!;!PATH!"
        
        REM Verify it works
        "!TESSERACT_PATH!\tesseract.exe" --version
        if !errorlevel! equ 0 (
            echo Tesseract successfully added to PATH!
            set "TESSERACT_CMD=!TESSERACT_PATH!\tesseract.exe"
        ) else (
            echo ERROR: Failed to run Tesseract from !TESSERACT_PATH!
            echo Please install Tesseract OCR from:
            echo https://github.com/UB-Mannheim/tesseract/wiki
            pause
            exit /b 1
        )
    ) else (
        echo ERROR: Tesseract OCR is not installed!
        echo.
        echo Please install Tesseract OCR from:
        echo https://github.com/UB-Mannheim/tesseract/wiki
        echo.
        echo After installation, either:
        echo 1. Add Tesseract to your system PATH, or
        echo 2. Install it in one of these locations:
        echo    - C:\Program Files\Tesseract-OCR
        echo    - C:\Program Files (x86)\Tesseract-OCR
        echo    - %LOCALAPPDATA%\Tesseract-OCR
        pause
        exit /b 1
    )
) else (
    echo Tesseract found in PATH!
    tesseract --version | findstr /i "tesseract"
)

echo.
echo Press any key to continue with build...
pause

echo.
echo [1/7] Running pre-build checks...
echo ---------------------------------
echo Debug: Running pre_build_check.py
if exist "pre_build_check.py" (
    python pre_build_check.py
    echo Debug: pre_build_check.py exit code: %errorlevel%
) else (
    echo Debug: pre_build_check.py not found, skipping...
)

echo.
echo [2/7] Installing dependencies...
echo --------------------------------
echo Debug: Running pip install...
pip install pyinstaller opencv-python pytesseract Pillow numpy requests psutil
echo Debug: pip install exit code: %errorlevel%

echo.
echo [3/7] Creating data directory...
echo --------------------------------
if not exist "data" (
    mkdir "data"
    echo Created data directory
) else (
    echo Data directory already exists
)

REM Create default preferences if not exists
if not exist "data\user_preferences.json" (
    echo Creating default preferences...
    echo { > "data\user_preferences.json"
    echo   "theme": "dark", >> "data\user_preferences.json"
    echo   "opacity": 0.95, >> "data\user_preferences.json"
    echo   "topmost": true, >> "data\user_preferences.json"
    echo   "default_method": "auto", >> "data\user_preferences.json"
    echo   "default_budget": 1000, >> "data\user_preferences.json"
    echo   "default_ilvl": 85, >> "data\user_preferences.json"
    echo   "league": "Standard" >> "data\user_preferences.json"
    echo } >> "data\user_preferences.json"
)

echo.
echo [4/7] Cleaning previous builds...
echo --------------------------------
if exist "build" (
    rmdir /s /q "build"
    echo Removed build directory
)
if exist "dist" (
    rmdir /s /q "dist"
    echo Removed dist directory
)
if exist "__pycache__" (
    rmdir /s /q "__pycache__"
    echo Removed __pycache__ directory
)

echo.
echo [5/7] Checking required files...
echo --------------------------------
echo Debug: Checking for launcher.py...
if exist "launcher.py" (
    echo launcher.py found
) else (
    echo ERROR: launcher.py not found!
    echo Please ensure launcher.py exists in the current directory
    pause
    exit /b 1
)

echo.
echo Debug: Build would start here, but stopping for debugging
echo.
echo Current directory contents:
dir /b
echo.
echo Press any key to exit debug mode...
pause
exit /b 0