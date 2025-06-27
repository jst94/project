"""
Simplified Auto-Detection Module for Path of Exile Items
A more robust implementation with better error handling and fallbacks
"""

import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageGrab
import re
import time
import threading
import logging
from typing import Dict, List, Optional, Tuple

# Configure logging
logger = logging.getLogger(__name__)

# Check for optional dependencies
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    logger.warning("keyboard module not available. Install with: pip install keyboard")

try:
    import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False
    logger.warning("mss module not available. Install with: pip install mss")

# Global flag to track if auto-detection is available
AUTO_DETECTION_AVAILABLE = True

class SimpleItemDetector:
    """Simplified item detector that focuses on reliability"""
    
    def __init__(self):
        self.hotkey_active = False
        self.app_instance = None
        
        # Basic patterns for PoE items
        self.item_patterns = {
            'item_level': r'Item Level:\s*(\d+)',
            'quality': r'Quality:\s*\+?(\d+)%',
            'rarity': r'Rarity:\s*(Normal|Magic|Rare|Unique)',
            'base_type': r'^([A-Z][a-zA-Z\s]+(?:Sword|Axe|Mace|Bow|Wand|Dagger|Claw|Staff|Sceptre|Helmet|Armour|Gloves|Boots|Shield|Ring|Amulet|Belt|Flask))$',
            'modifier': r'^[\+\-]?\d+.*|^\w+.*increased.*|^\w+.*to.*|^Adds.*|^(\d+)% increased.*'
        }
    
    def setup_hotkey(self, app_instance, hotkey='ctrl+d'):
        """Setup hotkey detection"""
        self.app_instance = app_instance
        
        if not KEYBOARD_AVAILABLE:
            messagebox.showerror("Error", 
                               "Keyboard module not available.\n\n"
                               "Install with: pip install keyboard\n\n"
                               "Auto-detection hotkey will not work.")
            return False
        
        try:
            def on_hotkey():
                if not self.hotkey_active:
                    self.hotkey_active = True
                    thread = threading.Thread(target=self._detect_async)
                    thread.daemon = True
                    thread.start()
            
            keyboard.add_hotkey(hotkey, on_hotkey)
            logger.info(f"Hotkey {hotkey} registered successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup hotkey: {e}")
            messagebox.showerror("Hotkey Error", f"Failed to setup hotkey {hotkey}:\n{e}")
            return False
    
    def _detect_async(self):
        """Perform detection asynchronously"""
        try:
            if self.app_instance:
                self.app_instance.update_status("Detecting item...")
            
            # Small delay to allow tooltip to stabilize
            time.sleep(0.3)
            
            # Capture screen
            screenshot = self._capture_screen()
            if screenshot is None:
                if self.app_instance:
                    self.app_instance.update_status("Screen capture failed")
                return
            
            # Extract text
            text = self._extract_text_from_image(screenshot)
            if not text.strip():
                if self.app_instance:
                    self.app_instance.update_status("No text detected")
                return
            
            # Parse item data
            item_data = self._parse_item_text(text)
            
            if item_data and self.app_instance:
                self._update_app_with_item(item_data)
                self.app_instance.update_status(f"Detected: {item_data.get('base_type', 'Unknown item')}")
            else:
                if self.app_instance:
                    self.app_instance.update_status("No item detected")
                    
        except Exception as e:
            logger.error(f"Detection error: {e}")
            if self.app_instance:
                self.app_instance.update_status(f"Detection error: {str(e)}")
        finally:
            self.hotkey_active = False
    
    def _capture_screen(self):
        """Capture the current screen"""
        try:
            if MSS_AVAILABLE:
                # Use MSS for faster capture
                with mss.mss() as sct:
                    monitor = sct.monitors[1]  # Primary monitor
                    screenshot = sct.grab(monitor)
                    img = np.array(screenshot)
                    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                # Fallback to PIL
                screenshot = ImageGrab.grab()
                return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                
        except Exception as e:
            logger.error(f"Screen capture failed: {e}")
            return None
    
    def _extract_text_from_image(self, image):
        """Extract text from image using OCR"""
        try:
            # Convert to PIL Image for pytesseract
            if isinstance(image, np.ndarray):
                image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            else:
                image_pil = image
            
            # Use pytesseract to extract text
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image_pil, config=custom_config)
            
            return text
            
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return ""
    
    def _parse_item_text(self, text):
        """Parse OCR text to extract item information"""
        lines = text.strip().split('\n')
        item_data = {
            'base_type': '',
            'item_level': None,
            'quality': None,
            'rarity': 'Normal',
            'modifiers': []
        }
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for item level
            match = re.search(self.item_patterns['item_level'], line, re.I)
            if match:
                item_data['item_level'] = int(match.group(1))
                continue
            
            # Check for quality
            match = re.search(self.item_patterns['quality'], line, re.I)
            if match:
                item_data['quality'] = int(match.group(1))
                continue
            
            # Check for rarity
            match = re.search(self.item_patterns['rarity'], line, re.I)
            if match:
                item_data['rarity'] = match.group(1)
                continue
            
            # Try to identify base type (look for weapon/armor names)
            if not item_data['base_type']:
                base_types = [
                    'sword', 'axe', 'mace', 'bow', 'wand', 'dagger', 'claw', 'staff', 'sceptre',
                    'helmet', 'armour', 'gloves', 'boots', 'shield', 'ring', 'amulet', 'belt', 'flask'
                ]
                
                line_lower = line.lower()
                for base_type in base_types:
                    if base_type in line_lower and len(line) > 3:
                        item_data['base_type'] = line
                        break
            
            # Check for modifiers (lines with numbers, percentages, or "increased")
            if re.search(self.item_patterns['modifier'], line, re.I):
                if line not in item_data['modifiers']:
                    item_data['modifiers'].append(line)
        
        # Only return if we found something useful
        if item_data['base_type'] or item_data['modifiers'] or item_data['item_level']:
            return item_data
        
        return None
    
    def _update_app_with_item(self, item_data):
        """Update the application with detected item data"""
        try:
            # Update base item field
            if hasattr(self.app_instance, 'base_entry') and item_data.get('base_type'):
                self.app_instance.base_entry.delete(0, 'end')
                self.app_instance.base_entry.insert(0, item_data['base_type'])
            
            # Update item level
            if hasattr(self.app_instance, 'ilvl_entry') and item_data.get('item_level'):
                self.app_instance.ilvl_entry.delete(0, 'end')
                self.app_instance.ilvl_entry.insert(0, str(item_data['item_level']))
            
            # Update modifiers
            if hasattr(self.app_instance, 'target_text') and item_data.get('modifiers'):
                self.app_instance.target_text.delete('1.0', 'end')
                for modifier in item_data['modifiers']:
                    self.app_instance.target_text.insert('end', f"{modifier}\n")
                    
        except Exception as e:
            logger.error(f"Failed to update app: {e}")

# Global detector instance
_detector = None

def setup_auto_detection(app_instance):
    """Setup auto-detection for an application instance"""
    global _detector
    
    if not AUTO_DETECTION_AVAILABLE:
        messagebox.showerror("Auto-Detection Not Available", 
                           "Auto-detection requires additional libraries.\n\n"
                           "Please run: python fix_auto_detection.py")
        return None
    
    try:
        _detector = SimpleItemDetector()
        
        if _detector.setup_hotkey(app_instance):
            messagebox.showinfo("Auto-Detection Enabled", 
                              "Auto-detection is now enabled!\n\n"
                              "How to use:\n"
                              "1. Hover over an item in Path of Exile\n"
                              "2. Press Ctrl+D\n"
                              "3. Item will be detected and populated\n\n"
                              "Note: Game should be in windowed or borderless mode.")
            return _detector
        else:
            return None
            
    except Exception as e:
        logger.error(f"Failed to setup auto-detection: {e}")
        messagebox.showerror("Setup Error", f"Failed to setup auto-detection:\n{e}")
        return None

def test_auto_detection():
    """Test if auto-detection is working"""
    try:
        # Test basic imports
        import cv2
        import pytesseract
        from PIL import ImageGrab
        
        # Test tesseract
        pytesseract.get_tesseract_version()
        
        # Test screen capture
        screenshot = ImageGrab.grab()
        
        return True, "Auto-detection test passed"
        
    except Exception as e:
        return False, f"Auto-detection test failed: {e}"

# Check if everything is available on import
try:
    import cv2
    import pytesseract
    from PIL import ImageGrab
    
    # Test tesseract availability
    pytesseract.get_tesseract_version()
    
except ImportError as e:
    AUTO_DETECTION_AVAILABLE = False
    logger.error(f"Auto-detection not available: {e}")
except Exception as e:
    AUTO_DETECTION_AVAILABLE = False
    logger.error(f"Auto-detection setup failed: {e}")

if __name__ == "__main__":
    # Test the module
    success, message = test_auto_detection()
    print(f"Auto-detection test: {message}")
    
    if success:
        print("\nAuto-detection is ready!")
        print("Keyboard available:", KEYBOARD_AVAILABLE)
        print("MSS available:", MSS_AVAILABLE)
    else:
        print("\nTo fix auto-detection, run: python fix_auto_detection.py")