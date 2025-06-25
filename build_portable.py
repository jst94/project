#!/usr/bin/env python3
"""
Portable PoE Craft Helper Build Script
Creates a standalone executable with all dependencies bundled
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_dependencies():
    """Install required packages"""
    print("Installing dependencies...")
    packages = [
        "pyinstaller>=5.0.0",
        "opencv-python>=4.5.0", 
        "pytesseract>=0.3.8",
        "Pillow>=8.0.0",
        "numpy>=1.20.0",
        "requests>=2.25.0"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package, "--break-system-packages"
            ])
            print(f"✓ Installed {package}")
        except Exception as e:
            print(f"✗ Failed to install {package}: {e}")

def create_spec_file():
    """Create PyInstaller spec file"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['poe_craft_helper.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'cv2', 'numpy', 'PIL', 'PIL._tkinter_finder',
        'tkinter', 'tkinter.ttk', 'tkinter.scrolledtext', 'tkinter.messagebox',
        'pytesseract', 'requests', 'json', 'threading', 'time', 'datetime',
        'random', 'os', 're', 'market_api', 'session_tracker', 'performance_optimizer'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open('poe_craft_helper.spec', 'w') as f:
        f.write(spec_content)
    print("✓ Created PyInstaller spec file")

def build_executable():
    """Build the executable"""
    print("Building executable...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--onefile", 
        "--windowed",
        "--name=PoE_Craft_Helper",
        "poe_craft_helper.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✓ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False

def create_portable_package():
    """Create portable package"""
    print("Creating portable package...")
    
    # Create portable directory
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
        print("✗ Executable not found")
        return False
    
    # Copy important files
    files_to_copy = ["README.md"]
    for file_name in files_to_copy:
        if Path(file_name).exists():
            shutil.copy2(file_name, portable_dir)
    
    # Create launcher script
    launcher_content = '''@echo off
echo ========================================
echo    PoE Craft Helper - Portable Version
echo ========================================
echo.
echo Starting application...
echo All dependencies are bundled within the executable.
echo.
echo If you encounter issues:
echo - Check Windows Defender is not blocking the file
echo - Run as administrator if needed
echo - Ensure you have sufficient disk space
echo.
start PoE_Craft_Helper.exe
'''
    
    with open(portable_dir / "launch.bat", 'w') as f:
        f.write(launcher_content)
    
    # Create README for portable version
    readme_content = '''# PoE Craft Helper - Portable Version

## Quick Start
1. Double-click `launch.bat` or `PoE_Craft_Helper.exe`
2. No installation required - all dependencies are bundled

## Features
- Intelligent crafting plan generation
- Real-time market price integration
- Session tracking and analytics
- Performance optimization
- Overlay functionality

## System Requirements
- Windows 10/11 (64-bit)
- 4GB RAM minimum
- 500MB free disk space

## Troubleshooting
- If the app doesn't start, try running as administrator
- Windows Defender may flag the executable - add to exclusions
- Ensure your antivirus isn't blocking the file

## Support
For issues or questions, check the main README.md file.
'''
    
    with open(portable_dir / "PORTABLE_README.txt", 'w') as f:
        f.write(readme_content)
    
    print(f"✓ Portable package created in: {portable_dir}")
    return True

def main():
    """Main build process"""
    print("=== PoE Craft Helper - Portable Builder ===")
    print()
    
    # Install dependencies
    install_dependencies()
    print()
    
    # Create spec file
    create_spec_file()
    print()
    
    # Build executable
    if build_executable():
        print()
        # Create portable package
        if create_portable_package():
            print()
            print("=== BUILD COMPLETE ===")
            print("✓ Executable: dist/PoE_Craft_Helper.exe")
            print("✓ Portable package: PoE_Craft_Helper_Portable/")
            print()
            print("To distribute:")
            print("1. Copy the entire 'PoE_Craft_Helper_Portable' folder")
            print("2. Recipients can run 'launch.bat' or 'PoE_Craft_Helper.exe'")
            print("3. No additional installations required!")
        else:
            print("✗ Failed to create portable package")
    else:
        print("✗ Build process failed")

if __name__ == "__main__":
    main() 