# PoE Craft Helper - Build Instructions

## Overview
This document provides complete instructions for building the PoE Craft Helper into a standalone executable that bundles all versions and dependencies.

## Quick Build (Windows)

### Automated Build
```batch
# Run the complete build script
build_complete.bat
```

This will:
1. Check all prerequisites
2. Install dependencies
3. Create data directories
4. Build the executable with all versions
5. Create a portable package
6. Generate launcher scripts

### Manual Build
```batch
# Install dependencies
pip install -r requirements-build.txt

# Run pre-build checks
python pre_build_check.py

# Build using PyInstaller
python build_all.py
```

## Build Components

### 1. Launcher (`launcher.py`)
- Main entry point for the executable
- Provides version selection interface
- Dark-themed modern UI
- Launches other versions as needed

### 2. Included Versions
- **Refactored Version** (`poe_craft_helper_refactored.py`) - Modern UI
- **Original Version** (`poe_craft_helper.py`) - Classic interface
- **Simple Version** (`poe_craft_helper_simple.py`) - Lightweight
- **Flask Helper** (`flask_craft_helper.py`) - Flask crafting

### 3. Dependencies Bundled
- **Core**: tkinter, requests, numpy, psutil
- **OCR**: opencv-python, pytesseract, Pillow
- **AI/ML**: All intelligent crafting modules
- **Market**: API and price optimization modules
- **Session**: Tracking and analytics modules

## Build Process Details

### Pre-Build Checks (`pre_build_check.py`)
Validates:
- Python 3.8+ installation
- All source files present
- Required packages installed
- Data directory structure
- Documentation files

### Main Build Script (`build_all.py`)
1. **Dependency Installation**: Installs all required packages
2. **Data Setup**: Creates data directories and default files
3. **Spec Generation**: Creates PyInstaller specification
4. **Compilation**: Builds executable with all components
5. **Packaging**: Creates portable distribution
6. **Documentation**: Generates user instructions

### PyInstaller Configuration
```python
# Key settings for successful build
hiddenimports = [
    # Core GUI
    'tkinter', 'tkinter.ttk', 'tkinter.scrolledtext', 'tkinter.messagebox',
    
    # Image processing
    'cv2', 'numpy', 'PIL', 'PIL._tkinter_finder', 'pytesseract',
    
    # Network and data
    'requests', 'json', 'sqlite3', 'psutil',
    
    # All local modules
    'market_api', 'ocr_analyzer', 'session_tracker', 'performance_optimizer',
    'ai_crafting_optimizer', 'intelligent_ocr', 'probability_engine',
    'market_intelligence', 'enhanced_modifier_database',
    'intelligent_recommendations', 'adaptive_learning_system',
    'realtime_strategy_optimizer', 'league_config', 'config',
    'flask_craft_helper', 'auto_detection', 'flask_crafting',
    
    # All versions
    'poe_craft_helper', 'poe_craft_helper_refactored', 'poe_craft_helper_simple'
]

datas = [
    ('data', 'data'),           # User data and preferences
    ('*.py', '.'),              # All Python source files
    ('*.md', '.'),              # Documentation
    ('requirements.txt', '.')   # Dependencies list
]
```

## Output Structure

### Built Executable
```
dist/
└── PoE_Craft_Helper.exe    # All-in-one executable
```

### Portable Package
```
PoE_Craft_Helper_Portable/
├── PoE_Craft_Helper.exe           # Main executable
├── Launch_PoE_Craft_Helper.bat    # Quick launcher
├── data/                          # User data directory
│   └── user_preferences.json      # Default preferences
├── README_PORTABLE.md             # User instructions
├── README.md                      # Main documentation
├── CHANGELOG.md                   # Version history
└── REFACTORING_NOTES.md          # UI improvements
```

## Troubleshooting

### Common Build Issues

1. **"Module not found" errors**
   - Ensure all dependencies are installed: `pip install -r requirements-build.txt`
   - Check that all source files are present
   - Run `python pre_build_check.py`

2. **PyInstaller import errors**
   - Add missing modules to `hiddenimports` in spec file
   - Check for dynamically loaded modules
   - Use `--debug` flag for detailed error information

3. **Large executable size**
   - Exclude unused modules in `excludes` list
   - Remove development packages before building
   - Consider using `--onedir` instead of `--onefile` for faster startup

4. **Runtime errors in executable**
   - Test with `--console` flag to see error messages
   - Check that all data files are properly bundled
   - Ensure relative paths are used for bundled resources

### Platform-Specific Issues

#### Windows
- Install Visual C++ Redistributable if needed
- Some antivirus software may flag the executable
- Use `--uac-admin` if administrator privileges required

#### Linux/Mac
- Ensure shared libraries are available
- Check file permissions on executable
- May need to install system packages for OCR

## Build Optimization

### For Distribution
```batch
# Create optimized build
python -m PyInstaller --clean --onefile --windowed ^
    --optimize=2 --strip --upx --upx-dir=upx ^
    launcher.py
```

### For Development
```batch
# Create debug build
python -m PyInstaller --clean --onedir --console ^
    --debug=all --log-level=DEBUG ^
    launcher.py
```

## Testing the Build

### Manual Testing
1. Extract portable package to test location
2. Run `Launch_PoE_Craft_Helper.bat`
3. Test each version through launcher
4. Verify all features work offline
5. Test with different Windows versions

### Automated Testing
```python
# Basic functionality test
python -c "
import subprocess
import sys
result = subprocess.run(['dist/PoE_Craft_Helper.exe', '--test-mode'], 
                       capture_output=True, timeout=30)
sys.exit(0 if result.returncode == 0 else 1)
"
```

## Distribution

### For Users
- ZIP the entire `PoE_Craft_Helper_Portable` folder
- Users extract and run `Launch_PoE_Craft_Helper.bat`
- No installation required

### For Developers
- Include source code and build scripts
- Document any custom modifications
- Test on clean Windows installation

## Advanced Configuration

### Custom Icon
```python
# Add to spec file
exe = EXE(
    ...
    icon='path/to/icon.ico',
    ...
)
```

### Version Information
```python
# Add version resource (Windows)
version_file = 'version_info.txt'
exe = EXE(
    ...
    version_file=version_file,
    ...
)
```

### Code Signing (Optional)
```python
# For trusted distribution
exe = EXE(
    ...
    codesign_identity='Your Code Signing Certificate',
    ...
)
```

## Support

For build issues:
1. Check this documentation
2. Run pre-build checks
3. Review PyInstaller logs in `build/` directory
4. Test with minimal configuration first