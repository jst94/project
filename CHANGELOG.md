# Changelog

## [3.26.0] - 2025-06-26

### Updated
- Updated version number to match Path of Exile 3.26 (Secrets of the Atlas)
- Fixed missing import for DEFAULT_PRICES in market_api.py
- Replaced bare except clauses with proper Exception handling
- Added logging import to league_config.py for better error handling
- Code quality improvements and modernization

### Features
- **Separated Flask Crafting Module**: Flask crafting is now a dedicated module with:
  - Specialized UI optimized for flask crafting workflow
  - Complete flask modifier database with all prefixes/suffixes
  - Flask type detection (Life, Mana, Utility, Unique, etc.)
  - Advanced simulation engine for testing strategies
  - OCR support for flask detection from screenshots
  - Strategy comparison and optimization tools
- **Main Interface Updates**: 
  - Removed flask crafting from gear/armour methods
  - Added "⚗️ Flask Crafting" button to launch specialized tool
  - Cleaner separation between equipment and flask crafting
- **Manual Detection Integration**:
  - Auto-detection unavailable message with manual fallback options
  - Comprehensive manual input dialogs for both gear and flasks
  - Detailed guides for item identification and modifier recognition
  - Quick-fill buttons and examples for common items
- **Auto-Detection Module** (NEW):
  - Complete OCR-based item detection system
  - Screen capture with tooltip recognition
  - Multiple OCR engines (Tesseract, EasyOCR)
  - Hotkey support (Ctrl+D) for quick detection
  - Confidence scoring and validation
  - Calibration tools for optimization
  - Intelligent item parsing for all PoE formats
  - Settings dialog with preprocessing options

### Technical Improvements
- Improved exception handling throughout the codebase
- Better error logging instead of print statements
- Maintained compatibility with current league API endpoints

## [2.0.0] - Previous Version
- AI-powered crafting assistant
- Real-time market analysis
- OCR item detection
- Comprehensive session tracking