#!/usr/bin/env python3
"""
Pre-build checklist for PoE Craft Helper
Ensures all files and dependencies are in place before building
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check Python version is 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        return False, f"Python 3.8+ required, found {version.major}.{version.minor}"
    return True, f"Python {version.major}.{version.minor} ✓"

def check_required_files():
    """Check all required source files exist"""
    required_files = [
        "launcher.py",
        "poe_craft_helper.py",
        "poe_craft_helper_refactored.py",
        "poe_craft_helper_simple.py",
        "flask_craft_helper.py",
        "config.py",
        "market_api.py",
        "league_config.py",
        "session_tracker.py",
        "performance_optimizer.py",
        "ocr_analyzer.py",
        "ai_crafting_optimizer.py",
        "intelligent_ocr.py",
        "probability_engine.py",
        "market_intelligence.py",
        "enhanced_modifier_database.py",
        "intelligent_recommendations.py",
        "adaptive_learning_system.py",
        "realtime_strategy_optimizer.py"
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        return False, f"Missing files: {', '.join(missing)}"
    return True, f"All {len(required_files)} source files present ✓"

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        "tkinter": "tkinter",
        "requests": "requests",
        "numpy": "numpy",
        "PIL": "Pillow",
        "psutil": "psutil",
        "cv2": "opencv-python",
        "pytesseract": "pytesseract",
        "PyInstaller": "pyinstaller"
    }
    
    missing = []
    for module, package in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        return False, f"Missing packages: {', '.join(missing)}\nInstall with: pip install {' '.join(missing)}"
    return True, "All required packages installed ✓"

def check_data_directory():
    """Check data directory and files"""
    data_dir = Path("data")
    if not data_dir.exists():
        return False, "Data directory missing (will be created during build)"
    
    prefs_file = data_dir / "user_preferences.json"
    if not prefs_file.exists():
        return False, "User preferences file missing (will be created with defaults)"
    
    return True, "Data directory ready ✓"

def check_documentation():
    """Check documentation files"""
    docs = ["README.md", "CHANGELOG.md", "requirements.txt"]
    missing = [doc for doc in docs if not Path(doc).exists()]
    
    if missing:
        return False, f"Missing docs: {', '.join(missing)} (non-critical)"
    return True, "Documentation files present ✓"

def main():
    """Run all checks"""
    print("=== PoE Craft Helper Pre-Build Checklist ===\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Source Files", check_required_files),
        ("Dependencies", check_dependencies),
        ("Data Directory", check_data_directory),
        ("Documentation", check_documentation)
    ]
    
    all_passed = True
    critical_passed = True
    
    for name, check_func in checks:
        passed, message = check_func()
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:.<30} {status}")
        print(f"  {message}")
        print()
        
        if not passed:
            all_passed = False
            # Only Python, source files, and dependencies are critical
            if name in ["Python Version", "Source Files", "Dependencies"]:
                critical_passed = False
    
    print("="*45)
    if all_passed:
        print("✓ All checks passed! Ready to build.")
        return 0
    elif critical_passed:
        print("⚠ Non-critical issues found, but build can proceed.")
        return 0
    else:
        print("✗ Critical issues found. Please fix before building.")
        return 1

if __name__ == "__main__":
    sys.exit(main())