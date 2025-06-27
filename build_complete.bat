@echo off
REM Ensure script stays open on error
if "%1"=="" (
    cmd /k "%~f0" RUN
    exit /b
)

setlocal enabledelayedexpansion
title PoE Craft Helper - Complete Build System
REM Change to script directory
cd /d "%~dp0"
echo =========================================
echo    PoE Craft Helper - Complete Build
echo =========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or later
    pause
    exit /b 1
)

echo [0/7] Checking for Tesseract OCR...
echo ------------------------------------

REM First try to find tesseract in PATH
set "TESSERACT_FOUND=0"
where tesseract >nul 2>&1 && set "TESSERACT_FOUND=1"

if "!TESSERACT_FOUND!"=="0" (
    echo Tesseract not found in PATH. Checking common locations...
    
    REM Check common Tesseract installation paths
    set "TESSERACT_PATH="
    if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
        set "TESSERACT_PATH=C:\Program Files\Tesseract-OCR"
    ) else if exist "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe" (
        set "TESSERACT_PATH=C:\Program Files (x86)\Tesseract-OCR"
    ) else if exist "%LOCALAPPDATA%\Tesseract-OCR\tesseract.exe" (
        set "TESSERACT_PATH=%LOCALAPPDATA%\Tesseract-OCR"
    ) else if exist "%PROGRAMFILES%\Tesseract-OCR\tesseract.exe" (
        set "TESSERACT_PATH=%PROGRAMFILES%\Tesseract-OCR"
    )
    
    if defined TESSERACT_PATH (
        echo Found Tesseract at: !TESSERACT_PATH!
        echo Adding to PATH for this session...
        set "PATH=!TESSERACT_PATH!;!PATH!"
        
        REM Verify it works
        "!TESSERACT_PATH!\tesseract.exe" --version >nul 2>&1
        if !errorlevel! equ 0 (
            echo Tesseract successfully added to PATH!
            
            REM Set the environment variable for pytesseract
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
    tesseract --version 2>&1 | findstr /i "tesseract"
)

echo.
echo [1/7] Running pre-build checks...
echo ---------------------------------
python pre_build_check.py
if %errorlevel% neq 0 (
    echo.
    echo Pre-build checks failed!
    echo Please fix the issues above before continuing.
    pause
    exit /b 1
)
echo Pre-build checks passed!

echo [2/7] Installing dependencies...
echo --------------------------------
pip install pyinstaller opencv-python pytesseract Pillow numpy requests psutil --quiet --break-system-packages

echo.
echo [3/7] Creating data directory...
echo --------------------------------
if not exist "data" mkdir "data"
echo Created data directory

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
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"
echo Cleaned build directories

echo.
echo [5/7] Building executable with launcher...
echo -----------------------------------------
echo This will include:
echo - Launcher (for choosing versions)
echo - Original POE Craft Helper
echo - Refactored version (modern UI)
echo - Simple version (lightweight)
echo - Flask Craft Helper
echo - All dependencies
echo.

REM Create the spec file inline
echo Creating build specification...
(
echo # -*- mode: python ; coding: utf-8 -*-
echo import os
echo from PyInstaller.utils.hooks import collect_submodules
echo.
echo block_cipher = None
echo.
echo # All required modules
echo hiddenimports = [
echo     'cv2', 'numpy', 'PIL', 'PIL._tkinter_finder',
echo     'tkinter', 'tkinter.ttk', 'tkinter.scrolledtext', 'tkinter.messagebox',
echo     'pytesseract', 'requests', 'json', 'threading', 'time', 'datetime',
echo     'random', 'os', 're', 'psutil', 'sqlite3', 'logging', 'typing',
echo     'market_api', 'ocr_analyzer', 'session_tracker', 'performance_optimizer',
echo     'ai_crafting_optimizer', 'intelligent_ocr', 'probability_engine',
echo     'market_intelligence', 'enhanced_modifier_database', 
echo     'intelligent_recommendations', 'adaptive_learning_system',
echo     'realtime_strategy_optimizer', 'league_config', 'config',
echo     'flask_craft_helper', 'auto_detection', 'flask_crafting',
echo     'poe_craft_helper', 'poe_craft_helper_refactored', 'poe_craft_helper_simple'
echo ]
echo.
echo hiddenimports += collect_submodules('psutil'^)
echo.
echo # Include all Python files and data
echo datas = [
echo     ('data', 'data'^),
echo     ('*.py', '.'^),
echo     ('README.md', '.'^),
echo     ('CHANGELOG.md', '.'^),
echo     ('REFACTORING_NOTES.md', '.'^),
echo     ('requirements.txt', '.'^)
echo ]
echo.
echo a = Analysis(
echo     ['launcher.py'],
echo     pathex=[os.path.abspath('.'^^)],
echo     binaries=[],
echo     datas=datas,
echo     hiddenimports=hiddenimports,
echo     hookspath=[],
echo     hooksconfig={},
echo     runtime_hooks=[],
echo     excludes=['matplotlib', 'scipy', 'pandas'],
echo     win_no_prefer_redirects=False,
echo     win_private_assemblies=False,
echo     cipher=block_cipher,
echo     noarchive=False,
echo ^)
echo.
echo pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher^)
echo.
echo exe = EXE(
echo     pyz,
echo     a.scripts,
echo     a.binaries,
echo     a.zipfiles,
echo     a.datas,
echo     [],
echo     name='PoE_Craft_Helper',
echo     debug=False,
echo     bootloader_ignore_signals=False,
echo     strip=False,
echo     upx=True,
echo     upx_exclude=[],
echo     runtime_tmpdir=None,
echo     console=False,
echo     disable_windowed_traceback=False,
echo     argv_emulation=False,
echo     target_arch=None,
echo     codesign_identity=None,
echo     entitlements_file=None,
echo ^)
) > "build_spec.spec"

REM Build with PyInstaller
python -m PyInstaller --clean "build_spec.spec"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [6/7] Creating portable package...
echo ---------------------------------
if exist "PoE_Craft_Helper_Portable" rmdir /s /q "PoE_Craft_Helper_Portable"
mkdir "PoE_Craft_Helper_Portable"
mkdir "PoE_Craft_Helper_Portable\data"

REM Copy executable
copy "dist\PoE_Craft_Helper.exe" "PoE_Craft_Helper_Portable\" >nul
echo Copied executable

REM Copy data files
if exist "data\user_preferences.json" (
    copy "data\user_preferences.json" "PoE_Craft_Helper_Portable\data\" >nul
)

REM Copy documentation
if exist "README.md" copy "README.md" "PoE_Craft_Helper_Portable\" >nul
if exist "CHANGELOG.md" copy "CHANGELOG.md" "PoE_Craft_Helper_Portable\" >nul
if exist "REFACTORING_NOTES.md" copy "REFACTORING_NOTES.md" "PoE_Craft_Helper_Portable\" >nul
echo Copied documentation

REM Create launcher batch
echo @echo off > "PoE_Craft_Helper_Portable\Launch_PoE_Craft_Helper.bat"
echo title PoE Craft Helper >> "PoE_Craft_Helper_Portable\Launch_PoE_Craft_Helper.bat"
echo echo Starting PoE Craft Helper... >> "PoE_Craft_Helper_Portable\Launch_PoE_Craft_Helper.bat"
echo cd /d "%%~dp0" >> "PoE_Craft_Helper_Portable\Launch_PoE_Craft_Helper.bat"
echo start "" "PoE_Craft_Helper.exe" >> "PoE_Craft_Helper_Portable\Launch_PoE_Craft_Helper.bat"
echo timeout /t 2 /nobreak ^>nul >> "PoE_Craft_Helper_Portable\Launch_PoE_Craft_Helper.bat"
echo exit >> "PoE_Craft_Helper_Portable\Launch_PoE_Craft_Helper.bat"

echo.
echo [7/7] Cleaning up...
echo -------------------
del "build_spec.spec" >nul 2>&1
echo Cleaned temporary files

echo.
echo =========================================
echo         BUILD COMPLETE!
echo =========================================
echo.
echo Your executable package is ready:
echo.
echo Location: PoE_Craft_Helper_Portable\
echo.
echo Contents:
echo - PoE_Craft_Helper.exe (All-in-one executable)
echo - Launch_PoE_Craft_Helper.bat (Quick launcher)
echo - data\ (User preferences and data)
echo - Documentation files
echo.
echo The package includes:
echo ✓ Version selector (launcher)
echo ✓ Original POE Craft Helper
echo ✓ Refactored version with modern UI
echo ✓ Simple lightweight version
echo ✓ Flask crafting helper
echo ✓ All dependencies bundled
echo.
echo To distribute:
echo 1. ZIP the entire 'PoE_Craft_Helper_Portable' folder
echo 2. Users can extract and run anywhere
echo 3. No Python or dependencies needed!
echo.
pause
exit /b 0

:error
echo.
echo =========================================
echo         ERROR OCCURRED!
echo =========================================
echo.
echo The build process encountered an error.
echo Please check the messages above for details.
echo.
pause
exit /b 1