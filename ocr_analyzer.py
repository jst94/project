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
        
        # Configure tesseract with multiple PSM modes for different scenarios
        self.base_config = '-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%+:- '
        self.psm_configs = {
            'uniform_block': f'--psm 6 {self.base_config}',  # Original - uniform text block
            'single_line': f'--psm 7 {self.base_config}',    # Single text line
            'single_word': f'--psm 8 {self.base_config}',    # Single word
            'raw_line': f'--psm 13 {self.base_config}',      # Raw line, bypass word detection
        }
        
        # Common PoE modifier aliases and variations for fuzzy matching
        self.modifier_aliases = {
            'life': ['maximum life', 'max life', 'to life', 'life pool', '+life'],
            'energy_shield': ['maximum energy shield', 'max energy shield', 'max es', 'energy shield', 'es'],
            'mana': ['maximum mana', 'max mana', 'to mana', 'mana pool', '+mana'],
            'damage': ['damage', 'dmg', 'adds damage', 'added damage'],
            'resistance': ['resistance', 'resist', 'res', '% to resistance', 'to resistance'],
            'attack_speed': ['attack speed', 'increased attack speed', 'ias', 'att speed'],
            'cast_speed': ['cast speed', 'increased cast speed', 'casting speed', 'ics'],
            'critical_strike': ['critical strike', 'crit', 'critical', 'crit chance'],
            'accuracy': ['accuracy rating', 'accuracy', 'acc', 'to accuracy'],
            'strength': ['strength', 'str', 'to strength', '+str'],
            'dexterity': ['dexterity', 'dex', 'to dexterity', '+dex'],
            'intelligence': ['intelligence', 'int', 'to intelligence', '+int'],
        }
        
    def capture_screen_region(self, x: int, y: int, width: int, height: int) -> Image.Image:
        """Capture a specific region of the screen"""
        try:
            # Use PIL to capture screen region
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            return screenshot
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None
    
    def auto_detect_tooltip(self) -> Optional[Image.Image]:
        """Automatically detect and capture PoE item tooltip from screen"""
        try:
            # Capture full screen
            full_screen = ImageGrab.grab()
            screen_array = np.array(full_screen)
            
            # Convert to different color spaces for analysis
            hsv = cv2.cvtColor(screen_array, cv2.COLOR_RGB2HSV)
            
            # PoE tooltip characteristics:
            # - Brown/dark border (typical PoE item tooltip style)
            # - Rectangular shape
            # - Text content inside
            # - Usually appears near cursor
            
            # Define color ranges for PoE tooltip detection
            # Brown/dark borders (adjust these values based on PoE's actual tooltip colors)
            tooltip_border_lower = np.array([15, 50, 20])   # Brown-ish lower bound
            tooltip_border_upper = np.array([25, 255, 80])  # Brown-ish upper bound
            
            # Create mask for tooltip colors
            tooltip_mask = cv2.inRange(hsv, tooltip_border_lower, tooltip_border_upper)
            
            # Find contours that might be tooltips
            contours, _ = cv2.findContours(tooltip_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            best_tooltip_region = None
            best_score = 0
            
            for contour in contours:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filter by size (tooltips are usually medium-sized rectangles)
                if w < 200 or h < 100 or w > 800 or h > 600:
                    continue
                
                # Calculate aspect ratio (tooltips are usually taller than wide)
                aspect_ratio = h / w
                if aspect_ratio < 0.8 or aspect_ratio > 3.0:
                    continue
                
                # Score based on size and shape
                area = w * h
                shape_score = min(1.0, area / 100000)  # Normalize area
                aspect_score = 1.0 - abs(aspect_ratio - 1.5) / 1.5  # Prefer ~1.5 aspect ratio
                
                total_score = (shape_score * 0.6) + (aspect_score * 0.4)
                
                if total_score > best_score:
                    best_score = total_score
                    best_tooltip_region = (x, y, w, h)
            
            # If we found a good candidate, extract it
            if best_tooltip_region and best_score > 0.3:
                x, y, w, h = best_tooltip_region
                tooltip_image = full_screen.crop((x, y, x + w, y + h))
                return tooltip_image
            
            return None
            
        except Exception as e:
            print(f"Auto tooltip detection error: {e}")
            return None
    
    def analyze_tooltip_content(self, tooltip_image: Image.Image) -> Dict:
        """Analyze the content of a detected tooltip for PoE-specific information"""
        try:
            # Preprocess the tooltip image
            processed = self.preprocess_image(tooltip_image)
            if processed is None:
                return {'error': 'Failed to preprocess tooltip'}
            
            # Extract text using intelligent OCR
            text = self.extract_text_from_image(processed)
            if not text:
                return {'error': 'No text extracted from tooltip'}
            
            # Parse modifiers
            modifiers = self.parse_item_modifiers(text)
            
            # Detect item rarity
            rarity = self.detect_item_rarity(tooltip_image)
            
            # Try to extract item name (usually first line)
            lines = text.split('\n')
            item_name = lines[0].strip() if lines else 'Unknown Item'
            
            return {
                'item_name': item_name,
                'rarity': rarity,
                'modifiers': modifiers,
                'raw_text': text,
                'modifier_count': len(modifiers),
                'high_confidence_mods': len([m for m in modifiers if m.get('confidence') == 'high'])
            }
            
        except Exception as e:
            return {'error': f'Tooltip analysis failed: {e}'}
            
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image with adaptive methods for better OCR results"""
        try:
            # Convert PIL to OpenCV format
            img_array = np.array(image)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # Try multiple preprocessing approaches and select the best one
            preprocessing_variants = [
                self._preprocess_standard,
                self._preprocess_high_contrast,
                self._preprocess_adaptive,
                self._preprocess_denoised
            ]
            
            best_image = None
            best_score = 0
            
            for preprocess_func in preprocessing_variants:
                try:
                    processed = preprocess_func(img_bgr)
                    score = self._evaluate_preprocessing_quality(processed)
                    
                    if score > best_score:
                        best_score = score
                        best_image = processed
                        
                except Exception as e:
                    print(f"Preprocessing variant failed: {e}")
                    continue
            
            # Fallback to standard if all variants failed
            if best_image is None:
                best_image = self._preprocess_standard(img_bgr)
            
            return best_image
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def _preprocess_standard(self, img_bgr: np.ndarray) -> np.ndarray:
        """Standard preprocessing (original method)"""
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        filtered = cv2.bilateralFilter(gray, 9, 75, 75)
        _, thresh = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((2, 2), np.uint8)
        return cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    def _preprocess_high_contrast(self, img_bgr: np.ndarray) -> np.ndarray:
        """High contrast preprocessing for faded text"""
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        
        # Enhance contrast using CLAHE
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Apply adaptive threshold
        thresh = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Clean up with morphological operations
        kernel = np.ones((1, 1), np.uint8)
        return cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    def _preprocess_adaptive(self, img_bgr: np.ndarray) -> np.ndarray:
        """Adaptive preprocessing that adjusts based on image characteristics"""
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        
        # Analyze image brightness to choose appropriate preprocessing
        mean_brightness = np.mean(gray)
        
        if mean_brightness < 100:  # Dark image
            # Enhance brightness and contrast
            alpha = 1.5  # Contrast
            beta = 50    # Brightness
            enhanced = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
        elif mean_brightness > 200:  # Bright image
            # Reduce brightness slightly
            enhanced = cv2.convertScaleAbs(gray, alpha=0.8, beta=-20)
        else:
            enhanced = gray
        
        # Apply adaptive threshold
        thresh = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                     cv2.THRESH_BINARY, 15, 8)
        
        return thresh
    
    def _preprocess_denoised(self, img_bgr: np.ndarray) -> np.ndarray:
        """Denoising-focused preprocessing for noisy images"""
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        
        # Apply Non-local Means Denoising
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # Apply Gaussian blur to further smooth
        blurred = cv2.GaussianBlur(denoised, (3, 3), 0)
        
        # Apply threshold
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    
    def _evaluate_preprocessing_quality(self, processed_image: np.ndarray) -> float:
        """Evaluate the quality of preprocessing for OCR"""
        try:
            # Calculate text-like regions using edge detection
            edges = cv2.Canny(processed_image, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            
            # Calculate contrast using standard deviation
            contrast = np.std(processed_image) / 255.0
            
            # Calculate noise level (inverse of smoothness)
            laplacian_var = cv2.Laplacian(processed_image, cv2.CV_64F).var()
            noise_score = min(1.0, laplacian_var / 1000.0)  # Normalize
            
            # Combine metrics (higher is better for edge_density and contrast, lower for noise)
            quality_score = (edge_density * 0.4) + (contrast * 0.4) + ((1.0 - noise_score) * 0.2)
            
            return quality_score
            
        except Exception:
            return 0.0
            
    def extract_text_from_image(self, image: np.ndarray) -> str:
        """Extract text using intelligent multi-PSM OCR approach"""
        try:
            # Try multiple PSM modes and select the best result
            ocr_results = []
            
            for mode_name, config in self.psm_configs.items():
                try:
                    # Extract text with this configuration
                    text = pytesseract.image_to_string(image, config=config)
                    
                    # Get confidence data
                    data = pytesseract.image_to_data(image, config=config, output_type=pytesseract.Output.DICT)
                    confidence = self._calculate_confidence(data)
                    
                    # Score the result based on confidence and content quality
                    score = self._score_ocr_result(text, confidence)
                    
                    ocr_results.append({
                        'mode': mode_name,
                        'text': text.strip(),
                        'confidence': confidence,
                        'score': score
                    })
                    
                except Exception as e:
                    print(f"OCR failed for mode {mode_name}: {e}")
                    continue
            
            if not ocr_results:
                return ""
            
            # Select the best result based on score
            best_result = max(ocr_results, key=lambda x: x['score'])
            
            # Optional: Log the decision for debugging
            print(f"Selected OCR mode: {best_result['mode']} (score: {best_result['score']:.2f})")
            
            return best_result['text']
            
        except Exception as e:
            print(f"OCR extraction error: {e}")
            return ""
    
    def _calculate_confidence(self, data: dict) -> float:
        """Calculate average confidence from OCR data"""
        confidences = [conf for conf in data['conf'] if conf > 0]
        return sum(confidences) / len(confidences) if confidences else 0.0
    
    def _score_ocr_result(self, text: str, confidence: float) -> float:
        """Score OCR result based on confidence and content quality"""
        if not text.strip():
            return 0.0
        
        base_score = confidence / 100.0  # Normalize confidence to 0-1
        
        # Bonus for PoE-like content
        poe_keywords = ['damage', 'resistance', 'life', 'mana', 'energy shield', 
                       'increased', 'maximum', 'accuracy', 'critical', 'attack']
        
        text_lower = text.lower()
        keyword_bonus = sum(0.1 for keyword in poe_keywords if keyword in text_lower)
        
        # Penalty for very short or very long text (likely OCR errors)
        length_penalty = 0.0
        if len(text.strip()) < 5:
            length_penalty = 0.2
        elif len(text.strip()) > 1000:
            length_penalty = 0.1
        
        # Bonus for having numbers (PoE modifiers often have numeric values)
        number_bonus = 0.1 if re.search(r'\d+', text) else 0.0
        
        final_score = base_score + keyword_bonus + number_bonus - length_penalty
        return max(0.0, min(1.0, final_score))  # Clamp to 0-1
            
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
        """Parse modifiers from extracted text with fuzzy matching"""
        modifiers = []
        lines = text.split('\n')
        
        for line in lines:
            line_clean = line.strip().lower()
            if not line_clean:
                continue
                
            # First try exact pattern matching
            found = False
            for mod_type, pattern in self.modifier_patterns.items():
                matches = re.findall(pattern, line_clean, re.IGNORECASE)
                if matches:
                    modifiers.append({
                        'type': mod_type,
                        'raw_text': line.strip(),
                        'values': matches[0] if isinstance(matches[0], tuple) else [matches[0]],
                        'tier': self.estimate_modifier_tier(mod_type, matches[0]),
                        'confidence': 'high'
                    })
                    found = True
                    break
            
            # If no exact match, try fuzzy matching
            if not found:
                fuzzy_match = self._fuzzy_match_modifier(line_clean)
                if fuzzy_match:
                    modifiers.append({
                        'type': fuzzy_match['type'],
                        'raw_text': line.strip(),
                        'values': fuzzy_match['values'],
                        'tier': 'unknown',
                        'confidence': 'medium',
                        'fuzzy_score': fuzzy_match['score']
                    })
                    
        return modifiers
    
    def _fuzzy_match_modifier(self, text: str) -> Optional[Dict]:
        """Use fuzzy matching to identify modifiers from misread text"""
        best_match = None
        best_score = 0.6  # Minimum similarity threshold
        
        # Extract numbers from the text first
        numbers = re.findall(r'\d+', text)
        
        for mod_type, aliases in self.modifier_aliases.items():
            for alias in aliases:
                similarity = self._calculate_similarity(text, alias)
                
                if similarity > best_score:
                    best_score = similarity
                    best_match = {
                        'type': mod_type,
                        'values': numbers if numbers else ['?'],
                        'score': similarity,
                        'matched_alias': alias
                    }
        
        return best_match
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two strings using simple Levenshtein-like approach"""
        # Simple implementation of edit distance similarity
        if not text1 or not text2:
            return 0.0
        
        # Convert to sets of words for fuzzy word matching
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        # Calculate Jaccard similarity (intersection over union)
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        jaccard_sim = intersection / union if union > 0 else 0.0
        
        # Also check for partial word matches
        partial_matches = 0
        for w1 in words1:
            for w2 in words2:
                if len(w1) >= 3 and len(w2) >= 3:
                    if w1 in w2 or w2 in w1:
                        partial_matches += 0.5
        
        partial_sim = min(1.0, partial_matches / max(len(words1), len(words2)))
        
        # Combine both similarities
        return (jaccard_sim * 0.7) + (partial_sim * 0.3)
        
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