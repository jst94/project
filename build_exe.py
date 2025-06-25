#!/usr/bin/env python3
"""
Build script for creating a standalone executable of the PoE Craft Helper
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "--break-system-packages"])

def create_spec_file():
    """Create a PyInstaller spec file for the application"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['poe_craft_helper.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'cv2',
        'numpy',
        'PIL',
        'PIL._tkinter_finder',
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'pytesseract',
        'requests',
        'json',
        'threading',
        'time',
        'datetime',
        'random',
        'os',
        're'
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
    console=False,  # Set to True if you want a console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add path to .ico file if you have one
)
'''
    
    with open('poe_craft_helper.spec', 'w') as f:
        f.write(spec_content)
    
    print("Created PyInstaller spec file: poe_craft_helper.spec")

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # Use the spec file for more control
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--onefile",
        "--windowed",  # No console window
        "--name=PoE_Craft_Helper",
        "poe_craft_helper.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("Build completed successfully!")
        print("Executable location: dist/PoE_Craft_Helper.exe")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False
    
    return True

def create_portable_package():
    """Create a portable package with the executable and any additional files"""
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
        print(f"Copied executable to {portable_dir}")
    else:
        print("Executable not found in dist/ directory")
        return False
    
    # Copy README and other important files
    files_to_copy = ["README.md", "requirements.txt"]
    for file_name in files_to_copy:
        if Path(file_name).exists():
            shutil.copy2(file_name, portable_dir)
    
    # Create a simple launcher script
    launcher_content = '''@echo off
echo Starting PoE Craft Helper...
echo.
echo This is a portable version of the Path of Exile Craft Helper.
echo All dependencies are bundled within the executable.
echo.
echo If you encounter any issues, please check:
echo - Windows Defender is not blocking the executable
echo - You have sufficient permissions to run the file
echo.
pause
start PoE_Craft_Helper.exe
'''
    
    with open(portable_dir / "launch.bat", 'w') as f:
        f.write(launcher_content)
    
    print(f"Portable package created in: {portable_dir}")
    return True

def main():
    """Main build process"""
    print("=== PoE Craft Helper - Executable Builder ===")
    print()
    
    # Install PyInstaller
    install_pyinstaller()
    print()
    
    # Create spec file
    create_spec_file()
    print()
    
    # Build executable
    if build_executable():
        print()
        # Create portable package
        create_portable_package()
        print()
        print("=== Build Process Complete ===")
        print("Your executable is ready in the 'dist' folder!")
        print("Portable package is in 'PoE_Craft_Helper_Portable' folder")
        print()
        print("To distribute:")
        print("1. Copy the entire 'PoE_Craft_Helper_Portable' folder")
        print("2. The recipient can run 'launch.bat' or 'PoE_Craft_Helper.exe' directly")
        print("3. No additional installations required!")
    else:
        print("Build process failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 