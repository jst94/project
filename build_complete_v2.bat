@echo off
REM PoE Craft Helper - Complete Build System v2
REM More robust version with better error handling

REM Keep window open on error
if "%1"=="" (
    cmd /k "%~f0" RUN
    exit /b
)

setlocal
title PoE Craft Helper - Complete Build System
cd /d "%~dp0"

echo =========================================
echo    PoE Craft Helper - Complete Build
echo =========================================
echo.

REM Step 1: Check Python
echo [Step 1/7] Checking Python installation...
echo -----------------------------------------
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from python.org
    goto :error
)
python --version
echo Python check passed!
echo.

REM Step 2: Check/Configure Tesseract
echo [Step 2/7] Checking for Tesseract OCR...
echo ----------------------------------------
set TESSERACT_FOUND=NO

REM Try to find tesseract in PATH first
for %%i in (tesseract.exe) do (
    if not "%%~$PATH:i"=="" (
        set TESSERACT_FOUND=YES
        echo Tesseract found in system PATH
        tesseract --version 2>&1 | find "tesseract"
    )
)

REM If not found, check common locations
if "%TESSERACT_FOUND%"=="NO" (
    echo Tesseract not in PATH. Checking common locations...
    
    REM Check standard locations
    if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
        set "TESSERACT_PATH=C:\Program Files\Tesseract-OCR"
        set TESSERACT_FOUND=YES
    ) else if exist "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe" (
        set "TESSERACT_PATH=C:\Program Files (x86)\Tesseract-OCR"
        set TESSERACT_FOUND=YES
    ) else if exist "%LOCALAPPDATA%\Tesseract-OCR\tesseract.exe" (
        set "TESSERACT_PATH=%LOCALAPPDATA%\Tesseract-OCR"
        set TESSERACT_FOUND=YES
    )
    
    if "%TESSERACT_FOUND%"=="YES" (
        echo Found Tesseract at: %TESSERACT_PATH%
        echo Adding to PATH for this build session...
        set "PATH=%TESSERACT_PATH%;%PATH%"
        
        REM Test if it works
        "%TESSERACT_PATH%\tesseract.exe" --version >nul 2>&1
        if errorlevel 1 (
            echo ERROR: Cannot run Tesseract from %TESSERACT_PATH%
            goto :tesseract_error
        )
        echo Tesseract configured successfully!
    ) else (
        goto :tesseract_error
    )
)
echo.

REM Step 3: Run pre-build checks
echo [Step 3/7] Running pre-build checks...
echo --------------------------------------
if exist "pre_build_check.py" (
    python pre_build_check.py
    if errorlevel 1 (
        echo Pre-build checks failed! Please fix the issues above.
        goto :error
    )
) else (
    echo Warning: pre_build_check.py not found, skipping checks
)
echo Pre-build checks passed!
echo.

REM Step 4: Install dependencies
echo [Step 4/7] Installing Python dependencies...
echo -------------------------------------------
echo Installing: pyinstaller opencv-python pytesseract Pillow numpy requests psutil
pip install pyinstaller opencv-python pytesseract Pillow numpy requests psutil
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    goto :error
)
echo Dependencies installed successfully!
echo.

REM Step 5: Prepare directories
echo [Step 5/7] Preparing build directories...
echo ----------------------------------------
if not exist "data" mkdir "data"
echo Created/verified data directory

REM Create default preferences if missing
if not exist "data\user_preferences.json" (
    echo Creating default preferences...
    (
        echo {
        echo   "theme": "dark",
        echo   "opacity": 0.95,
        echo   "topmost": true,
        echo   "default_method": "auto",
        echo   "default_budget": 1000,
        echo   "default_ilvl": 85,
        echo   "league": "Standard"
        echo }
    ) > "data\user_preferences.json"
)

REM Clean old builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"
echo Cleaned old build directories
echo.

REM Step 6: Build executable
echo [Step 6/7] Building executable...
echo --------------------------------
echo Checking required files...

if not exist "launcher.py" (
    echo ERROR: launcher.py not found!
    goto :error
)

echo Creating PyInstaller spec file...
call :create_spec_file

echo Running PyInstaller...
python -m PyInstaller --clean "build_spec.spec"
if errorlevel 1 (
    echo ERROR: Build failed!
    goto :error
)
echo Build completed successfully!
echo.

REM Step 7: Create portable package
echo [Step 7/7] Creating portable package...
echo --------------------------------------
if exist "PoE_Craft_Helper_Portable" rmdir /s /q "PoE_Craft_Helper_Portable"
mkdir "PoE_Craft_Helper_Portable"
mkdir "PoE_Craft_Helper_Portable\data"

REM Copy files
copy "dist\PoE_Craft_Helper.exe" "PoE_Craft_Helper_Portable\" >nul
if exist "data\user_preferences.json" (
    copy "data\user_preferences.json" "PoE_Craft_Helper_Portable\data\" >nul
)
if exist "README.md" copy "README.md" "PoE_Craft_Helper_Portable\" >nul
if exist "CHANGELOG.md" copy "CHANGELOG.md" "PoE_Craft_Helper_Portable\" >nul

REM Create launcher batch
(
    echo @echo off
    echo title PoE Craft Helper
    echo echo Starting PoE Craft Helper...
    echo cd /d "%%~dp0"
    echo start "" "PoE_Craft_Helper.exe"
    echo timeout /t 2 /nobreak ^>nul
    echo exit
) > "PoE_Craft_Helper_Portable\Launch_PoE_Craft_Helper.bat"

REM Cleanup
del "build_spec.spec" >nul 2>&1

echo.
echo =========================================
echo         BUILD COMPLETE!
echo =========================================
echo.
echo Package location: PoE_Craft_Helper_Portable\
echo.
echo The package includes:
echo - PoE_Craft_Helper.exe (All versions)
echo - Launch_PoE_Craft_Helper.bat (Quick launcher)
echo - User preferences and documentation
echo.
echo Ready for distribution!
echo.
pause
exit /b 0

REM Error handlers
:tesseract_error
echo.
echo ERROR: Tesseract OCR is not installed!
echo.
echo Please install from: https://github.com/UB-Mannheim/tesseract/wiki
echo.
echo Recommended: Install to C:\Program Files\Tesseract-OCR
echo.
goto :error

:error
echo.
echo =========================================
echo         BUILD FAILED!
echo =========================================
echo.
echo Please check the error messages above.
echo.
pause
exit /b 1

REM Function to create spec file
:create_spec_file
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
goto :eof