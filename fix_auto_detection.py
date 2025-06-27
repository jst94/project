#!/usr/bin/env python3
"""
Auto-Detection Fix Script
Installs missing dependencies and tests auto-detection functionality
"""

import subprocess
import sys
import os
from pathlib import Path

def install_package(package):
    """Install a package with pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--break-system-packages"])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_dependencies():
    """Check and install all auto-detection dependencies"""
    print("=== Auto-Detection Dependency Installer ===\n")
    
    # Required packages for auto-detection
    required_packages = {
        'keyboard': 'keyboard',  # For hotkey detection
        'mss': 'mss',           # For fast screen capture
        'easyocr': 'easyocr',   # Enhanced OCR (optional but recommended)
    }
    
    # Core packages (should already be installed)
    core_packages = {
        'cv2': 'opencv-python',
        'pytesseract': 'pytesseract',
        'PIL': 'Pillow',
        'numpy': 'numpy'
    }
    
    installed = []
    failed = []
    
    print("Checking core dependencies...")
    for module, package in core_packages.items():
        try:
            __import__(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - Installing...")
            if install_package(package):
                print(f"✓ {package} installed")
                installed.append(package)
            else:
                print(f"✗ {package} failed to install")
                failed.append(package)
    
    print("\nInstalling auto-detection specific packages...")
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✓ {package} already installed")
        except ImportError:
            print(f"Installing {package}...")
            if install_package(package):
                print(f"✓ {package} installed")
                installed.append(package)
            else:
                print(f"✗ {package} failed to install")
                failed.append(package)
    
    print(f"\n=== Installation Summary ===")
    if installed:
        print(f"Installed: {', '.join(installed)}")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    
    return len(failed) == 0

def test_auto_detection():
    """Test auto-detection functionality"""
    print("\n=== Testing Auto-Detection ===\n")
    
    try:
        # Test imports
        print("Testing imports...")
        import auto_detection
        print("✓ auto_detection module")
        
        print(f"✓ EasyOCR available: {auto_detection.EASYOCR_AVAILABLE}")
        print(f"✓ MSS available: {auto_detection.MSS_AVAILABLE}")
        
        # Test basic OCR
        print("\nTesting OCR engine...")
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"✓ Tesseract version: {version}")
        
        # Test screen capture
        print("\nTesting screen capture...")
        from auto_detection import ScreenCapture
        capture = ScreenCapture()
        print("✓ Screen capture initialized")
        
        # Test hotkey support
        print("\nTesting hotkey support...")
        try:
            import keyboard
            print("✓ Keyboard module available")
        except ImportError:
            print("✗ Keyboard module not available")
        
        print("\n✓ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        return False

def create_test_script():
    """Create a test script for auto-detection"""
    test_script = '''#!/usr/bin/env python3
"""
Auto-Detection Test Script
Tests the auto-detection functionality manually
"""

import sys
import time
import tkinter as tk
from tkinter import messagebox

def test_detection():
    """Test auto-detection manually"""
    try:
        from auto_detection import AutoDetector
        
        print("Starting auto-detection test...")
        print("Position your mouse over a PoE item tooltip and press Enter...")
        input("Press Enter when ready...")
        
        detector = AutoDetector()
        
        print("Detecting item at cursor position...")
        item = detector.detect_item_at_cursor()
        
        if item:
            print(f"\\n✓ Item detected!")
            print(f"Base Type: {item.base_type}")
            print(f"Item Type: {item.item_type}")
            print(f"Rarity: {item.rarity}")
            print(f"Confidence: {item.confidence:.0%}")
            
            if item.item_level:
                print(f"Item Level: {item.item_level}")
            
            if item.modifiers:
                print(f"Modifiers ({len(item.modifiers)}):")
                for mod in item.modifiers[:5]:  # Show first 5
                    print(f"  - {mod}")
        else:
            print("\\n✗ No item detected")
            print("Make sure:")
            print("- You're hovering over a PoE item tooltip")
            print("- The tooltip is clearly visible")
            print("- The game is in windowed or borderless mode")
        
    except Exception as e:
        print(f"\\n✗ Test failed: {e}")

def test_hotkey():
    """Test hotkey functionality"""
    try:
        import keyboard
        
        print("Testing hotkey functionality...")
        print("Press Ctrl+D to test hotkey detection (Ctrl+C to exit)")
        
        def on_hotkey():
            print("\\n🔥 Hotkey detected! Ctrl+D pressed")
        
        keyboard.add_hotkey('ctrl+d', on_hotkey)
        
        try:
            keyboard.wait('ctrl+c')
        except KeyboardInterrupt:
            pass
        
        print("\\nHotkey test complete")
        
    except ImportError:
        print("✗ Keyboard module not available for hotkey testing")
    except Exception as e:
        print(f"✗ Hotkey test failed: {e}")

if __name__ == "__main__":
    print("=== Auto-Detection Manual Test ===\\n")
    
    print("1. Manual detection test")
    print("2. Hotkey test")
    print("3. Exit")
    
    choice = input("\\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        test_detection()
    elif choice == '2':
        test_hotkey()
    else:
        print("Exiting...")
'''
    
    with open('test_auto_detection.py', 'w') as f:
        f.write(test_script)
    
    print("✓ Created test_auto_detection.py")

def main():
    """Main installation and test process"""
    print("This script will install and test auto-detection functionality.\n")
    
    # Install dependencies
    success = check_and_install_dependencies()
    
    if not success:
        print("\n⚠ Some packages failed to install.")
        print("Auto-detection may not work properly.")
        print("\nTry installing manually:")
        print("pip install keyboard mss easyocr")
        return
    
    # Test functionality
    if test_auto_detection():
        print("\n🎉 Auto-detection is ready!")
        print("\nTo use auto-detection:")
        print("1. Start the PoE Craft Helper")
        print("2. Click 'Item Detection' > 'Enable auto-detection'")
        print("3. Hover over an item in PoE and press Ctrl+D")
        
        # Create test script
        create_test_script()
        print("\n📝 Created test_auto_detection.py for manual testing")
        
    else:
        print("\n❌ Auto-detection test failed")
        print("Check the error messages above")

if __name__ == "__main__":
    main()