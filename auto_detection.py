"""
Auto-Detection Module for Path of Exile Items
Provides screen capture and OCR functionality for automatic item detection
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageGrab
import re
from typing import Dict, List, Optional, Tuple, Union
import logging
from dataclasses import dataclass
import threading
import time
import json

# Configure logging
logger = logging.getLogger(__name__)

# Try to import additional libraries for better detection
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    logger.warning("EasyOCR not available. Install with: pip install easyocr")

try:
    import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False
    logger.warning("MSS not available. Install with: pip install mss")


@dataclass
class DetectedItem:
    """Represents a detected PoE item"""
    item_type: str  # weapon, armour, jewelry, flask, currency, etc.
    base_type: str  # e.g., "Titanium Spirit Shield"
    rarity: str  # normal, magic, rare, unique
    item_level: Optional[int] = None
    quality: Optional[int] = None
    sockets: Optional[str] = None
    modifiers: List[str] = None
    implicit_mods: List[str] = None
    explicit_mods: List[str] = None
    crafted_mods: List[str] = None
    corrupted: bool = False
    influenced: Optional[str] = None  # shaper, elder, crusader, etc.
    raw_text: str = ""
    confidence: float = 0.0
    screenshot_region: Tuple[int, int, int, int] = None


class ScreenCapture:
    """Handles screen capture for item detection"""
    
    def __init__(self):
        try:
            self.mss = mss.mss() if MSS_AVAILABLE else None
        except Exception as e:
            logger.warning(f"Failed to initialize MSS: {e}")
            self.mss = None
        
    def capture_screen_region(self, x: int, y: int, width: int, height: int) -> np.ndarray:
        """Capture a specific region of the screen"""
        if self.mss:
            # Use mss for faster capture
            monitor = {"left": x, "top": y, "width": width, "height": height}
            screenshot = self.mss.grab(monitor)
            img = np.array(screenshot)
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        else:
            # Fallback to PIL
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def capture_fullscreen(self) -> np.ndarray:
        """Capture the entire screen"""
        if self.mss:
            screenshot = self.mss.grab(self.mss.monitors[1])
            img = np.array(screenshot)
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        else:
            screenshot = ImageGrab.grab()
            return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def find_tooltip_region(self, screenshot: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Find PoE item tooltip region in screenshot"""
        # Convert to grayscale
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        
        # PoE tooltips have distinctive borders
        # Look for dark backgrounds with light borders
        _, binary = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by size and aspect ratio
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # PoE tooltips are typically:
            # - Width: 300-500 pixels
            # - Height: 200-800 pixels
            # - Aspect ratio: 0.4 to 0.8
            if 300 <= w <= 500 and 200 <= h <= 800:
                aspect_ratio = w / h
                if 0.3 <= aspect_ratio <= 0.8:
                    # Additional validation: check for dark interior
                    roi = gray[y:y+h, x:x+w]
                    mean_val = cv2.mean(roi)[0]
                    if mean_val < 50:  # Dark interior
                        return (x, y, w, h)
        
        return None
    
    def enhance_image_for_ocr(self, image: np.ndarray) -> np.ndarray:
        """Enhance image for better OCR results"""
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Increase contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        
        # Resize for better OCR (PoE text is small)
        height, width = enhanced.shape
        scale = 2.0  # Double the size
        resized = cv2.resize(enhanced, (int(width * scale), int(height * scale)), 
                           interpolation=cv2.INTER_CUBIC)
        
        # Invert if text is light on dark background
        mean_val = cv2.mean(resized)[0]
        if mean_val < 128:
            resized = cv2.bitwise_not(resized)
        
        return resized


class ItemParser:
    """Parses PoE item text into structured data"""
    
    # Regex patterns for parsing
    PATTERNS = {
        'item_level': r'Item Level:\s*(\d+)',
        'quality': r'Quality:\s*\+?(\d+)%',
        'sockets': r'Sockets:\s*([RGBWAD\-]+)',
        'rarity': r'Rarity:\s*(Normal|Magic|Rare|Unique)',
        'corrupted': r'Corrupted',
        'influenced': r'(Shaper|Elder|Crusader|Hunter|Redeemer|Warlord)',
        'implicit_separator': r'-{3,}',
        'crafted_mod': r'(?:Can have up to|\(crafted\))',
        'modifier_line': r'^[\+\-]?\d+.*|^\w+.*increased.*|^\w+.*to.*|^Adds.*|^Gain.*',
    }
    
    # Item type keywords
    ITEM_TYPES = {
        'weapon': ['sword', 'axe', 'mace', 'bow', 'wand', 'dagger', 'claw', 'staff', 'sceptre'],
        'armour': ['helmet', 'body armour', 'gloves', 'boots', 'shield', 'quiver'],
        'jewelry': ['ring', 'amulet', 'belt'],
        'flask': ['flask'],
        'jewel': ['jewel'],
        'map': ['map'],
        'currency': ['orb', 'essence', 'fossil', 'shard', 'splinter'],
    }
    
    def parse_item_text(self, text: str) -> DetectedItem:
        """Parse OCR text into structured item data"""
        lines = text.strip().split('\n')
        
        item = DetectedItem(
            item_type='unknown',
            base_type='',
            rarity='normal',
            modifiers=[],
            implicit_mods=[],
            explicit_mods=[],
            crafted_mods=[],
            raw_text=text
        )
        
        # Extract basic properties
        for line in lines:
            # Item level
            if match := re.search(self.PATTERNS['item_level'], line, re.I):
                item.item_level = int(match.group(1))
            
            # Quality
            elif match := re.search(self.PATTERNS['quality'], line, re.I):
                item.quality = int(match.group(1))
            
            # Sockets
            elif match := re.search(self.PATTERNS['sockets'], line, re.I):
                item.sockets = match.group(1)
            
            # Rarity
            elif match := re.search(self.PATTERNS['rarity'], line, re.I):
                item.rarity = match.group(1).lower()
            
            # Corrupted
            elif re.search(self.PATTERNS['corrupted'], line, re.I):
                item.corrupted = True
            
            # Influenced
            elif match := re.search(self.PATTERNS['influenced'], line, re.I):
                item.influenced = match.group(1)
        
        # Determine item type and base
        item.item_type, item.base_type = self._identify_item_type(lines)
        
        # Parse modifiers
        self._parse_modifiers(lines, item)
        
        return item
    
    def _identify_item_type(self, lines: List[str]) -> Tuple[str, str]:
        """Identify item type and base from text lines"""
        # Usually the item base is in the first few lines
        for line in lines[:5]:
            line_lower = line.lower()
            
            # Check each item type
            for item_type, keywords in self.ITEM_TYPES.items():
                for keyword in keywords:
                    if keyword in line_lower:
                        return item_type, line.strip()
        
        # Check for specific bases
        base_candidates = []
        for line in lines[:5]:
            # Skip property lines
            if any(prop in line.lower() for prop in ['rarity:', 'sockets:', 'item level:', 'quality:']):
                continue
            # Skip empty lines
            if line.strip():
                base_candidates.append(line.strip())
        
        if base_candidates:
            return 'unknown', base_candidates[0]
        
        return 'unknown', 'Unknown Item'
    
    def _parse_modifiers(self, lines: List[str], item: DetectedItem):
        """Parse item modifiers from text lines"""
        # Find separator positions
        separator_indices = []
        for i, line in enumerate(lines):
            if re.search(self.PATTERNS['implicit_separator'], line):
                separator_indices.append(i)
        
        # Categorize modifiers
        current_section = 'header'
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check for section changes
            if i in separator_indices:
                if current_section == 'header':
                    current_section = 'implicit'
                elif current_section == 'implicit':
                    current_section = 'explicit'
                continue
            
            # Check if it's a modifier line
            if re.match(self.PATTERNS['modifier_line'], line):
                # Check if crafted
                if re.search(self.PATTERNS['crafted_mod'], line):
                    item.crafted_mods.append(line)
                elif current_section == 'implicit':
                    item.implicit_mods.append(line)
                elif current_section == 'explicit':
                    item.explicit_mods.append(line)
                
                # Add to general modifiers list
                item.modifiers.append(line)


class OCREngine:
    """Handles OCR processing with multiple backends"""
    
    def __init__(self, use_easyocr: bool = True):
        self.use_easyocr = use_easyocr and EASYOCR_AVAILABLE
        
        if self.use_easyocr:
            try:
                self.reader = easyocr.Reader(['en'], gpu=True)
                logger.info("EasyOCR initialized with GPU support")
            except:
                self.reader = easyocr.Reader(['en'], gpu=False)
                logger.info("EasyOCR initialized with CPU support")
        
        # Configure Tesseract
        self.tesseract_config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+-%():,. '
    
    def extract_text(self, image: np.ndarray, method: str = 'auto') -> Tuple[str, float]:
        """Extract text from image with confidence score"""
        if method == 'auto':
            if self.use_easyocr:
                return self._extract_with_easyocr(image)
            else:
                return self._extract_with_tesseract(image)
        elif method == 'tesseract':
            return self._extract_with_tesseract(image)
        elif method == 'easyocr' and self.use_easyocr:
            return self._extract_with_easyocr(image)
        else:
            return self._extract_with_tesseract(image)
    
    def _extract_with_tesseract(self, image: np.ndarray) -> Tuple[str, float]:
        """Extract text using Tesseract OCR"""
        try:
            # Get detailed data
            data = pytesseract.image_to_data(image, config=self.tesseract_config, output_type=pytesseract.Output.DICT)
            
            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Get text
            text = pytesseract.image_to_string(image, config=self.tesseract_config)
            
            return text.strip(), avg_confidence / 100.0
        except Exception as e:
            logger.error(f"Tesseract OCR failed: {e}")
            return "", 0.0
    
    def _extract_with_easyocr(self, image: np.ndarray) -> Tuple[str, float]:
        """Extract text using EasyOCR"""
        try:
            results = self.reader.readtext(image)
            
            if not results:
                return "", 0.0
            
            # Combine text and calculate average confidence
            text_lines = []
            confidences = []
            
            for (bbox, text, conf) in results:
                text_lines.append(text)
                confidences.append(conf)
            
            full_text = '\n'.join(text_lines)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return full_text.strip(), avg_confidence
        except Exception as e:
            logger.error(f"EasyOCR failed: {e}")
            return "", 0.0


class AutoDetector:
    """Main auto-detection system for PoE items"""
    
    def __init__(self, ocr_method: str = 'auto'):
        self.screen_capture = ScreenCapture()
        self.ocr_engine = OCREngine()
        self.item_parser = ItemParser()
        self.ocr_method = ocr_method
        
        # Detection settings
        self.settings = {
            'capture_delay': 0.5,  # Delay after hotkey press
            'max_tooltip_wait': 3.0,  # Max wait for tooltip to appear
            'confidence_threshold': 0.6,  # Minimum OCR confidence
            'enable_preprocessing': True,
            'multi_method_ocr': True,  # Try multiple OCR methods
        }
    
    def detect_item_at_cursor(self) -> Optional[DetectedItem]:
        """Detect item at current cursor position"""
        # Give user time to hover over item
        time.sleep(self.settings['capture_delay'])
        
        # Capture full screen
        screenshot = self.screen_capture.capture_fullscreen()
        
        # Find tooltip region
        tooltip_region = self.screen_capture.find_tooltip_region(screenshot)
        
        if not tooltip_region:
            logger.warning("No tooltip detected on screen")
            return None
        
        # Extract tooltip image
        x, y, w, h = tooltip_region
        tooltip_img = screenshot[y:y+h, x:x+w]
        
        # Process and detect
        return self._process_tooltip_image(tooltip_img, tooltip_region)
    
    def detect_item_from_image(self, image_path: str) -> Optional[DetectedItem]:
        """Detect item from saved image file"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                logger.error(f"Failed to load image: {image_path}")
                return None
            
            # Try to find tooltip region or use whole image
            tooltip_region = self.screen_capture.find_tooltip_region(image)
            
            if tooltip_region:
                x, y, w, h = tooltip_region
                tooltip_img = image[y:y+h, x:x+w]
            else:
                tooltip_img = image
                tooltip_region = (0, 0, image.shape[1], image.shape[0])
            
            return self._process_tooltip_image(tooltip_img, tooltip_region)
            
        except Exception as e:
            logger.error(f"Error detecting item from image: {e}")
            return None
    
    def _process_tooltip_image(self, tooltip_img: np.ndarray, region: Tuple[int, int, int, int]) -> Optional[DetectedItem]:
        """Process tooltip image and extract item data"""
        best_result = None
        best_confidence = 0.0
        
        # Enhance image if enabled
        if self.settings['enable_preprocessing']:
            processed_img = self.screen_capture.enhance_image_for_ocr(tooltip_img)
        else:
            processed_img = tooltip_img
        
        # Try multiple OCR methods if enabled
        if self.settings['multi_method_ocr']:
            methods = ['tesseract', 'easyocr'] if EASYOCR_AVAILABLE else ['tesseract']
        else:
            methods = [self.ocr_method]
        
        for method in methods:
            # Extract text
            text, confidence = self.ocr_engine.extract_text(processed_img, method)
            
            if confidence < self.settings['confidence_threshold']:
                continue
            
            # Parse item
            item = self.item_parser.parse_item_text(text)
            item.confidence = confidence
            item.screenshot_region = region
            
            # Keep best result
            if confidence > best_confidence:
                best_result = item
                best_confidence = confidence
        
        if best_result:
            logger.info(f"Item detected: {best_result.base_type} (confidence: {best_confidence:.2%})")
        else:
            logger.warning("Failed to detect item with sufficient confidence")
        
        return best_result
    
    def calibrate_detection(self, test_image_path: str) -> Dict:
        """Calibrate detection settings using a test image"""
        results = {}
        
        # Test different preprocessing options
        for preprocess in [True, False]:
            self.settings['enable_preprocessing'] = preprocess
            
            # Test different OCR methods
            for method in ['tesseract', 'easyocr']:
                if method == 'easyocr' and not EASYOCR_AVAILABLE:
                    continue
                
                start_time = time.time()
                item = self.detect_item_from_image(test_image_path)
                detection_time = time.time() - start_time
                
                key = f"{method}_{'preprocessed' if preprocess else 'raw'}"
                results[key] = {
                    'success': item is not None,
                    'confidence': item.confidence if item else 0.0,
                    'time': detection_time,
                    'item_type': item.item_type if item else None,
                    'base_type': item.base_type if item else None,
                    'modifiers_count': len(item.modifiers) if item else 0
                }
        
        return results


class AutoDetectionUI:
    """UI integration for auto-detection"""
    
    def __init__(self, parent_app):
        self.app = parent_app
        self.detector = AutoDetector()
        self.detection_thread = None
        self.hotkey_enabled = False
        
    def enable_hotkey_detection(self, hotkey: str = 'ctrl+d'):
        """Enable hotkey for item detection"""
        try:
            import keyboard
            
            def on_hotkey():
                if self.detection_thread is None or not self.detection_thread.is_alive():
                    self.detection_thread = threading.Thread(target=self._detect_item_async)
                    self.detection_thread.start()
            
            keyboard.add_hotkey(hotkey, on_hotkey)
            self.hotkey_enabled = True
            logger.info(f"Hotkey detection enabled: {hotkey}")
            
        except ImportError:
            logger.error("Keyboard module not available. Install with: pip install keyboard")
            return False
        
        return True
    
    def _detect_item_async(self):
        """Detect item asynchronously"""
        try:
            # Update UI to show detection in progress
            self.app.update_status("Detecting item...")
            
            # Perform detection
            item = self.detector.detect_item_at_cursor()
            
            if item:
                # Update UI with detected item
                self._update_ui_with_item(item)
                self.app.update_status(f"Detected: {item.base_type} ({item.confidence:.0%} confidence)")
            else:
                self.app.update_status("No item detected")
                
        except Exception as e:
            logger.error(f"Detection error: {e}")
            self.app.update_status(f"Detection failed: {str(e)}")
    
    def _update_ui_with_item(self, item: DetectedItem):
        """Update application UI with detected item data"""
        # Update base item field
        if hasattr(self.app, 'base_entry'):
            self.app.base_entry.delete(0, 'end')
            self.app.base_entry.insert(0, item.base_type)
        
        # Update modifiers
        if hasattr(self.app, 'target_text'):
            self.app.target_text.delete('1.0', 'end')
            # Add implicit mods
            for mod in item.implicit_mods:
                self.app.target_text.insert('end', f"{mod}\n")
            # Add explicit mods
            for mod in item.explicit_mods:
                self.app.target_text.insert('end', f"{mod}\n")
        
        # Update item level
        if hasattr(self.app, 'ilvl_entry') and item.item_level:
            self.app.ilvl_entry.delete(0, 'end')
            self.app.ilvl_entry.insert(0, str(item.item_level))
        
        # Store full item data
        self.app.detected_item = item
    
    def show_detection_settings(self):
        """Show detection settings dialog"""
        import tkinter as tk
        from tkinter import ttk, messagebox
        
        settings_window = tk.Toplevel(self.app.root)
        settings_window.title("Auto-Detection Settings")
        settings_window.geometry("500x600")
        settings_window.transient(self.app.root)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(settings_window, text="Detection Settings", padding=10)
        settings_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # OCR method
        ttk.Label(settings_frame, text="OCR Method:").grid(row=0, column=0, sticky='w', pady=5)
        ocr_var = tk.StringVar(value=self.detector.ocr_method)
        ocr_menu = ttk.Combobox(settings_frame, textvariable=ocr_var, 
                               values=['auto', 'tesseract', 'easyocr'], state='readonly')
        ocr_menu.grid(row=0, column=1, sticky='ew', pady=5)
        
        # Confidence threshold
        ttk.Label(settings_frame, text="Confidence Threshold:").grid(row=1, column=0, sticky='w', pady=5)
        conf_var = tk.DoubleVar(value=self.detector.settings['confidence_threshold'])
        conf_scale = ttk.Scale(settings_frame, from_=0.1, to=1.0, variable=conf_var, orient='horizontal')
        conf_scale.grid(row=1, column=1, sticky='ew', pady=5)
        conf_label = ttk.Label(settings_frame, text=f"{conf_var.get():.0%}")
        conf_label.grid(row=1, column=2, pady=5)
        
        def update_conf_label(*args):
            conf_label.config(text=f"{conf_var.get():.0%}")
        conf_var.trace('w', update_conf_label)
        
        # Preprocessing
        preprocess_var = tk.BooleanVar(value=self.detector.settings['enable_preprocessing'])
        ttk.Checkbutton(settings_frame, text="Enable Image Preprocessing", 
                       variable=preprocess_var).grid(row=2, column=0, columnspan=2, sticky='w', pady=5)
        
        # Multi-method OCR
        multi_var = tk.BooleanVar(value=self.detector.settings['multi_method_ocr'])
        ttk.Checkbutton(settings_frame, text="Try Multiple OCR Methods", 
                       variable=multi_var).grid(row=3, column=0, columnspan=2, sticky='w', pady=5)
        
        # Capture delay
        ttk.Label(settings_frame, text="Capture Delay (sec):").grid(row=4, column=0, sticky='w', pady=5)
        delay_var = tk.DoubleVar(value=self.detector.settings['capture_delay'])
        delay_spin = ttk.Spinbox(settings_frame, from_=0.1, to=3.0, increment=0.1, 
                                textvariable=delay_var, width=10)
        delay_spin.grid(row=4, column=1, sticky='w', pady=5)
        
        # Test detection
        test_frame = ttk.LabelFrame(settings_window, text="Test Detection", padding=10)
        test_frame.pack(fill='x', padx=10, pady=5)
        
        def test_detection():
            messagebox.showinfo("Test Detection", 
                              "Hover over an item in PoE and press OK.\n"
                              "The detection will start after the capture delay.")
            item = self.detector.detect_item_at_cursor()
            if item:
                result = f"Detected: {item.base_type}\n"
                result += f"Type: {item.item_type}\n"
                result += f"Rarity: {item.rarity}\n"
                result += f"Confidence: {item.confidence:.0%}\n"
                result += f"Modifiers: {len(item.modifiers)}"
                messagebox.showinfo("Detection Result", result)
            else:
                messagebox.showwarning("Detection Failed", "No item detected")
        
        ttk.Button(test_frame, text="Test Detection", command=test_detection).pack(pady=5)
        
        # Calibration
        calib_frame = ttk.LabelFrame(settings_window, text="Calibration", padding=10)
        calib_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(calib_frame, text="Use a screenshot of a PoE item tooltip for calibration").pack()
        
        def calibrate():
            from tkinter import filedialog
            filename = filedialog.askopenfilename(
                title="Select Item Screenshot",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
            )
            if filename:
                results = self.detector.calibrate_detection(filename)
                
                # Show results
                result_text = "Calibration Results:\n\n"
                for method, data in results.items():
                    result_text += f"{method}:\n"
                    result_text += f"  Success: {data['success']}\n"
                    result_text += f"  Confidence: {data['confidence']:.0%}\n"
                    result_text += f"  Time: {data['time']:.2f}s\n"
                    result_text += f"  Modifiers: {data['modifiers_count']}\n\n"
                
                messagebox.showinfo("Calibration Complete", result_text)
        
        ttk.Button(calib_frame, text="Calibrate with Image", command=calibrate).pack(pady=5)
        
        # Save settings
        def save_settings():
            self.detector.ocr_method = ocr_var.get()
            self.detector.settings['confidence_threshold'] = conf_var.get()
            self.detector.settings['enable_preprocessing'] = preprocess_var.get()
            self.detector.settings['multi_method_ocr'] = multi_var.get()
            self.detector.settings['capture_delay'] = delay_var.get()
            
            # Save to file
            settings_file = "auto_detection_settings.json"
            with open(settings_file, 'w') as f:
                json.dump({
                    'ocr_method': self.detector.ocr_method,
                    'settings': self.detector.settings
                }, f, indent=2)
            
            messagebox.showinfo("Settings Saved", "Detection settings saved successfully")
            settings_window.destroy()
        
        # Buttons
        button_frame = tk.Frame(settings_window)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="Save", command=save_settings).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side='right')


# Convenience function for integration
def setup_auto_detection(app_instance):
    """Setup auto-detection for an application instance"""
    detection_ui = AutoDetectionUI(app_instance)
    
    # Try to enable hotkey
    if detection_ui.enable_hotkey_detection():
        app_instance.update_status("Auto-detection enabled (Ctrl+D)")
    
    return detection_ui