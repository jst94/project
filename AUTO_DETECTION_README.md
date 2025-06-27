# Auto-Detection Module for PoE Craft Helper

This module provides automatic item detection functionality for Path of Exile items using OCR (Optical Character Recognition) technology.

## Features

- **Screen Capture**: Automatic detection of PoE item tooltips on screen
- **OCR Processing**: Multiple OCR engines (Tesseract, EasyOCR) for accurate text extraction
- **Item Parsing**: Intelligent parsing of PoE item format including:
  - Item base type and rarity
  - Implicit and explicit modifiers
  - Crafted modifiers
  - Item level, quality, sockets
  - Influenced items (Shaper, Elder, etc.)
- **Hotkey Support**: Ctrl+D for quick detection
- **Confidence Scoring**: Validation of detection accuracy
- **Calibration Tools**: Optimize detection for your setup

## Installation

### Basic Installation (Required)
```bash
pip install pytesseract opencv-python pillow numpy
```

### Enhanced Installation (Recommended)
```bash
pip install pytesseract opencv-python pillow numpy easyocr mss keyboard
```

### System Requirements

#### Tesseract OCR Engine
- **Windows**: Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
- **Linux**: `sudo apt-get install tesseract-ocr`
- **Mac**: `brew install tesseract`

#### Windows Path Configuration
Add Tesseract to system PATH or set in code:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## Usage

### Enable Auto-Detection

1. Launch PoE Craft Helper
2. Click "📝 Manual Input Guide" button
3. Select "YES - Enable auto-detection"
4. Auto-detection is now active with Ctrl+D hotkey

### Detect Items

1. Hover over an item in Path of Exile
2. Press **Ctrl+D**
3. Wait for detection (0.5 second delay)
4. Item data automatically populates in the interface

### Configure Settings

1. Click "📝 Manual Input Guide"
2. Select "CANCEL - Configure detection settings"
3. Adjust:
   - OCR method (auto/tesseract/easyocr)
   - Confidence threshold
   - Image preprocessing
   - Capture delay

### Calibration

1. Take a screenshot of a PoE item tooltip
2. Open detection settings
3. Click "Calibrate with Image"
4. Select your screenshot
5. Review results and adjust settings

## Architecture

### Core Components

1. **ScreenCapture** - Handles screen capture operations
   - Full screen capture
   - Region detection for tooltips
   - Image enhancement for OCR

2. **OCREngine** - Multi-engine OCR processing
   - Tesseract OCR (fast, lightweight)
   - EasyOCR (better accuracy, GPU support)
   - Automatic method selection

3. **ItemParser** - PoE item format parsing
   - Regex patterns for all item properties
   - Modifier categorization
   - Item type identification

4. **AutoDetector** - Main detection orchestrator
   - Coordinates capture, OCR, and parsing
   - Confidence validation
   - Multi-method fallback

5. **AutoDetectionUI** - UI integration
   - Hotkey management
   - Settings dialog
   - Status updates

## Troubleshooting

### Detection Not Working

1. **Install all dependencies**: Ensure Tesseract is installed and in PATH
2. **Run as administrator**: Keyboard module may require admin rights
3. **Adjust confidence threshold**: Lower if no items detected
4. **Enable preprocessing**: Improves detection on dark backgrounds
5. **Try different OCR method**: EasyOCR often works better

### Poor Accuracy

1. **Calibrate with your setup**: Use actual screenshots from your game
2. **Adjust capture delay**: Give tooltip time to fully appear
3. **Check resolution**: Works best at 1920x1080 or higher
4. **Disable UI scaling**: Windows display scaling can affect detection

### Performance Issues

1. **Use Tesseract only**: Faster but less accurate
2. **Disable preprocessing**: Reduces CPU usage
3. **Install mss**: Faster screen capture
4. **Use GPU with EasyOCR**: Significant speed improvement

## API Reference

### Basic Usage
```python
from auto_detection import AutoDetector

detector = AutoDetector()
item = detector.detect_item_at_cursor()

if item:
    print(f"Detected: {item.base_type}")
    print(f"Modifiers: {item.modifiers}")
```

### Custom Configuration
```python
detector = AutoDetector(ocr_method='easyocr')
detector.settings['confidence_threshold'] = 0.7
detector.settings['enable_preprocessing'] = True
```

### UI Integration
```python
from auto_detection import setup_auto_detection

# In your tkinter app
detection_ui = setup_auto_detection(self)
```

## Technical Details

### Tooltip Detection Algorithm
1. Convert screenshot to grayscale
2. Apply threshold to find dark regions
3. Find contours matching tooltip dimensions
4. Validate aspect ratio and interior darkness
5. Extract tooltip region for OCR

### OCR Preprocessing
1. Denoise with fastNlMeans
2. Enhance contrast with CLAHE
3. Resize 2x for better character recognition
4. Invert if light text on dark background

### Confidence Scoring
- Based on OCR engine confidence
- Validated against expected patterns
- Modifier count validation
- Item type verification

## Future Enhancements

- [ ] Support for more item types (prophecies, etc.)
- [ ] Multi-language support
- [ ] Cloud-based OCR option
- [ ] Machine learning for better accuracy
- [ ] Batch detection mode
- [ ] Trade macro integration