"""
Enhanced Modifier Database with Comprehensive Tier Data and Meta Analysis
Complete database of PoE modifiers with advanced tier analysis and meta insights
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import defaultdict
import sqlite3
import os


@dataclass
class ModifierTier:
    """Detailed modifier tier information"""
    tier: str
    tier_number: int
    value_min: float
    value_max: float
    weight: int
    ilvl_requirement: int
    rarity_factor: float  # How rare this tier is (0-1)
    meta_popularity: float  # How popular in current meta (0-1)
    market_demand: float  # Market demand factor (0-1)


@dataclass
class ModifierData:
    """Complete modifier information"""
    name: str
    display_name: str
    type: str  # 'prefix' or 'suffix'
    category: str  # 'defensive', 'offensive', 'utility', 'resistance'
    tiers: List[ModifierTier]
    item_types: List[str]  # Which item types can have this modifier
    tags: List[str]  # Searchable tags
    essence_sources: List[str]  # Which essences guarantee this
    fossil_affinities: List[str]  # Which fossils increase chance
    meta_rating: float  # Current meta rating (0-1)
    crafting_difficulty: float  # How hard to craft (0-1)
    synergies: List[str]  # Modifiers that synergize well
    conflicts: List[str]  # Modifiers that conflict
    description: str
    patch_history: List[Dict[str, Any]]


@dataclass
class MetaAnalysis:
    """Meta game analysis for modifiers"""
    league: str
    timeframe: str
    top_modifiers: List[Tuple[str, float]]  # (modifier, popularity_score)
    emerging_trends: List[str]
    declining_modifiers: List[str]
    build_archetypes: Dict[str, List[str]]  # archetype -> preferred modifiers
    price_trends: Dict[str, float]  # modifier -> price trend
    craft_efficiency: Dict[str, float]  # modifier -> efficiency score
    generated_at: str


class EnhancedModifierDatabase:
    """Comprehensive modifier database with meta analysis"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.modifier_db_path = os.path.join(data_dir, "enhanced_modifiers.db")
        
        # Core modifier database
        self.modifiers = {}
        self.modifier_categories = defaultdict(list)
        self.item_type_modifiers = defaultdict(list)
        
        # Meta analysis data
        self.current_meta = None
        self.meta_history = []
        self.build_archetypes = {}
        
        # Tier value calculations
        self.tier_weights = {
            'T1': 1.0, 'T2': 0.85, 'T3': 0.7, 'T4': 0.55, 'T5': 0.4,
            'T6': 0.25, 'T7': 0.15, 'T8': 0.1
        }
        
        # Initialize database
        self.init_modifier_database()
        
        # Load comprehensive modifier data
        self.load_comprehensive_modifiers()
    
    def init_modifier_database(self):
        """Initialize enhanced modifier database"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        with sqlite3.connect(self.modifier_db_path) as conn:
            cursor = conn.cursor()
            
            # Enhanced modifiers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS modifiers (
                    name TEXT PRIMARY KEY,
                    display_name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    item_types TEXT NOT NULL,
                    tags TEXT NOT NULL,
                    essence_sources TEXT,
                    fossil_affinities TEXT,
                    meta_rating REAL NOT NULL,
                    crafting_difficulty REAL NOT NULL,
                    synergies TEXT,
                    conflicts TEXT,
                    description TEXT,
                    last_updated TEXT NOT NULL
                )
            ''')
            
            # Modifier tiers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS modifier_tiers (
                    modifier_name TEXT NOT NULL,
                    tier TEXT NOT NULL,
                    tier_number INTEGER NOT NULL,
                    value_min REAL NOT NULL,
                    value_max REAL NOT NULL,
                    weight INTEGER NOT NULL,
                    ilvl_requirement INTEGER NOT NULL,
                    rarity_factor REAL NOT NULL,
                    meta_popularity REAL NOT NULL,
                    market_demand REAL NOT NULL,
                    PRIMARY KEY (modifier_name, tier),
                    FOREIGN KEY (modifier_name) REFERENCES modifiers (name)
                )
            ''')
            
            # Meta analysis table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS meta_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    league TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    analysis_data TEXT NOT NULL,
                    generated_at TEXT NOT NULL
                )
            ''')
            
            # Build archetypes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS build_archetypes (
                    archetype_name TEXT PRIMARY KEY,
                    preferred_modifiers TEXT NOT NULL,
                    modifier_weights TEXT NOT NULL,
                    popularity REAL NOT NULL,
                    last_updated TEXT NOT NULL
                )
            ''')
            
            conn.commit()
    
    def load_comprehensive_modifiers(self):
        """Load comprehensive modifier database"""
        
        # Life modifiers
        self._add_modifier_family('life', {
            'Maximum Life': {
                'display_name': 'Maximum Life',
                'type': 'prefix',
                'category': 'defensive',
                'tiers': [
                    ('T1', 1, 100, 120, 100, 85, 0.95, 0.9, 0.95),
                    ('T2', 2, 80, 99, 200, 70, 0.8, 0.85, 0.9),
                    ('T3', 3, 60, 79, 400, 50, 0.6, 0.75, 0.8),
                    ('T4', 4, 40, 59, 800, 30, 0.4, 0.6, 0.65),
                    ('T5', 5, 20, 39, 1600, 1, 0.2, 0.4, 0.45)
                ],
                'item_types': ['body_armour', 'helmet', 'gloves', 'boots', 'belt', 'ring', 'amulet'],
                'essence_sources': ['Essence of Greed'],
                'fossil_affinities': ['Prismatic Fossil'],
                'meta_rating': 0.95,
                'crafting_difficulty': 0.3,
                'synergies': ['Life Regeneration', 'Life Recovery'],
                'description': 'Increases maximum life, fundamental defensive modifier'
            },
            'Life Regeneration': {
                'display_name': 'Life Regeneration per second',
                'type': 'suffix',
                'category': 'defensive',
                'tiers': [
                    ('T1', 1, 8.0, 10.0, 150, 85, 0.9, 0.7, 0.75),
                    ('T2', 2, 6.0, 7.9, 300, 70, 0.75, 0.65, 0.7),
                    ('T3', 3, 4.0, 5.9, 600, 50, 0.6, 0.55, 0.6),
                    ('T4', 4, 2.0, 3.9, 1200, 30, 0.4, 0.4, 0.45),
                    ('T5', 5, 1.0, 1.9, 2400, 1, 0.2, 0.25, 0.3)
                ],
                'item_types': ['body_armour', 'helmet', 'gloves', 'boots', 'ring', 'amulet'],
                'essence_sources': [],
                'fossil_affinities': ['Prismatic Fossil'],
                'meta_rating': 0.6,
                'crafting_difficulty': 0.4,
                'synergies': ['Maximum Life', '% Life Recovery'],
                'description': 'Regenerates life per second'
            }
        })
        
        # Energy Shield modifiers
        self._add_modifier_family('energy_shield', {
            'Maximum Energy Shield': {
                'display_name': 'Maximum Energy Shield',
                'type': 'prefix',
                'category': 'defensive',
                'tiers': [
                    ('T1', 1, 100, 120, 100, 85, 0.9, 0.75, 0.8),
                    ('T2', 2, 80, 99, 200, 70, 0.75, 0.7, 0.75),
                    ('T3', 3, 60, 79, 400, 50, 0.6, 0.6, 0.65),
                    ('T4', 4, 40, 59, 800, 30, 0.4, 0.45, 0.5),
                    ('T5', 5, 20, 39, 1600, 1, 0.2, 0.3, 0.35)
                ],
                'item_types': ['body_armour', 'helmet', 'gloves', 'boots', 'shield'],
                'essence_sources': ['Essence of Woe'],
                'fossil_affinities': ['Dense Fossil'],
                'meta_rating': 0.75,
                'crafting_difficulty': 0.35,
                'synergies': ['% Energy Shield', 'Energy Shield Recharge'],
                'description': 'Increases maximum energy shield'
            },
            '% Energy Shield': {
                'display_name': 'Increased Energy Shield',
                'type': 'prefix',
                'category': 'defensive',
                'tiers': [
                    ('T1', 1, 18, 20, 200, 85, 0.85, 0.8, 0.85),
                    ('T2', 2, 15, 17, 400, 70, 0.7, 0.75, 0.8),
                    ('T3', 3, 12, 14, 800, 50, 0.55, 0.65, 0.7),
                    ('T4', 4, 9, 11, 1600, 30, 0.4, 0.5, 0.55),
                    ('T5', 5, 6, 8, 3200, 1, 0.25, 0.35, 0.4)
                ],
                'item_types': ['body_armour', 'helmet', 'gloves', 'boots', 'shield'],
                'essence_sources': [],
                'fossil_affinities': ['Dense Fossil'],
                'meta_rating': 0.8,
                'crafting_difficulty': 0.4,
                'synergies': ['Maximum Energy Shield', 'Energy Shield Recharge'],
                'description': 'Increases energy shield percentage'
            }
        })
        
        # Attack modifiers
        self._add_modifier_family('attack', {
            'Attack Speed': {
                'display_name': 'Increased Attack Speed',
                'type': 'suffix',
                'category': 'offensive',
                'tiers': [
                    ('T1', 1, 15, 17, 100, 85, 0.95, 0.9, 0.95),
                    ('T2', 2, 12, 14, 200, 70, 0.8, 0.85, 0.9),
                    ('T3', 3, 9, 11, 400, 50, 0.65, 0.75, 0.8),
                    ('T4', 4, 6, 8, 800, 30, 0.45, 0.6, 0.65),
                    ('T5', 5, 3, 5, 1600, 1, 0.25, 0.4, 0.45)
                ],
                'item_types': ['weapon', 'gloves', 'ring', 'amulet'],
                'essence_sources': ['Essence of Zeal'],
                'fossil_affinities': ['Jagged Fossil'],
                'meta_rating': 0.9,
                'crafting_difficulty': 0.45,
                'synergies': ['Critical Strike Chance', 'Accuracy Rating'],
                'description': 'Increases attack speed percentage'
            },
            'Critical Strike Chance': {
                'display_name': 'Increased Critical Strike Chance',
                'type': 'suffix',
                'category': 'offensive',
                'tiers': [
                    ('T1', 1, 35, 38, 100, 85, 0.9, 0.85, 0.9),
                    ('T2', 2, 30, 34, 200, 70, 0.75, 0.8, 0.85),
                    ('T3', 3, 25, 29, 400, 50, 0.6, 0.7, 0.75),
                    ('T4', 4, 20, 24, 800, 30, 0.45, 0.55, 0.6),
                    ('T5', 5, 15, 19, 1600, 1, 0.3, 0.4, 0.45)
                ],
                'item_types': ['weapon', 'ring', 'amulet'],
                'essence_sources': ['Essence of Spite'],
                'fossil_affinities': ['Jagged Fossil'],
                'meta_rating': 0.85,
                'crafting_difficulty': 0.5,
                'synergies': ['Critical Strike Multiplier', 'Attack Speed'],
                'description': 'Increases critical strike chance'
            }
        })
        
        # Resistance modifiers
        self._add_modifier_family('resistance', {
            'Fire Resistance': {
                'display_name': 'Fire Resistance',
                'type': 'suffix',
                'category': 'resistance',
                'tiers': [
                    ('T1', 1, 43, 48, 250, 85, 0.8, 0.95, 0.9),
                    ('T2', 2, 37, 42, 500, 70, 0.65, 0.9, 0.85),
                    ('T3', 3, 31, 36, 750, 50, 0.5, 0.8, 0.75),
                    ('T4', 4, 25, 30, 1000, 30, 0.35, 0.65, 0.6),
                    ('T5', 5, 18, 24, 1500, 1, 0.2, 0.45, 0.4)
                ],
                'item_types': ['ring', 'amulet', 'body_armour', 'helmet', 'gloves', 'boots', 'belt'],
                'essence_sources': ['Essence of Anger'],
                'fossil_affinities': ['Prismatic Fossil'],
                'meta_rating': 0.95,
                'crafting_difficulty': 0.25,
                'synergies': ['Cold Resistance', 'Lightning Resistance'],
                'description': 'Resistance to fire damage'
            },
            'Cold Resistance': {
                'display_name': 'Cold Resistance',
                'type': 'suffix',
                'category': 'resistance',
                'tiers': [
                    ('T1', 1, 43, 48, 250, 85, 0.8, 0.95, 0.9),
                    ('T2', 2, 37, 42, 500, 70, 0.65, 0.9, 0.85),
                    ('T3', 3, 31, 36, 750, 50, 0.5, 0.8, 0.75),
                    ('T4', 4, 25, 30, 1000, 30, 0.35, 0.65, 0.6),
                    ('T5', 5, 18, 24, 1500, 1, 0.2, 0.45, 0.4)
                ],
                'item_types': ['ring', 'amulet', 'body_armour', 'helmet', 'gloves', 'boots', 'belt'],
                'essence_sources': ['Essence of Hatred'],
                'fossil_affinities': ['Prismatic Fossil'],
                'meta_rating': 0.95,
                'crafting_difficulty': 0.25,
                'synergies': ['Fire Resistance', 'Lightning Resistance'],
                'description': 'Resistance to cold damage'
            },
            'Lightning Resistance': {
                'display_name': 'Lightning Resistance',
                'type': 'suffix',
                'category': 'resistance',
                'tiers': [
                    ('T1', 1, 43, 48, 250, 85, 0.8, 0.95, 0.9),
                    ('T2', 2, 37, 42, 500, 70, 0.65, 0.9, 0.85),
                    ('T3', 3, 31, 36, 750, 50, 0.5, 0.8, 0.75),
                    ('T4', 4, 25, 30, 1000, 30, 0.35, 0.65, 0.6),
                    ('T5', 5, 18, 24, 1500, 1, 0.2, 0.45, 0.4)
                ],
                'item_types': ['ring', 'amulet', 'body_armour', 'helmet', 'gloves', 'boots', 'belt'],
                'essence_sources': ['Essence of Wrath'],
                'fossil_affinities': ['Prismatic Fossil'],
                'meta_rating': 0.95,
                'crafting_difficulty': 0.25,
                'synergies': ['Fire Resistance', 'Cold Resistance'],
                'description': 'Resistance to lightning damage'
            }
        })
        
        # Load build archetypes
        self._load_build_archetypes()
    
    def _add_modifier_family(self, family_name: str, modifiers: Dict[str, Dict]):
        """Add a family of related modifiers"""
        for mod_name, mod_data in modifiers.items():
            tiers = []
            for tier_data in mod_data['tiers']:
                tier = ModifierTier(
                    tier=tier_data[0],
                    tier_number=tier_data[1],
                    value_min=tier_data[2],
                    value_max=tier_data[3],
                    weight=tier_data[4],
                    ilvl_requirement=tier_data[5],
                    rarity_factor=tier_data[6],
                    meta_popularity=tier_data[7],
                    market_demand=tier_data[8]
                )
                tiers.append(tier)
            
            modifier = ModifierData(
                name=mod_name,
                display_name=mod_data['display_name'],
                type=mod_data['type'],
                category=mod_data['category'],
                tiers=tiers,
                item_types=mod_data['item_types'],
                tags=[family_name, mod_data['category'], mod_data['type']],
                essence_sources=mod_data['essence_sources'],
                fossil_affinities=mod_data['fossil_affinities'],
                meta_rating=mod_data['meta_rating'],
                crafting_difficulty=mod_data['crafting_difficulty'],
                synergies=mod_data['synergies'],
                conflicts=mod_data.get('conflicts', []),
                description=mod_data['description'],
                patch_history=[]
            )
            
            self.modifiers[mod_name] = modifier
            self.modifier_categories[mod_data['category']].append(mod_name)
            
            for item_type in mod_data['item_types']:
                self.item_type_modifiers[item_type].append(mod_name)
    
    def _load_build_archetypes(self):
        """Load popular build archetypes and their preferred modifiers"""
        self.build_archetypes = {
            'Life-based Melee': {
                'core_modifiers': ['Maximum Life', 'Life Regeneration', 'Attack Speed', 'Fire Resistance', 'Cold Resistance', 'Lightning Resistance'],
                'secondary_modifiers': ['Critical Strike Chance', 'Accuracy Rating'],
                'popularity': 0.85,
                'meta_tags': ['beginner_friendly', 'league_starter', 'tanky']
            },
            'Energy Shield Caster': {
                'core_modifiers': ['Maximum Energy Shield', '% Energy Shield', 'Fire Resistance', 'Cold Resistance', 'Lightning Resistance'],
                'secondary_modifiers': ['Spell Damage', 'Critical Strike Chance'],
                'popularity': 0.7,
                'meta_tags': ['endgame', 'high_investment', 'glass_cannon']
            },
            'Hybrid Life/ES': {
                'core_modifiers': ['Maximum Life', 'Maximum Energy Shield', 'Fire Resistance', 'Cold Resistance', 'Lightning Resistance'],
                'secondary_modifiers': ['Life Regeneration', '% Energy Shield'],
                'popularity': 0.6,
                'meta_tags': ['balanced', 'versatile', 'moderate_investment']
            },
            'Critical Strike Build': {
                'core_modifiers': ['Critical Strike Chance', 'Critical Strike Multiplier', 'Attack Speed', 'Maximum Life'],
                'secondary_modifiers': ['Accuracy Rating', 'Fire Resistance', 'Cold Resistance'],
                'popularity': 0.75,
                'meta_tags': ['high_damage', 'endgame', 'skill_dependent']
            }
        }
    
    def get_modifier_info(self, modifier_name: str) -> Optional[ModifierData]:
        """Get complete information about a modifier"""
        return self.modifiers.get(modifier_name)
    
    def get_best_tier_for_ilvl(self, modifier_name: str, item_level: int) -> Optional[ModifierTier]:
        """Get the best available tier for a given item level"""
        modifier = self.modifiers.get(modifier_name)
        if not modifier:
            return None
        
        available_tiers = [tier for tier in modifier.tiers if tier.ilvl_requirement <= item_level]
        return min(available_tiers, key=lambda t: t.tier_number) if available_tiers else None
    
    def analyze_modifier_combination(self, modifiers: List[str], item_type: str) -> Dict[str, Any]:
        """Analyze a combination of modifiers for compatibility and efficiency"""
        
        if not modifiers:
            return {'error': 'No modifiers provided'}
        
        analysis = {
            'compatibility': True,
            'warnings': [],
            'synergies': [],
            'conflicts': [],
            'prefix_count': 0,
            'suffix_count': 0,
            'item_type_compatibility': {},
            'meta_rating': 0.0,
            'crafting_difficulty': 0.0,
            'build_archetype_matches': []
        }
        
        modifier_objects = []
        
        for mod_name in modifiers:
            mod_data = self.modifiers.get(mod_name)
            if not mod_data:
                analysis['warnings'].append(f"Unknown modifier: {mod_name}")
                continue
            
            modifier_objects.append(mod_data)
            
            # Count prefixes/suffixes
            if mod_data.type == 'prefix':
                analysis['prefix_count'] += 1
            else:
                analysis['suffix_count'] += 1
            
            # Check item type compatibility
            if item_type not in mod_data.item_types:
                analysis['warnings'].append(f"{mod_name} not available on {item_type}")
                analysis['item_type_compatibility'][mod_name] = False
            else:
                analysis['item_type_compatibility'][mod_name] = True
            
            # Accumulate meta rating and difficulty
            analysis['meta_rating'] += mod_data.meta_rating
            analysis['crafting_difficulty'] += mod_data.crafting_difficulty
        
        # Check prefix/suffix limits
        if analysis['prefix_count'] > 3:
            analysis['compatibility'] = False
            analysis['warnings'].append("Too many prefixes (maximum 3)")
        
        if analysis['suffix_count'] > 3:
            analysis['compatibility'] = False
            analysis['warnings'].append("Too many suffixes (maximum 3)")
        
        # Analyze synergies and conflicts
        for i, mod1 in enumerate(modifier_objects):
            for j, mod2 in enumerate(modifier_objects[i+1:], i+1):
                # Check synergies
                if mod2.name in mod1.synergies or mod1.name in mod2.synergies:
                    analysis['synergies'].append((mod1.name, mod2.name))
                
                # Check conflicts
                if mod2.name in mod1.conflicts or mod1.name in mod2.conflicts:
                    analysis['conflicts'].append((mod1.name, mod2.name))
                    analysis['warnings'].append(f"Conflict between {mod1.name} and {mod2.name}")
        
        # Calculate averages
        if modifier_objects:
            analysis['meta_rating'] /= len(modifier_objects)
            analysis['crafting_difficulty'] /= len(modifier_objects)
        
        # Find matching build archetypes
        for archetype_name, archetype_data in self.build_archetypes.items():
            core_mods = set(archetype_data['core_modifiers'])
            provided_mods = set(modifiers)
            
            overlap = len(core_mods.intersection(provided_mods))
            if overlap >= len(core_mods) * 0.6:  # 60% overlap
                match_score = overlap / len(core_mods)
                analysis['build_archetype_matches'].append({
                    'archetype': archetype_name,
                    'match_score': match_score,
                    'popularity': archetype_data['popularity'],
                    'missing_mods': list(core_mods - provided_mods)
                })
        
        # Sort archetype matches by score
        analysis['build_archetype_matches'].sort(key=lambda x: x['match_score'], reverse=True)
        
        return analysis
    
    def suggest_complementary_modifiers(self, existing_modifiers: List[str], 
                                      item_type: str, category_focus: str = None) -> List[Dict[str, Any]]:
        """Suggest modifiers that complement the existing ones"""
        
        suggestions = []
        existing_set = set(existing_modifiers)
        
        # Get existing modifier data
        existing_mod_objects = [self.modifiers[mod] for mod in existing_modifiers if mod in self.modifiers]
        
        # Count existing prefixes/suffixes
        prefix_count = sum(1 for mod in existing_mod_objects if mod.type == 'prefix')
        suffix_count = sum(1 for mod in existing_mod_objects if mod.type == 'suffix')
        
        # Determine available slots
        available_prefixes = 3 - prefix_count
        available_suffixes = 3 - suffix_count
        
        # Find synergistic modifiers
        synergy_candidates = set()
        for mod in existing_mod_objects:
            for synergy in mod.synergies:
                if synergy in self.modifiers and synergy not in existing_set:
                    synergy_candidates.add(synergy)
        
        # Evaluate all possible modifiers
        for mod_name, mod_data in self.modifiers.items():
            if mod_name in existing_set:
                continue
            
            if item_type not in mod_data.item_types:
                continue
            
            # Check slot availability
            if mod_data.type == 'prefix' and available_prefixes <= 0:
                continue
            if mod_data.type == 'suffix' and available_suffixes <= 0:
                continue
            
            # Calculate suggestion score
            score = 0.0
            
            # Base meta rating
            score += mod_data.meta_rating * 0.3
            
            # Synergy bonus
            if mod_name in synergy_candidates:
                score += 0.4
            
            # Category focus bonus
            if category_focus and mod_data.category == category_focus:
                score += 0.2
            
            # Ease of crafting bonus (inverse of difficulty)
            score += (1 - mod_data.crafting_difficulty) * 0.1
            
            # Build archetype relevance
            archetype_relevance = 0.0
            for archetype_data in self.build_archetypes.values():
                if mod_name in archetype_data['core_modifiers']:
                    archetype_relevance += archetype_data['popularity']
            score += min(0.3, archetype_relevance * 0.3)
            
            if score > 0.3:  # Minimum threshold
                suggestions.append({
                    'modifier': mod_name,
                    'score': score,
                    'type': mod_data.type,
                    'category': mod_data.category,
                    'meta_rating': mod_data.meta_rating,
                    'crafting_difficulty': mod_data.crafting_difficulty,
                    'reason': self._get_suggestion_reason(mod_name, existing_modifiers, synergy_candidates, category_focus)
                })
        
        # Sort by score and return top suggestions
        suggestions.sort(key=lambda x: x['score'], reverse=True)
        return suggestions[:10]
    
    def _get_suggestion_reason(self, mod_name: str, existing_mods: List[str], 
                             synergy_candidates: set, category_focus: str) -> str:
        """Generate reason for modifier suggestion"""
        reasons = []
        
        if mod_name in synergy_candidates:
            reasons.append("synergizes with existing modifiers")
        
        mod_data = self.modifiers[mod_name]
        
        if mod_data.meta_rating > 0.8:
            reasons.append("highly popular in current meta")
        
        if category_focus and mod_data.category == category_focus:
            reasons.append(f"fits {category_focus} focus")
        
        if mod_data.crafting_difficulty < 0.4:
            reasons.append("relatively easy to craft")
        
        if not reasons:
            reasons.append("good general modifier")
        
        return ", ".join(reasons)
    
    def generate_meta_analysis(self, league: str = "Current", timeframe: str = "30d") -> MetaAnalysis:
        """Generate comprehensive meta analysis"""
        
        # Calculate modifier popularity based on meta ratings and build archetypes
        modifier_popularity = {}
        
        for mod_name, mod_data in self.modifiers.items():
            # Base popularity from meta rating
            popularity = mod_data.meta_rating * 0.5
            
            # Bonus from build archetype inclusion
            archetype_bonus = 0.0
            for archetype_data in self.build_archetypes.values():
                if mod_name in archetype_data['core_modifiers']:
                    archetype_bonus += archetype_data['popularity'] * 0.3
                elif mod_name in archetype_data.get('secondary_modifiers', []):
                    archetype_bonus += archetype_data['popularity'] * 0.1
            
            popularity += min(0.5, archetype_bonus)
            modifier_popularity[mod_name] = popularity
        
        # Sort by popularity
        top_modifiers = sorted(modifier_popularity.items(), key=lambda x: x[1], reverse=True)[:20]
        
        # Identify emerging trends (high meta rating, low current usage)
        emerging_trends = []
        for mod_name, mod_data in self.modifiers.items():
            if mod_data.meta_rating > 0.7 and modifier_popularity[mod_name] < 0.6:
                emerging_trends.append(mod_name)
        
        # Identify declining modifiers (low meta rating, historically popular)
        declining_modifiers = []
        for mod_name, mod_data in self.modifiers.items():
            if mod_data.meta_rating < 0.5 and modifier_popularity[mod_name] > 0.4:
                declining_modifiers.append(mod_name)
        
        # Build archetype preferences
        build_archetypes = {}
        for archetype_name, archetype_data in self.build_archetypes.items():
            build_archetypes[archetype_name] = archetype_data['core_modifiers'] + archetype_data.get('secondary_modifiers', [])
        
        # Price trends (simplified - would be based on market data)
        price_trends = {}
        for mod_name in self.modifiers.keys():
            # Simulate price trend based on popularity
            pop = modifier_popularity[mod_name]
            price_trends[mod_name] = (pop - 0.5) * 0.2  # -10% to +10% trend
        
        # Craft efficiency (inverse of difficulty weighted by popularity)
        craft_efficiency = {}
        for mod_name, mod_data in self.modifiers.items():
            efficiency = (1 - mod_data.crafting_difficulty) * modifier_popularity[mod_name]
            craft_efficiency[mod_name] = efficiency
        
        return MetaAnalysis(
            league=league,
            timeframe=timeframe,
            top_modifiers=top_modifiers,
            emerging_trends=emerging_trends[:10],
            declining_modifiers=declining_modifiers[:10],
            build_archetypes=build_archetypes,
            price_trends=price_trends,
            craft_efficiency=craft_efficiency,
            generated_at=datetime.now().isoformat()
        )
    
    def get_modifier_statistics(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        stats = {
            'total_modifiers': len(self.modifiers),
            'by_type': defaultdict(int),
            'by_category': defaultdict(int),
            'by_item_type': defaultdict(int),
            'meta_rating_distribution': {},
            'crafting_difficulty_distribution': {},
            'tier_distribution': defaultdict(int)
        }
        
        meta_ratings = []
        crafting_difficulties = []
        
        for mod_data in self.modifiers.values():
            stats['by_type'][mod_data.type] += 1
            stats['by_category'][mod_data.category] += 1
            
            for item_type in mod_data.item_types:
                stats['by_item_type'][item_type] += 1
            
            meta_ratings.append(mod_data.meta_rating)
            crafting_difficulties.append(mod_data.crafting_difficulty)
            
            for tier in mod_data.tiers:
                stats['tier_distribution'][tier.tier] += 1
        
        # Calculate distributions
        if meta_ratings:
            stats['meta_rating_distribution'] = {
                'mean': np.mean(meta_ratings),
                'median': np.median(meta_ratings),
                'std': np.std(meta_ratings),
                'high_meta': len([r for r in meta_ratings if r > 0.8])
            }
        
        if crafting_difficulties:
            stats['crafting_difficulty_distribution'] = {
                'mean': np.mean(crafting_difficulties),
                'median': np.median(crafting_difficulties),
                'std': np.std(crafting_difficulties),
                'easy_to_craft': len([d for d in crafting_difficulties if d < 0.4])
            }
        
        return dict(stats)
    
    def export_database(self, file_path: str):
        """Export the complete modifier database"""
        export_data = {
            'modifiers': {name: asdict(data) for name, data in self.modifiers.items()},
            'build_archetypes': self.build_archetypes,
            'database_stats': self.get_modifier_statistics(),
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2)


# Global enhanced modifier database instance
enhanced_modifier_db = EnhancedModifierDatabase()