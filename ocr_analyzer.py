"""
OCR and Screenshot Analysis for Path of Exile Items
Automatically detects and analyzes items from screenshots
"""

import cv2
import numpy as np
import pytesseract
import re
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab
import json
from typing import Dict, List, Tuple, Optional
import threading
import time


class POEItemOCR:
    """OCR analyzer for Path of Exile item screenshots"""
    
    def __init__(self):
        # PoE item text patterns
        self.modifier_patterns = {
            'life': r'(?:\+)?(\d+) to maximum life',
            'energy_shield': r'(?:\+)?(\d+) to maximum energy shield',
            'mana': r'(?:\+)?(\d+) to maximum mana',
            'damage': r'adds (\d+) to (\d+) (\w+) damage',
            'resistance': r'(?:\+)?(\d+)% to (\w+) resistance',
            'attack_speed': r'(\d+)% increased attack speed',
            'cast_speed': r'(\d+)% increased cast speed',
            'critical_strike': r'(\d+)% increased critical strike',
            'accuracy': r'(?:\+)?(\d+) to accuracy rating',
            'strength': r'(?:\+)?(\d+) to strength',
            'dexterity': r'(?:\+)?(\d+) to dexterity',
            'intelligence': r'(?:\+)?(\d+) to intelligence',
        }
        
        # Item rarity colors (BGR format for OpenCV)
        self.rarity_colors = {
            'normal': [(200, 200, 200), (255, 255, 255)],    # White
            'magic': [(255, 100, 100), (255, 150, 150)],     # Blue
            'rare': [(0, 255, 255), (100, 255, 255)],        # Yellow
            'unique': [(0, 100, 200), (50, 150, 255)],       # Orange/Brown
        }
        
        # Configure tesseract (adjust path if needed)
        self.tesseract_config = '--psm 6 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%+:- '
        
    def capture_screen_region(self, x: int, y: int, width: int, height: int) -> Image.Image:
        """Capture a specific region of the screen"""
        try:
            # Use PIL to capture screen region
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            return screenshot
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None
            
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image for better OCR results"""
        try:
            # Convert PIL to OpenCV format
            img_array = np.array(image)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Convert to grayscale
            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            
            # Apply bilateral filter to reduce noise while preserving edges
            filtered = cv2.bilateralFilter(gray, 9, 75, 75)
            
            # Apply threshold to get binary image
            _, thresh = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Apply morphological operations to clean up
            kernel = np.ones((2, 2), np.uint8)
            cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            return cleaned
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
            
    def extract_text_from_image(self, image: np.ndarray) -> str:
        """Extract text using OCR"""
        try:
            # Use tesseract to extract text
            text = pytesseract.image_to_string(image, config=self.tesseract_config)
            return text.strip()
        except Exception as e:
            print(f"OCR extraction error: {e}")
            return ""
            
    def detect_item_rarity(self, image: Image.Image) -> str:
        """Detect item rarity based on text color"""
        try:
            img_array = np.array(image)
            img_hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            
            # Check for different rarity colors
            for rarity, (color_min, color_max) in self.rarity_colors.items():
                # Convert to HSV for better color detection
                hsv_min = cv2.cvtColor(np.uint8([[color_min]]), cv2.COLOR_BGR2HSV)[0][0]
                hsv_max = cv2.cvtColor(np.uint8([[color_max]]), cv2.COLOR_BGR2HSV)[0][0]
                
                # Create mask for color range
                mask = cv2.inRange(img_hsv, hsv_min, hsv_max)
                
                # If enough pixels match, this is likely the rarity
                if np.sum(mask) > 1000:  # Threshold for color detection
                    return rarity
                    
            return 'normal'  # Default to normal
            
        except Exception as e:
            print(f"Error detecting rarity: {e}")
            return 'unknown'
            
    def parse_item_modifiers(self, text: str) -> List[Dict]:
        """Parse modifiers from extracted text"""
        modifiers = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip().lower()
            if not line:
                continue
                
            # Check each modifier pattern
            for mod_type, pattern in self.modifier_patterns.items():
                matches = re.findall(pattern, line, re.IGNORECASE)
                if matches:
                    modifiers.append({
                        'type': mod_type,
                        'raw_text': line,
                        'values': matches[0] if isinstance(matches[0], tuple) else [matches[0]],
                        'tier': self.estimate_modifier_tier(mod_type, matches[0])
                    })
                    break
                    
        return modifiers
        
    def estimate_modifier_tier(self, mod_type: str, values) -> str:
        """Estimate modifier tier based on values"""
        # This is a simplified tier estimation
        # In a full implementation, you'd have comprehensive tier data
        tier_thresholds = {
            'life': [(120, 'T1'), (100, 'T2'), (80, 'T3'), (60, 'T4'), (0, 'T5')],
            'energy_shield': [(100, 'T1'), (80, 'T2'), (60, 'T3'), (40, 'T4'), (0, 'T5')],
            'damage': [(50, 'T1'), (40, 'T2'), (30, 'T3'), (20, 'T4'), (0, 'T5')],
        }
        
        if mod_type not in tier_thresholds:
            return 'Unknown'
            
        try:
            value = int(values) if not isinstance(values, tuple) else int(values[0])
            for threshold, tier in tier_thresholds[mod_type]:
                if value >= threshold:
                    return tier
        except (ValueError, IndexError):
            pass
            
        return 'T5'
        
    def analyze_item_screenshot(self, image_path: Optional[str] = None, 
                               screen_region: Optional[Tuple[int, int, int, int]] = None) -> Dict:
        """Analyze item from screenshot or screen capture"""
        try:
            # Get image
            if image_path:
                image = Image.open(image_path)
            elif screen_region:
                x, y, width, height = screen_region
                image = self.capture_screen_region(x, y, width, height)
            else:
                raise ValueError("Either image_path or screen_region must be provided")
                
            if image is None:
                return {'error': 'Failed to load image'}
                
            # Preprocess image
            processed_img = self.preprocess_image(image)
            if processed_img is None:
                return {'error': 'Failed to preprocess image'}
                
            # Extract text
            text = self.extract_text_from_image(processed_img)
            if not text:
                return {'error': 'No text extracted from image'}
                
            # Detect item rarity
            rarity = self.detect_item_rarity(image)
            
            # Parse modifiers
            modifiers = self.parse_item_modifiers(text)
            
            # Extract item name and base (first few lines usually)
            lines = text.split('\n')
            item_name = lines[0].strip() if lines else 'Unknown Item'
            item_base = lines[1].strip() if len(lines) > 1 else 'Unknown Base'
            
            return {
                'success': True,
                'item_name': item_name,
                'item_base': item_base,
                'rarity': rarity,
                'raw_text': text,
                'modifiers': modifiers,
                'modifier_count': len(modifiers),
                'analysis_timestamp': time.time()
            }
            
        except Exception as e:
            return {'error': f'Analysis failed: {e}'}
            
    def create_capture_overlay(self, callback_func) -> tk.Toplevel:
        """Create overlay for selecting screen region to capture"""
        overlay = tk.Toplevel()
        overlay.attributes('-alpha', 0.3)
        overlay.attributes('-topmost', True)
        overlay.attributes('-fullscreen', True)
        overlay.configure(bg='red')
        overlay.attributes('-transparentcolor', 'red')
        
        # Variables for selection
        self.selection_start = None
        self.selection_end = None
        self.selection_rect = None
        
        canvas = tk.Canvas(overlay, highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        def start_selection(event):
            self.selection_start = (event.x_root, event.y_root)
            
        def update_selection(event):
            if self.selection_start:
                self.selection_end = (event.x_root, event.y_root)
                # Clear previous rectangle
                canvas.delete('selection')
                # Draw new rectangle
                canvas.create_rectangle(
                    self.selection_start[0], self.selection_start[1],
                    self.selection_end[0], self.selection_end[1],
                    outline='yellow', width=2, tags='selection'
                )
                
        def finish_selection(event):
            if self.selection_start and self.selection_end:
                x1, y1 = self.selection_start
                x2, y2 = self.selection_end
                
                # Ensure x1,y1 is top-left
                x = min(x1, x2)
                y = min(y1, y2)
                width = abs(x2 - x1)
                height = abs(y2 - y1)
                
                overlay.destroy()
                callback_func((x, y, width, height))
                
        # Bind mouse events
        overlay.bind('<Button-1>', start_selection)
        overlay.bind('<B1-Motion>', update_selection)
        overlay.bind('<ButtonRelease-1>', finish_selection)
        
        # ESC to cancel
        overlay.bind('<Escape>', lambda e: overlay.destroy())
        overlay.focus_set()
        
        return overlay
        
    def auto_detect_item_tooltip(self) -> Optional[Dict]:
        """Automatically detect PoE item tooltip on screen"""
        try:
            # This is a placeholder for automatic tooltip detection
            # In a full implementation, you would:
            # 1. Take full screen screenshot
            # 2. Look for PoE tooltip patterns (specific colors, borders)
            # 3. Extract the tooltip region
            # 4. Analyze the extracted region
            
            # For now, return None to indicate manual selection needed
            return None
            
        except Exception as e:
            print(f"Auto-detection error: {e}")
            return None


class ItemDetectionGUI:
    """GUI interface for item detection and analysis"""
    
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.ocr_analyzer = POEItemOCR()
        self.detection_window = None
        
    def open_detection_window(self):
        """Open the item detection window"""
        if self.detection_window and self.detection_window.winfo_exists():
            self.detection_window.lift()
            return
            
        self.detection_window = tk.Toplevel(self.parent_app.root)
        self.detection_window.title("PoE Item Detection")
        self.detection_window.geometry("500x400")
        self.detection_window.attributes('-topmost', True)
        
        # Title
        tk.Label(self.detection_window, text="Path of Exile Item Detection", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(self.detection_window)
        button_frame.pack(pady=10)
        
        # Screen capture button
        tk.Button(button_frame, text="Capture Screen Region", 
                 command=self.capture_screen_region,
                 bg='#4CAF50', fg='white', width=20).pack(pady=5)
        
        # File upload button
        tk.Button(button_frame, text="Analyze Image File", 
                 command=self.analyze_image_file,
                 bg='#2196F3', fg='white', width=20).pack(pady=5)
        
        # Auto-detect button (placeholder)
        tk.Button(button_frame, text="Auto-Detect Tooltip", 
                 command=self.auto_detect_tooltip,
                 bg='#FF9800', fg='white', width=20).pack(pady=5)
        
        # Results area
        tk.Label(self.detection_window, text="Detection Results:", 
                font=("Arial", 12, "bold")).pack(anchor='w', padx=10, pady=(20,5))
        
        self.results_text = tk.Text(self.detection_window, height=15, width=60)
        self.results_text.pack(fill='both', expand=True, padx=10, pady=5)
        
    def capture_screen_region(self):
        """Initiate screen region capture"""
        self.detection_window.withdraw()  # Hide detection window temporarily
        
        def on_region_selected(region):
            self.detection_window.deiconify()  # Show detection window again
            result = self.ocr_analyzer.analyze_item_screenshot(screen_region=region)
            self.display_results(result)
            
        self.ocr_analyzer.create_capture_overlay(on_region_selected)
        
    def analyze_image_file(self):
        """Analyze uploaded image file"""
        file_path = filedialog.askopenfilename(
            title="Select PoE Item Screenshot",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )
        
        if file_path:
            result = self.ocr_analyzer.analyze_item_screenshot(image_path=file_path)
            self.display_results(result)
            
    def auto_detect_tooltip(self):
        """Attempt automatic tooltip detection"""
        result = self.ocr_analyzer.auto_detect_item_tooltip()
        if result:
            self.display_results(result)
        else:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Auto-detection not available yet. Please use manual capture methods.")
            
    def display_results(self, result: Dict):
        """Display analysis results"""
        self.results_text.delete(1.0, tk.END)
        
        if 'error' in result:
            self.results_text.insert(tk.END, f"Error: {result['error']}")
            return
            
        # Display item information
        output = f"ITEM ANALYSIS RESULTS\n"
        output += "=" * 40 + "\n\n"
        
        if 'item_name' in result:
            output += f"Item Name: {result['item_name']}\n"
        if 'item_base' in result:
            output += f"Item Base: {result['item_base']}\n"
        if 'rarity' in result:
            output += f"Rarity: {result['rarity'].title()}\n\n"
            
        # Display modifiers
        if 'modifiers' in result and result['modifiers']:
            output += f"DETECTED MODIFIERS ({len(result['modifiers'])}):\n"
            output += "-" * 30 + "\n"
            
            for i, mod in enumerate(result['modifiers'], 1):
                output += f"{i}. {mod['type'].replace('_', ' ').title()}\n"
                output += f"   Text: {mod['raw_text']}\n"
                output += f"   Tier: {mod['tier']}\n"
                if 'values' in mod:
                    output += f"   Values: {mod['values']}\n"
                output += "\n"
        else:
            output += "No modifiers detected.\n\n"
            
        # Raw text section
        if 'raw_text' in result:
            output += "RAW EXTRACTED TEXT:\n"
            output += "-" * 20 + "\n"
            output += result['raw_text']
            output += "\n\n"
            
        # Auto-populate main application
        if result.get('success') and 'modifiers' in result:
            self.auto_populate_main_app(result)
            output += "✅ Main application auto-populated with detected data!\n"
        
        self.results_text.insert(tk.END, output)
        
    def auto_populate_main_app(self, result: Dict):
        """Auto-populate main application with detected data"""
        try:
            # Clear existing entries
            self.parent_app.base_entry.delete(0, tk.END)
            self.parent_app.target_mods_text.delete(1.0, tk.END)
            
            # Set base item
            if 'item_base' in result:
                self.parent_app.base_entry.insert(0, result['item_base'])
                
            # Set target modifiers
            if 'modifiers' in result:
                mod_text = ""
                for mod in result['modifiers']:
                    mod_name = mod['type'].replace('_', ' ').title()
                    mod_text += f"{mod_name}\n"
                    
                self.parent_app.target_mods_text.insert(1.0, mod_text.strip())
                
        except Exception as e:
            print(f"Error auto-populating: {e}")


# Global OCR analyzer instance
poe_ocr = POEItemOCR()