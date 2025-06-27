# Auto-Detection Setup Guide

## Overview
The auto-detection feature allows you to automatically detect Path of Exile items by hovering over them and pressing a hotkey (Ctrl+D by default).

## Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
python fix_auto_detection.py
```
This script will:
- Install all required dependencies
- Test the functionality
- Create a test script for manual verification

### Option 2: Manual Installation
```bash
# Required dependencies
pip install keyboard mss

# Optional but recommended for better OCR
pip install easyocr

# Core dependencies (should already be installed)
pip install opencv-python pytesseract Pillow numpy
```

## System Requirements

### Windows
- **Tesseract OCR**: Download from [GitHub Releases](https://github.com/UB-Mannheim/tesseract/wiki)
- Add Tesseract to your system PATH, or install to default location

### Linux
```bash
sudo apt-get install tesseract-ocr
```

### macOS
```bash
brew install tesseract
```

## How It Works

1. **Screen Capture**: Captures the current screen when hotkey is pressed
2. **Text Extraction**: Uses OCR (Optical Character Recognition) to read text from the image
3. **Item Parsing**: Analyzes the extracted text to identify item properties
4. **UI Update**: Automatically fills in the detected information

## Usage

### Enabling Auto-Detection
1. Start the PoE Craft Helper
2. Go to the "Detection" tab or click "Item Detection"
3. Click "Enable Auto-Detection (Ctrl+D)"
4. You should see a confirmation message

### Using Auto-Detection
1. **In Path of Exile**: Hover your mouse over an item tooltip
2. **Press Ctrl+D**: The hotkey will trigger detection
3. **Check Results**: The application will populate detected information
4. **Verify Data**: Always verify the detected information is correct

## Troubleshooting

### Common Issues

#### 1. "Keyboard module not available"
**Solution**: Install the keyboard module
```bash
pip install keyboard
```

#### 2. "Tesseract not found"
**Symptoms**: OCR fails with tesseract errors
**Solutions**:
- **Windows**: Download and install Tesseract from the official releases
- **Linux**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`
- Check that tesseract is in your system PATH

#### 3. "No item detected"
**Possible Causes**:
- Item tooltip not visible or partially obscured
- Game is in fullscreen mode (use windowed or borderless)
- Tooltip disappeared too quickly
- Low contrast or small text

**Solutions**:
- Ensure the item tooltip is fully visible
- Use windowed or borderless windowed mode
- Try hovering over the item again and press Ctrl+D while tooltip is stable
- Check that the tooltip has good contrast

#### 4. "Permission denied" or "Access denied"
**Solution**: Run the application as administrator (Windows) or with appropriate permissions

#### 5. "Detection is slow"
**Solutions**:
- Install `mss` for faster screen capture: `pip install mss`
- Install `easyocr` for better OCR: `pip install easyocr`
- Close unnecessary applications

### Advanced Troubleshooting

#### Test OCR Manually
```python
import pytesseract
from PIL import ImageGrab

# Test basic OCR
screenshot = ImageGrab.grab()
text = pytesseract.image_to_string(screenshot)
print("OCR working:", len(text) > 0)
```

#### Test Screen Capture
```python
# Test with PIL
from PIL import ImageGrab
screenshot = ImageGrab.grab()
screenshot.save("test_capture.png")
print("Screen capture saved to test_capture.png")
```

#### Test Hotkey Detection
```python
# Run the test script
python test_auto_detection.py
```

## Optimization Tips

### For Better Detection Accuracy
1. **Game Settings**:
   - Use windowed or borderless windowed mode
   - Ensure good contrast in game settings
   - Use a consistent UI scale

2. **System Settings**:
   - Ensure adequate lighting if using a CRT monitor
   - Use standard DPI settings (100% scaling recommended)
   - Close screen recording software that might interfere

3. **Usage Tips**:
   - Let the tooltip stabilize before pressing Ctrl+D
   - Ensure the entire tooltip is visible
   - Avoid pressing the hotkey multiple times rapidly

### For Better Performance
1. **Install Optional Dependencies**:
   ```bash
   pip install mss easyocr
   ```

2. **System Optimization**:
   - Close unnecessary applications
   - Ensure adequate RAM is available
   - Use an SSD for better I/O performance

## Configuration

### Custom Hotkey
To change the hotkey from Ctrl+D to something else, modify the setup call:
```python
detector.setup_hotkey(app_instance, 'ctrl+shift+d')  # Custom hotkey
```

### OCR Settings
Advanced users can modify OCR settings in the auto-detection module:
- Confidence threshold
- Preprocessing options
- Multiple OCR engine usage

## Supported Item Types

The auto-detection system can detect:
- **Weapons**: Swords, Axes, Maces, Bows, Wands, Daggers, Claws, Staves, Sceptres
- **Armor**: Helmets, Body Armour, Gloves, Boots, Shields
- **Jewelry**: Rings, Amulets, Belts
- **Other**: Flasks, Jewels, Maps (with varying accuracy)

### Detected Properties
- Item base type
- Item level
- Quality percentage
- Rarity (Normal, Magic, Rare, Unique)
- Modifiers (affixes)
- Some implicit modifiers

## Limitations

### Technical Limitations
- Requires the game to be in windowed or borderless mode
- OCR accuracy depends on image quality and contrast
- May not work with custom UI mods that change tooltip appearance
- Performance depends on system specifications

### Detection Limitations
- Complex or corrupted items may not be fully parsed
- Very long modifier lists might be truncated
- Some implicit modifiers may not be detected
- Currency items and skill gems have limited detection

### System Limitations
- Hotkey may conflict with other applications
- Screen capture may be blocked by some security software
- Requires appropriate system permissions

## Security Notes

### Permissions Required
- **Screen Capture**: Required to capture game tooltips
- **Keyboard Hooks**: Required for hotkey detection
- **File System**: Required to save settings and cache

### Privacy
- No data is transmitted over the network during detection
- Screenshots are processed locally and not saved permanently
- Only the immediate screen area is analyzed

## FAQ

**Q: Does this work with other games?**
A: The auto-detection is specifically designed for Path of Exile tooltips and may not work with other games.

**Q: Can I use this with multiple monitors?**
A: Yes, but the detection will capture the primary monitor. Ensure PoE is on the primary monitor.

**Q: Does this violate the game's terms of service?**
A: This tool only reads pixels from the screen and does not interact with the game process. However, always check the current ToS.

**Q: Why is detection sometimes inaccurate?**
A: OCR technology has limitations with small text, low contrast, or complex backgrounds. The system works best with clear, high-contrast tooltips.

**Q: Can I improve detection accuracy?**
A: Yes, ensure good game contrast settings, use windowed mode, and install the optional `easyocr` package for better OCR.

## Support

If you continue to have issues:
1. Run the diagnostic script: `python fix_auto_detection.py`
2. Check the console output for error messages
3. Verify all dependencies are installed correctly
4. Test with the manual test script: `python test_auto_detection.py`

For additional help, ensure you can provide:
- Your operating system and version
- Python version (`python --version`)
- Error messages from the console
- Whether basic OCR works (`python -c "import pytesseract; print(pytesseract.get_tesseract_version())"`)