#!/usr/bin/env python3
"""
Simple build script for creating a standalone executable
"""

import os
import sys
import subprocess

def main():
    print("=== Building PoE Craft Helper Executable ===")
    
    # Install PyInstaller if needed
    try:
        import PyInstaller
        print("PyInstaller found")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "--break-system-packages"])
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=PoE_Craft_Helper",
        "--hidden-import=cv2",
        "--hidden-import=numpy",
        "--hidden-import=PIL",
        "--hidden-import=tkinter",
        "--hidden-import=requests",
        "--hidden-import=json",
        "--hidden-import=threading",
        "--hidden-import=time",
        "--hidden-import=datetime",
        "--hidden-import=random",
        "--hidden-import=os",
        "--hidden-import=re",
        "poe_craft_helper.py"
    ]
    
    print("Building executable...")
    subprocess.check_call(cmd)
    
    print("\n=== Build Complete ===")
    print("Executable created: dist/PoE_Craft_Helper.exe")
    print("You can now copy this file to any Windows PC and run it!")

if __name__ == "__main__":
    main() 