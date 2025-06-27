"""
Intelligent OCR System with Machine Learning Capabilities
Advanced OCR with pattern recognition, confidence scoring, and adaptive learning
"""

import cv2
import numpy as np
import re
import json
import time
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

# Import our new auto-detection module
try:
    from auto_detection import AutoDetector, DetectedItem, AutoDetectionUI
    AUTO_DETECTION_AVAILABLE = True
except ImportError:
    AUTO_DETECTION_AVAILABLE = False


@dataclass
class OCRResult:
    """Enhanced OCR result with confidence and metadata"""
    text: str
    confidence: float
    bounding_box: Tuple[int, int, int, int]
    preprocessing_method: str
    recognition_time: float
    quality_score: float


@dataclass
class ModifierMatch:
    """Advanced modifier matching result"""
    modifier_name: str
    raw_text: str
    confidence: float
    tier: Optional[str]
    values: List[str]
    match_method: str  # 'exact', 'fuzzy', 'pattern', 'ml'
    similarity_score: float


class IntelligentOCREngine:
    """ML-enhanced OCR engine for PoE items"""
    
    def __init__(self):
        # Enhanced pattern library with machine learning features
        self.modifier_patterns = {
            'life': {
                'patterns': [
                    r'(?:\+)?(\d+)\s*to\s*maximum\s*life',
                    r'(\d+)\s*maximum\s*life',
                    r'life\s*(?:\+)?(\d+)',
                    r'(?:\+)?(\d+)\s*life'
                ],
                'keywords': ['life', 'maximum', 'max', 'hp'],
                'value_range': (1, 150),
                'common_ocr_errors': {'1ife': 'life', '11fe': 'life', 'lite': 'life'}
            },
            'energy_shield': {
                'patterns': [
                    r'(?:\+)?(\d+)\s*to\s*maximum\s*energy\s*shield',
                    r'(\d+)\s*maximum\s*energy\s*shield',
                    r'energy\s*shield\s*(?:\+)?(\d+)',
                    r'(?:\+)?(\d+)\s*(?:energy\s*shield|es)'
                ],
                'keywords': ['energy', 'shield', 'es', 'maximum'],
                'value_range': (1, 120),
                'common_ocr_errors': {'enerqy': 'energy', 'sh1eld': 'shield', 'shie1d': 'shield'}
            },
            'attack_speed': {
                'patterns': [
                    r'(\d+)%\s*increased\s*attack\s*speed',
                    r'attack\s*speed\s*(?:\+)?(\d+)%',
                    r'(?:\+)?(\d+)%\s*attack\s*speed',
                    r'increased\s*attack\s*speed\s*(\d+)%'
                ],
                'keywords': ['attack', 'speed', 'increased', 'ias'],
                'value_range': (1, 25),
                'common_ocr_errors': {'atlack': 'attack', 'speeci': 'speed', 'increaseci': 'increased'}
            },
            'critical_strike': {
                'patterns': [
                    r'(\d+)%\s*increased\s*critical\s*strike\s*chance',
                    r'critical\s*strike\s*chance\s*(?:\+)?(\d+)%',
                    r'(?:\+)?(\d+)%\s*critical\s*strike',
                    r'crit(?:ical)?\s*chance\s*(?:\+)?(\d+)%'
                ],
                'keywords': ['critical', 'strike', 'crit', 'chance'],
                'value_range': (1, 50),
                'common_ocr_errors': {'critica1': 'critical', 'stnke': 'strike', 'crit1cal': 'critical'}
            },
            'resistance': {
                'patterns': [
                    r'(?:\+)?(\d+)%\s*to\s*(fire|cold|lightning|chaos)\s*resistance',
                    r'(fire|cold|lightning|chaos)\s*resistance\s*(?:\+)?(\d+)%',
                    r'(?:\+)?(\d+)%\s*(fire|cold|lightning|chaos)\s*res(?:istance)?'
                ],
                'keywords': ['resistance', 'fire', 'cold', 'lightning', 'chaos', 'res'],
                'value_range': (1, 50),
                'common_ocr_errors': {'res1stance': 'resistance', 'l1ghtning': 'lightning', 'co1d': 'cold'}
            }
        }
        
        # Learning database for pattern recognition
        self.learning_database = {
            'successful_matches': defaultdict(list),
            'failed_recognitions': defaultdict(list),
            'user_corrections': defaultdict(list),
            'confidence_calibration': defaultdict(list)
        }
        
        # Advanced preprocessing techniques
        self.preprocessing_techniques = {
            'adaptive_threshold': self._adaptive_threshold,
            'morphological_clean': self._morphological_cleaning,
            'noise_reduction': self._noise_reduction,
            'contrast_enhancement': self._contrast_enhancement,
            'edge_preserving': self._edge_preserving_filter,
            'text_isolation': self._text_isolation
        }
        
        # Confidence scoring weights
        self.confidence_weights = {
            'pattern_match': 0.3,
            'value_range': 0.2,
            'keyword_presence': 0.2,
            'ocr_confidence': 0.15,
            'context_coherence': 0.15
        }
        
    def extract_modifiers_intelligent(self, image: np.ndarray, 
                                    context: Optional[Dict] = None) -> List[ModifierMatch]:
        """Intelligently extract modifiers using ML-enhanced techniques"""
        
        # Apply multiple preprocessing techniques and find best result
        preprocessing_results = []
        
        for technique_name, technique_func in self.preprocessing_techniques.items():
            try:
                processed_image = technique_func(image)
                ocr_result = self._perform_ocr_with_confidence(processed_image, technique_name)
                preprocessing_results.append(ocr_result)
            except Exception as e:
                print(f"Preprocessing technique {technique_name} failed: {e}")
                continue
        
        if not preprocessing_results:
            return []
        
        # Select best preprocessing result based on quality scores
        best_result = max(preprocessing_results, key=lambda x: x.quality_score)
        
        # Extract modifiers using advanced pattern matching
        modifiers = self._extract_modifiers_from_text(best_result.text, best_result.confidence)
        
        # Apply machine learning enhancements
        enhanced_modifiers = self._enhance_with_ml(modifiers, image, context)
        
        # Update learning database
        self._update_learning_database(enhanced_modifiers, best_result)
        
        return enhanced_modifiers
    
    def _adaptive_threshold(self, image: np.ndarray) -> np.ndarray:
        """Adaptive thresholding with local optimization"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Adaptive threshold with optimized parameters
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        return thresh
    
    def _morphological_cleaning(self, image: np.ndarray) -> np.ndarray:
        """Morphological operations to clean up text"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply threshold
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Morphological operations
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        return cleaned
    
    def _noise_reduction(self, image: np.ndarray) -> np.ndarray:
        """Advanced noise reduction"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Non-local means denoising
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # Apply threshold
        _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    
    def _contrast_enhancement(self, image: np.ndarray) -> np.ndarray:
        """CLAHE-based contrast enhancement"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply CLAHE
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Apply threshold
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    
    def _edge_preserving_filter(self, image: np.ndarray) -> np.ndarray:
        """Edge-preserving smoothing filter"""
        if len(image.shape) == 3:
            filtered = cv2.edgePreservingFilter(image, flags=1, sigma_s=50, sigma_r=0.4)
            gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply threshold
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    
    def _text_isolation(self, image: np.ndarray) -> np.ndarray:
        """Isolate text regions using connected components"""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply threshold
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Find connected components
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)
        
        # Filter components by size (remove very small and very large)
        min_size = 50
        max_size = image.shape[0] * image.shape[1] * 0.3
        
        filtered = np.zeros_like(thresh)
        for i in range(1, num_labels):
            size = stats[i, cv2.CC_STAT_AREA]
            if min_size <= size <= max_size:
                filtered[labels == i] = 255
        
        return filtered
    
    def _perform_ocr_with_confidence(self, image: np.ndarray, method: str) -> OCRResult:
        """Perform OCR with confidence scoring"""
        start_time = time.time()
        
        try:
            import pytesseract
            
            # Configure tesseract
            config = '--psm 6 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%+:-. '
            
            # Extract text
            text = pytesseract.image_to_string(image, config=config)
            
            # Get confidence data
            data = pytesseract.image_to_data(image, config=config, output_type=pytesseract.Output.DICT)
            
            # Calculate overall confidence
            confidences = [conf for conf in data['conf'] if conf > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Calculate quality score
            quality_score = self._calculate_image_quality(image)
            
            # Extract bounding box
            bbox = self._extract_text_bbox(data)
            
            processing_time = time.time() - start_time
            
            return OCRResult(
                text=text.strip(),
                confidence=avg_confidence / 100.0,  # Normalize to 0-1
                bounding_box=bbox,
                preprocessing_method=method,
                recognition_time=processing_time,
                quality_score=quality_score
            )
            
        except Exception as e:
            print(f"OCR failed with method {method}: {e}")
            return OCRResult("", 0.0, (0, 0, 0, 0), method, time.time() - start_time, 0.0)
    
    def _calculate_image_quality(self, image: np.ndarray) -> float:
        """Calculate image quality score for OCR suitability"""
        # Variance of Laplacian (sharpness)
        laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
        sharpness_score = min(1.0, laplacian_var / 1000.0)
        
        # Contrast score
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        contrast_score = np.std(gray) / 255.0
        
        # Text-like structure detection
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        structure_score = min(1.0, edge_density * 10)
        
        # Combined quality score
        quality = (sharpness_score * 0.4) + (contrast_score * 0.3) + (structure_score * 0.3)
        
        return max(0.0, min(1.0, quality))
    
    def _extract_text_bbox(self, ocr_data: Dict) -> Tuple[int, int, int, int]:
        """Extract overall text bounding box from OCR data"""
        valid_boxes = []
        
        for i, conf in enumerate(ocr_data['conf']):
            if conf > 0:
                x, y, w, h = ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i]
                valid_boxes.append((x, y, x + w, y + h))
        
        if not valid_boxes:
            return (0, 0, 0, 0)
        
        # Calculate overall bounding box
        min_x = min(box[0] for box in valid_boxes)
        min_y = min(box[1] for box in valid_boxes)
        max_x = max(box[2] for box in valid_boxes)
        max_y = max(box[3] for box in valid_boxes)
        
        return (min_x, min_y, max_x - min_x, max_y - min_y)
    
    def _extract_modifiers_from_text(self, text: str, base_confidence: float) -> List[ModifierMatch]:
        """Extract modifiers using enhanced pattern matching"""
        modifiers = []
        lines = text.split('\n')
        
        for line in lines:
            line_clean = line.strip()
            if not line_clean:
                continue
            
            # Try exact pattern matching first
            for mod_type, mod_data in self.modifier_patterns.items():
                for pattern in mod_data['patterns']:
                    matches = re.findall(pattern, line_clean, re.IGNORECASE)
                    if matches:
                        confidence = self._calculate_pattern_confidence(
                            line_clean, mod_type, matches, base_confidence
                        )
                        
                        modifier = ModifierMatch(
                            modifier_name=mod_type.replace('_', ' ').title(),
                            raw_text=line_clean,
                            confidence=confidence,
                            tier=self._estimate_tier(mod_type, matches),
                            values=list(matches[0]) if isinstance(matches[0], tuple) else [str(matches[0])],
                            match_method='pattern',
                            similarity_score=1.0
                        )
                        
                        modifiers.append(modifier)
                        break
                else:
                    continue
                break
            else:
                # Try fuzzy matching for unrecognized lines
                fuzzy_match = self._fuzzy_match_advanced(line_clean, base_confidence)
                if fuzzy_match:
                    modifiers.append(fuzzy_match)
        
        return modifiers
    
    def _calculate_pattern_confidence(self, text: str, mod_type: str, 
                                    matches: List, base_confidence: float) -> float:
        """Calculate confidence score for pattern matches"""
        mod_data = self.modifier_patterns.get(mod_type, {})
        
        # Base pattern match confidence
        pattern_conf = 0.8
        
        # Value range validation
        value_conf = 1.0
        try:
            value = int(matches[0]) if not isinstance(matches[0], tuple) else int(matches[0][0])
            value_range = mod_data.get('value_range', (0, 1000))
            if not (value_range[0] <= value <= value_range[1]):
                value_conf = 0.5  # Suspicious value
        except (ValueError, IndexError):
            value_conf = 0.3
        
        # Keyword presence
        keywords = mod_data.get('keywords', [])
        keyword_conf = 0.5
        if keywords:
            text_lower = text.lower()
            keyword_matches = sum(1 for kw in keywords if kw in text_lower)
            keyword_conf = min(1.0, keyword_matches / len(keywords) + 0.3)
        
        # OCR confidence
        ocr_conf = base_confidence
        
        # Context coherence (simplified)
        context_conf = 0.7
        
        # Weighted combination
        weights = self.confidence_weights
        total_confidence = (
            pattern_conf * weights['pattern_match'] +
            value_conf * weights['value_range'] +
            keyword_conf * weights['keyword_presence'] +
            ocr_conf * weights['ocr_confidence'] +
            context_conf * weights['context_coherence']
        )
        
        return max(0.1, min(0.95, total_confidence))
    
    def _estimate_tier(self, mod_type: str, matches: List) -> Optional[str]:
        """Estimate modifier tier based on values"""
        tier_thresholds = {
            'life': [(120, 'T1'), (100, 'T2'), (80, 'T3'), (60, 'T4'), (0, 'T5')],
            'energy_shield': [(100, 'T1'), (80, 'T2'), (60, 'T3'), (40, 'T4'), (0, 'T5')],
            'attack_speed': [(17, 'T1'), (14, 'T2'), (11, 'T3'), (8, 'T4'), (0, 'T5')],
            'critical_strike': [(38, 'T1'), (34, 'T2'), (29, 'T3'), (24, 'T4'), (0, 'T5')],
            'resistance': [(48, 'T1'), (42, 'T2'), (36, 'T3'), (30, 'T4'), (0, 'T5')]
        }
        
        if mod_type not in tier_thresholds:
            return None
        
        try:
            value = int(matches[0]) if not isinstance(matches[0], tuple) else int(matches[0][0])
            
            for threshold, tier in tier_thresholds[mod_type]:
                if value >= threshold:
                    return tier
                    
        except (ValueError, IndexError):
            pass
        
        return 'Unknown'
    
    def _fuzzy_match_advanced(self, text: str, base_confidence: float) -> Optional[ModifierMatch]:
        """Advanced fuzzy matching with error correction"""
        text_lower = text.lower()
        
        # Apply common OCR error corrections
        corrected_text = text_lower
        for mod_type, mod_data in self.modifier_patterns.items():
            corrections = mod_data.get('common_ocr_errors', {})
            for error, correction in corrections.items():
                corrected_text = corrected_text.replace(error, correction)
        
        # Try pattern matching on corrected text
        for mod_type, mod_data in self.modifier_patterns.items():
            for pattern in mod_data['patterns']:
                matches = re.findall(pattern, corrected_text, re.IGNORECASE)
                if matches:
                    # Calculate similarity score
                    similarity = self._calculate_text_similarity(text_lower, corrected_text)
                    
                    confidence = base_confidence * 0.7 * similarity  # Reduced confidence for fuzzy matches
                    
                    return ModifierMatch(
                        modifier_name=mod_type.replace('_', ' ').title(),
                        raw_text=text,
                        confidence=confidence,
                        tier=self._estimate_tier(mod_type, matches),
                        values=list(matches[0]) if isinstance(matches[0], tuple) else [str(matches[0])],
                        match_method='fuzzy',
                        similarity_score=similarity
                    )
        
        return None
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two strings"""
        if not text1 or not text2:
            return 0.0
        
        # Simple Levenshtein-like similarity
        len1, len2 = len(text1), len(text2)
        if len1 == 0:
            return 0.0 if len2 > 0 else 1.0
        if len2 == 0:
            return 0.0
        
        # Calculate edit distance (simplified)
        max_len = max(len1, len2)
        edit_distance = abs(len1 - len2)
        
        # Count different characters
        for i in range(min(len1, len2)):
            if text1[i] != text2[i]:
                edit_distance += 1
        
        similarity = 1.0 - (edit_distance / max_len)
        return max(0.0, similarity)
    
    def _enhance_with_ml(self, modifiers: List[ModifierMatch], 
                        image: np.ndarray, context: Optional[Dict]) -> List[ModifierMatch]:
        """Enhance modifier recognition using ML techniques"""
        enhanced_modifiers = []
        
        for modifier in modifiers:
            # Apply learning-based confidence adjustment
            historical_success = self._get_historical_success_rate(modifier.modifier_name)
            
            # Adjust confidence based on historical performance
            confidence_adjustment = (historical_success - 0.5) * 0.2  # +/- 10% max adjustment
            adjusted_confidence = max(0.1, min(0.95, modifier.confidence + confidence_adjustment))
            
            # Context-based validation
            if context:
                context_boost = self._validate_with_context(modifier, context)
                adjusted_confidence *= context_boost
            
            # Create enhanced modifier
            enhanced_modifier = ModifierMatch(
                modifier_name=modifier.modifier_name,
                raw_text=modifier.raw_text,
                confidence=adjusted_confidence,
                tier=modifier.tier,
                values=modifier.values,
                match_method=f"{modifier.match_method}_ml_enhanced",
                similarity_score=modifier.similarity_score
            )
            
            enhanced_modifiers.append(enhanced_modifier)
        
        return enhanced_modifiers
    
    def _get_historical_success_rate(self, modifier_name: str) -> float:
        """Get historical success rate for a modifier type"""
        successes = self.learning_database['successful_matches'][modifier_name]
        failures = self.learning_database['failed_recognitions'][modifier_name]
        
        total_attempts = len(successes) + len(failures)
        if total_attempts == 0:
            return 0.5  # Neutral baseline
        
        return len(successes) / total_attempts
    
    def _validate_with_context(self, modifier: ModifierMatch, context: Dict) -> float:
        """Validate modifier with contextual information"""
        boost = 1.0
        
        # Item type context
        item_type = context.get('item_type', '').lower()
        modifier_lower = modifier.modifier_name.lower()
        
        # Logical consistency checks
        if 'weapon' in item_type and 'attack speed' in modifier_lower:
            boost *= 1.1  # Attack speed makes sense on weapons
        elif 'armor' in item_type and ('life' in modifier_lower or 'energy shield' in modifier_lower):
            boost *= 1.1  # Life/ES makes sense on armor
        elif 'ring' in item_type and 'resistance' in modifier_lower:
            boost *= 1.1  # Resistances make sense on rings
        
        # Value consistency
        try:
            value = int(modifier.values[0]) if modifier.values else 0
            if value > 0:
                # Check if value is reasonable for the modifier type
                reasonable_ranges = {
                    'maximum life': (1, 150),
                    'maximum energy shield': (1, 120),
                    'attack speed': (1, 25),
                    'critical strike chance': (1, 50)
                }
                
                range_check = reasonable_ranges.get(modifier_lower, (1, 1000))
                if range_check[0] <= value <= range_check[1]:
                    boost *= 1.05
                else:
                    boost *= 0.8  # Suspicious value
        except (ValueError, IndexError):
            boost *= 0.9  # No valid value found
        
        return max(0.5, min(1.3, boost))
    
    def _update_learning_database(self, modifiers: List[ModifierMatch], ocr_result: OCRResult):
        """Update learning database with recognition results"""
        timestamp = datetime.now().isoformat()
        
        for modifier in modifiers:
            # Store successful matches for learning
            success_entry = {
                'timestamp': timestamp,
                'confidence': modifier.confidence,
                'method': modifier.match_method,
                'preprocessing': ocr_result.preprocessing_method,
                'image_quality': ocr_result.quality_score
            }
            
            self.learning_database['successful_matches'][modifier.modifier_name].append(success_entry)
            
            # Maintain sliding window of recent entries
            max_entries = 100
            if len(self.learning_database['successful_matches'][modifier.modifier_name]) > max_entries:
                self.learning_database['successful_matches'][modifier.modifier_name] = \
                    self.learning_database['successful_matches'][modifier.modifier_name][-max_entries:]
    
    def learn_from_user_feedback(self, text: str, expected_modifiers: List[str], 
                                actual_modifiers: List[str]):
        """Learn from user corrections and feedback"""
        timestamp = datetime.now().isoformat()
        
        # Store user corrections
        correction_entry = {
            'timestamp': timestamp,
            'original_text': text,
            'expected': expected_modifiers,
            'detected': actual_modifiers,
            'accuracy': len(set(expected_modifiers) & set(actual_modifiers)) / max(len(expected_modifiers), 1)
        }
        
        for mod in expected_modifiers:
            self.learning_database['user_corrections'][mod].append(correction_entry)
    
    def get_learning_statistics(self) -> Dict:
        """Get statistics about the learning system performance"""
        stats = {}
        
        for mod_type in self.modifier_patterns.keys():
            successes = len(self.learning_database['successful_matches'][mod_type])
            failures = len(self.learning_database['failed_recognitions'][mod_type])
            corrections = len(self.learning_database['user_corrections'][mod_type])
            
            stats[mod_type] = {
                'total_attempts': successes + failures,
                'success_rate': successes / (successes + failures) if (successes + failures) > 0 else 0,
                'user_corrections': corrections,
                'confidence_trend': self._calculate_confidence_trend(mod_type)
            }
        
        return stats
    
    def _calculate_confidence_trend(self, mod_type: str) -> str:
        """Calculate confidence trend for a modifier type"""
        recent_entries = self.learning_database['successful_matches'][mod_type][-20:]
        
        if len(recent_entries) < 5:
            return 'insufficient_data'
        
        confidences = [entry['confidence'] for entry in recent_entries]
        
        # Simple trend calculation
        first_half = confidences[:len(confidences)//2]
        second_half = confidences[len(confidences)//2:]
        
        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)
        
        if avg_second > avg_first + 0.05:
            return 'improving'
        elif avg_second < avg_first - 0.05:
            return 'declining'
        else:
            return 'stable'


    def detect_item_from_screen(self) -> Optional[Dict]:
        """Detect item from screen using auto-detection if available"""
        if AUTO_DETECTION_AVAILABLE:
            detector = AutoDetector()
            item = detector.detect_item_at_cursor()
            
            if item:
                return {
                    'base': item.base_type,
                    'type': item.item_type,
                    'rarity': item.rarity,
                    'modifiers': item.modifiers,
                    'implicit_mods': item.implicit_mods,
                    'explicit_mods': item.explicit_mods,
                    'crafted_mods': item.crafted_mods,
                    'item_level': item.item_level,
                    'quality': item.quality,
                    'corrupted': item.corrupted,
                    'confidence': item.confidence
                }
        
        # Fallback message if auto-detection not available
        return None


# Global intelligent OCR instance
intelligent_ocr = IntelligentOCREngine()