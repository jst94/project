#!/usr/bin/env python3
"""
Comprehensive build script for PoE Craft Helper
Builds the launcher and all versions into a single executable package
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json

def install_dependencies():
    """Install all required dependencies"""
    print("Installing build dependencies...")
    dependencies = [
        "pyinstaller",
        "opencv-python",
        "pytesseract",
        "Pillow",
        "numpy",
        "requests",
        "psutil"
    ]
    
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep, "--quiet"])
            print(f"✓ {dep}")
        except:
            print(f"✗ {dep} (failed, but continuing...)")

def create_comprehensive_spec():
    """Create a spec file that includes all versions and resources"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# Collect all Python modules
all_modules = [
    'cv2', 'numpy', 'PIL', 'PIL._tkinter_finder',
    'tkinter', 'tkinter.ttk', 'tkinter.scrolledtext', 'tkinter.messagebox',
    'pytesseract', 'requests', 'json', 'threading', 'time', 'datetime',
    'random', 'os', 're', 'psutil', 'sqlite3', 'logging', 'typing'
]

# Add all local modules
local_modules = [
    'market_api', 'ocr_analyzer', 'session_tracker', 'performance_optimizer',
    'ai_crafting_optimizer', 'intelligent_ocr', 'probability_engine',
    'market_intelligence', 'enhanced_modifier_database', 
    'intelligent_recommendations', 'adaptive_learning_system',
    'realtime_strategy_optimizer', 'league_config', 'config',
    'flask_craft_helper', 'auto_detection', 'flask_crafting'
]

hiddenimports = all_modules + local_modules
hiddenimports += collect_submodules('psutil')

# Collect data files
datas = [
    ('data', 'data'),
    ('*.py', '.'),  # Include all Python files
    ('README.md', '.'),
    ('CHANGELOG.md', '.'),
    ('REFACTORING_NOTES.md', '.'),
    ('requirements.txt', '.')
]

# Main analysis for launcher
a = Analysis(
    ['launcher.py'],
    pathex=[os.path.abspath('.')],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'pandas'],  # Exclude unused large libraries
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PoE_Craft_Helper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path if available
    version_file=None,
)
'''
    
    with open('poe_craft_helper_all.spec', 'w') as f:
        f.write(spec_content)
    
    print("Created comprehensive spec file: poe_craft_helper_all.spec")

def create_version_info():
    """Create version information file"""
    version_info = {
        "name": "PoE Craft Helper",
        "version": "3.26.0",
        "description": "Intelligent Path of Exile Crafting Assistant",
        "author": "PoE Craft Helper Team",
        "copyright": "Copyright 2024",
        "includes": {
            "launcher": True,
            "original_version": True,
            "refactored_version": True,
            "simple_version": True,
            "flask_helper": True
        }
    }
    
    with open('version_info.json', 'w') as f:
        json.dump(version_info, f, indent=2)

def ensure_data_directory():
    """Ensure data directory exists with necessary files"""
    data_dir = Path("data")
    if not data_dir.exists():
        data_dir.mkdir()
        print("Created data directory")
    
    # Create default user preferences if not exists
    prefs_file = data_dir / "user_preferences.json"
    if not prefs_file.exists():
        default_prefs = {
            "theme": "dark",
            "opacity": 0.95,
            "topmost": True,
            "default_method": "auto",
            "default_budget": 1000,
            "default_ilvl": 85,
            "league": "Standard"
        }
        with open(prefs_file, 'w') as f:
            json.dump(default_prefs, f, indent=2)
        print("Created default user preferences")

def build_executable():
    """Build the all-in-one executable"""
    print("\nBuilding executable...")
    
    # Clean previous builds
    for folder in ['build', 'dist']:
        if Path(folder).exists():
            shutil.rmtree(folder)
            print(f"Cleaned {folder} directory")
    
    # Run PyInstaller with spec file
    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "poe_craft_helper_all.spec"]
    
    try:
        subprocess.check_call(cmd)
        print("\n✓ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        return False

def create_portable_package():
    """Create the final portable package"""
    print("\nCreating portable package...")
    
    portable_dir = Path("PoE_Craft_Helper_Portable")
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    portable_dir.mkdir()
    
    # Copy executable
    exe_source = Path("dist/PoE_Craft_Helper.exe")
    if exe_source.exists():
        shutil.copy2(exe_source, portable_dir / "PoE_Craft_Helper.exe")
        print("✓ Copied executable")
    else:
        print("✗ Executable not found!")
        return False
    
    # Create data directory in portable package
    (portable_dir / "data").mkdir(exist_ok=True)
    
    # Copy data files if they exist
    if Path("data/user_preferences.json").exists():
        shutil.copy2("data/user_preferences.json", portable_dir / "data")
    
    # Copy documentation
    docs_to_copy = ["README.md", "CHANGELOG.md", "REFACTORING_NOTES.md", "requirements.txt"]
    for doc in docs_to_copy:
        if Path(doc).exists():
            shutil.copy2(doc, portable_dir)
            print(f"✓ Copied {doc}")
    
    # Create comprehensive launcher batch file
    launcher_content = '''@echo off
title PoE Craft Helper Launcher
echo =====================================
echo    Path of Exile Craft Helper
echo          Version 3.26.0
echo =====================================
echo.
echo Starting application...
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges
) else (
    echo Running with standard privileges
)

REM Set working directory to script location
cd /d "%~dp0"

REM Check for data directory
if not exist "data" (
    mkdir "data"
    echo Created data directory
)

REM Launch the application
start "" "PoE_Craft_Helper.exe"

REM Exit after 3 seconds
timeout /t 3 /nobreak >nul
exit
'''
    
    with open(portable_dir / "Launch_PoE_Craft_Helper.bat", 'w') as f:
        f.write(launcher_content)
    
    # Create README for the portable version
    portable_readme = '''# PoE Craft Helper - Portable Edition

## Quick Start
1. Double-click `Launch_PoE_Craft_Helper.bat` or `PoE_Craft_Helper.exe`
2. Choose your preferred interface from the launcher
3. Start crafting!

## Features
- **Launcher**: Choose between Original, Refactored, or Simple interface
- **All-in-One**: All versions bundled in a single executable
- **Portable**: No installation required, runs from any location
- **Self-Contained**: All dependencies included

## Included Versions
1. **Refactored Version** (Recommended)
   - Modern, clean interface with tabs
   - Better organization and visual hierarchy
   - All features from original version

2. **Original Version**
   - Classic interface with all features
   - Proven functionality
   - Full feature set

3. **Simple Version**
   - Lightweight interface
   - Basic crafting features
   - Fast and responsive

## Troubleshooting
- If Windows Defender blocks the executable, add an exception
- Run as administrator if you encounter permission issues
- The `data` folder stores your preferences and session data

## System Requirements
- Windows 7 or later
- 100MB free disk space
- Internet connection for market prices (optional)

## Notes
- First launch may take a few seconds to extract resources
- Settings are saved in the `data` folder
- Market prices update every 5 minutes when connected
'''
    
    with open(portable_dir / "README_PORTABLE.md", 'w') as f:
        f.write(portable_readme)
    
    print(f"\n✓ Portable package created in: {portable_dir}")
    return True

def create_installer_script():
    """Create an optional installer script"""
    installer_content = '''@echo off
title PoE Craft Helper Installer
echo =====================================
echo    PoE Craft Helper Installation
echo =====================================
echo.

REM Get installation directory
set "install_dir=%PROGRAMFILES%\PoE Craft Helper"
echo Default installation directory: %install_dir%
echo.

REM Ask for custom directory
set /p custom_dir="Press ENTER to use default or type a custom path: "
if not "%custom_dir%"=="" set "install_dir=%custom_dir%"

echo.
echo Installing to: %install_dir%
echo.

REM Create directory
if not exist "%install_dir%" mkdir "%install_dir%"

REM Copy files
echo Copying files...
xcopy /E /I /Y "PoE_Craft_Helper_Portable\*" "%install_dir%"

REM Create desktop shortcut
echo.
echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\PoE Craft Helper.lnk'); $Shortcut.TargetPath = '%install_dir%\PoE_Craft_Helper.exe'; $Shortcut.WorkingDirectory = '%install_dir%'; $Shortcut.Save()"

REM Create start menu entry
echo Creating start menu entry...
if not exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\PoE Craft Helper" mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\PoE Craft Helper"
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\PoE Craft Helper\PoE Craft Helper.lnk'); $Shortcut.TargetPath = '%install_dir%\PoE_Craft_Helper.exe'; $Shortcut.WorkingDirectory = '%install_dir%'; $Shortcut.Save()"

echo.
echo =====================================
echo    Installation Complete!
echo =====================================
echo.
echo PoE Craft Helper has been installed to:
echo %install_dir%
echo.
echo Desktop shortcut created
echo Start menu entry created
echo.
pause
'''
    
    with open("install.bat", 'w') as f:
        f.write(installer_content)
    
    print("✓ Created installer script: install.bat")

def main():
    """Main build process"""
    print("=== PoE Craft Helper - Comprehensive Build ===\n")
    
    # Install dependencies
    install_dependencies()
    print()
    
    # Ensure data directory exists
    ensure_data_directory()
    print()
    
    # Create version info
    create_version_info()
    
    # Create spec file
    create_comprehensive_spec()
    print()
    
    # Build executable
    if build_executable():
        # Create portable package
        if create_portable_package():
            # Create installer
            create_installer_script()
            
            print("\n=== Build Complete! ===")
            print("\nCreated:")
            print("✓ dist/PoE_Craft_Helper.exe - Standalone executable")
            print("✓ PoE_Craft_Helper_Portable/ - Portable package folder")
            print("✓ install.bat - Optional installer script")
            print("\nTo distribute:")
            print("1. ZIP the 'PoE_Craft_Helper_Portable' folder")
            print("2. Users can run directly or use install.bat")
            print("\nThe executable includes:")
            print("- Launcher for choosing versions")
            print("- Original POE Craft Helper")
            print("- Refactored version with modern UI")
            print("- Simple lightweight version")
            print("- All dependencies bundled")
        else:
            print("\n✗ Failed to create portable package")
    else:
        print("\n✗ Build failed. Check error messages above.")

if __name__ == "__main__":
    main()