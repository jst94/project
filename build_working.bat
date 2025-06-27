@echo off
REM PoE Craft Helper - Working Build Script

if "%1"=="" (
    cmd /k "%~f0" RUN
    exit /b
)

setlocal
title PoE Craft Helper - Build System
cd /d "%~dp0"

echo =========================================
echo    PoE Craft Helper - Build System
echo =========================================
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
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Check Tesseract
echo Checking for Tesseract OCR...
echo NOTE: Make sure Tesseract is installed and in PATH
echo You can download it from: https://github.com/UB-Mannheim/tesseract/wiki
echo.

REM Prepare directories
echo Preparing directories...
if not exist "data" mkdir "data"
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"
echo.

REM Check launcher.py
if not exist "launcher.py" (
    echo ERROR: launcher.py not found!
    pause
    exit /b 1
)

REM Create a simple spec file
echo Creating build configuration...
(
echo # PyInstaller spec file
echo import os
echo from PyInstaller.utils.hooks import collect_submodules
echo.
echo block_cipher = None
echo.
echo hiddenimports = ['cv2', 'numpy', 'PIL', 'tkinter', 'pytesseract', 'requests',
echo                  'psutil', 'sqlite3', 'logging', 'json', 'threading', 'time',
echo                  'market_api', 'ocr_analyzer', 'session_tracker',
echo                  'flask_craft_helper', 'auto_detection', 'flask_crafting',
echo                  'poe_craft_helper', 'poe_craft_helper_refactored', 
echo                  'poe_craft_helper_simple', 'launcher']
echo.
echo hiddenimports += collect_submodules('psutil'^)
echo.
echo datas = [('data', 'data'^), ('*.py', '.'^)]
echo.
echo a = Analysis(['launcher.py'],
echo              pathex=['.'],
echo              binaries=[],
echo              datas=datas,
echo              hiddenimports=hiddenimports,
echo              hookspath=[],
echo              runtime_hooks=[],
echo              excludes=['matplotlib', 'scipy', 'pandas'],
echo              win_no_prefer_redirects=False,
echo              win_private_assemblies=False,
echo              cipher=block_cipher,
echo              noarchive=False^)
echo.
echo pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher^)
echo.
echo exe = EXE(pyz,
echo           a.scripts,
echo           a.binaries,
echo           a.zipfiles,
echo           a.datas,
echo           [],
echo           name='PoE_Craft_Helper',
echo           debug=False,
echo           bootloader_ignore_signals=False,
echo           strip=False,
echo           upx=True,
echo           runtime_tmpdir=None,
echo           console=False,
echo           disable_windowed_traceback=False,
echo           argv_emulation=False,
echo           target_arch=None,
echo           codesign_identity=None,
echo           entitlements_file=None^)
) > poe_craft.spec

echo.
echo Building executable...
python -m PyInstaller --clean poe_craft.spec
if errorlevel 1 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo Creating portable package...
if exist "PoE_Craft_Helper_Portable" rmdir /s /q "PoE_Craft_Helper_Portable"
mkdir "PoE_Craft_Helper_Portable"
mkdir "PoE_Craft_Helper_Portable\data"

copy "dist\PoE_Craft_Helper.exe" "PoE_Craft_Helper_Portable\" >nul
if exist "README.md" copy "README.md" "PoE_Craft_Helper_Portable\" >nul
if exist "CHANGELOG.md" copy "CHANGELOG.md" "PoE_Craft_Helper_Portable\" >nul

echo.
echo =========================================
echo         BUILD COMPLETE!
echo =========================================
echo.
echo Executable location: PoE_Craft_Helper_Portable\PoE_Craft_Helper.exe
echo.
pause
exit /b 0