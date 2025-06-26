"""
Flask Crafting Module for Path of Exile
Specialized crafting logic for flasks, separated from gear/armour crafting
"""

import random
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class FlaskType(Enum):
    """Flask types in Path of Exile"""
    LIFE = "Life Flask"
    MANA = "Mana Flask"
    HYBRID = "Hybrid Flask"
    DIAMOND = "Diamond Flask"
    GRANITE = "Granite Flask"
    JADE = "Jade Flask"
    QUARTZ = "Quartz Flask"
    QUICKSILVER = "Quicksilver Flask"
    BISMUTH = "Bismuth Flask"
    AMETHYST = "Amethyst Flask"
    RUBY = "Ruby Flask"
    SAPPHIRE = "Sapphire Flask"
    TOPAZ = "Topaz Flask"
    AQUAMARINE = "Aquamarine Flask"
    SULPHUR = "Sulphur Flask"
    BASALT = "Basalt Flask"
    SILVER = "Silver Flask"
    STIBNITE = "Stibnite Flask"
    GOLD = "Gold Flask"


@dataclass
class FlaskModifier:
    """Flask modifier data"""
    name: str
    tier: int
    min_roll: float
    max_roll: float
    mod_type: str  # prefix or suffix
    weight: int
    required_level: int = 1
    tags: List[str] = None


@dataclass
class FlaskCraftingResult:
    """Result of a flask crafting attempt"""
    success: bool
    flask_type: FlaskType
    modifiers: List[FlaskModifier]
    quality: int
    cost: Dict[str, int]
    attempts: int
    final_stats: Dict[str, float]


class FlaskCraftingEngine:
    """Specialized engine for flask crafting"""
    
    def __init__(self):
        self.flask_modifiers = self._initialize_flask_modifiers()
        self.flask_bases = self._initialize_flask_bases()
        
    def _initialize_flask_modifiers(self) -> Dict[str, List[FlaskModifier]]:
        """Initialize all possible flask modifiers"""
        return {
            'prefix': [
                # Utility prefixes
                FlaskModifier("Surgeon's", 1, 1, 1, "prefix", 1000, 8, ["charge_on_crit"]),
                FlaskModifier("Alchemist's", 1, 25, 25, "prefix", 1000, 20, ["increased_effect"]),
                FlaskModifier("Experimenter's", 1, 30, 40, "prefix", 1000, 20, ["increased_duration"]),
                FlaskModifier("Chemist's", 1, 20, 25, "prefix", 1000, 20, ["reduced_charges"]),
                FlaskModifier("Perpetual", 1, 1, 3, "prefix", 500, 1, ["charges_per_3_seconds"]),
                FlaskModifier("Ample", 1, 10, 20, "prefix", 1000, 1, ["increased_charges"]),
                FlaskModifier("Cautious", 1, 40, 60, "prefix", 500, 7, ["recovery_when_hit"]),
                FlaskModifier("Bubbling", 1, 50, 50, "prefix", 1000, 7, ["instant_recovery"]),
                FlaskModifier("Seething", 1, 66, 66, "prefix", 1000, 18, ["instant_recovery"]),
                FlaskModifier("Catalysed", 1, 15, 25, "prefix", 1000, 30, ["recovery_rate"]),
                FlaskModifier("Saturated", 1, 33, 33, "prefix", 1000, 7, ["instant_low_life"]),
                FlaskModifier("Panicked", 1, 15, 25, "prefix", 1000, 7, ["instant_low_life_end"]),
            ],
            'suffix': [
                # Immunity suffixes
                FlaskModifier("of Staunching", 1, 1, 1, "suffix", 1000, 8, ["bleed_immune"]),
                FlaskModifier("of Heat", 1, 1, 1, "suffix", 1000, 4, ["freeze_immune"]),
                FlaskModifier("of Dousing", 1, 1, 1, "suffix", 1000, 1, ["ignite_immune"]),
                FlaskModifier("of Grounding", 1, 1, 1, "suffix", 1000, 10, ["shock_immune"]),
                FlaskModifier("of Curing", 1, 1, 1, "suffix", 1000, 16, ["poison_immune"]),
                FlaskModifier("of Warding", 1, 1, 1, "suffix", 1000, 18, ["curse_immune"]),
                # Utility suffixes
                FlaskModifier("of Adrenaline", 1, 20, 30, "suffix", 1000, 5, ["movement_speed"]),
                FlaskModifier("of Quickening", 1, 10, 17, "suffix", 500, 30, ["attack_speed"]),
                FlaskModifier("of the Dove", 1, 20, 30, "suffix", 500, 12, ["reduced_crit_taken"]),
                FlaskModifier("of the Skunk", 1, 20, 30, "suffix", 500, 14, ["evasion_rating"]),
                FlaskModifier("of the Armadillo", 1, 40, 60, "suffix", 500, 8, ["armor"]),
                FlaskModifier("of the Conger", 1, 60, 90, "suffix", 250, 30, ["lightning_resistance"]),
                FlaskModifier("of the Walrus", 1, 60, 90, "suffix", 250, 30, ["cold_resistance"]),
                FlaskModifier("of the Salamander", 1, 60, 90, "suffix", 250, 30, ["fire_resistance"]),
            ]
        }
    
    def _initialize_flask_bases(self) -> Dict[FlaskType, Dict]:
        """Initialize flask base properties"""
        return {
            FlaskType.LIFE: {"life_recovery": (300, 1000), "duration": 3.0, "charges": (21, 60)},
            FlaskType.MANA: {"mana_recovery": (50, 170), "duration": 4.0, "charges": (21, 60)},
            FlaskType.HYBRID: {"recovery": (140, 470), "duration": 5.0, "charges": (20, 40)},
            FlaskType.DIAMOND: {"crit_chance": 100, "duration": 4.0, "charges": (20, 40)},
            FlaskType.GRANITE: {"armor": (1500, 3000), "duration": 4.0, "charges": (30, 60)},
            FlaskType.JADE: {"evasion": (1500, 3000), "duration": 4.0, "charges": (30, 60)},
            FlaskType.QUARTZ: {"phasing": True, "dodge": 10, "duration": 4.0, "charges": (30, 60)},
            FlaskType.QUICKSILVER: {"movement_speed": 40, "duration": 4.0, "charges": (20, 50)},
            FlaskType.BISMUTH: {"elemental_res": 35, "duration": 5.0, "charges": (15, 40)},
            FlaskType.AMETHYST: {"chaos_res": 35, "duration": 3.5, "charges": (35, 65)},
            FlaskType.RUBY: {"fire_res": 50, "fire_damage_taken": -20, "duration": 3.5, "charges": (30, 60)},
            FlaskType.SAPPHIRE: {"cold_res": 50, "cold_damage_taken": -20, "duration": 3.5, "charges": (30, 60)},
            FlaskType.TOPAZ: {"lightning_res": 50, "lightning_damage_taken": -20, "duration": 3.5, "charges": (30, 60)},
            FlaskType.AQUAMARINE: {"freeze_chance": 15, "chill_effect": 0, "duration": 5.0, "charges": (20, 50)},
            FlaskType.SULPHUR: {"consecrated_ground": True, "damage": 40, "duration": 3.5, "charges": (20, 50)},
            FlaskType.BASALT: {"physical_damage_taken": -20, "armor": 0, "duration": 4.5, "charges": (20, 50)},
            FlaskType.SILVER: {"onslaught": True, "duration": 5.0, "charges": (20, 50)},
            FlaskType.STIBNITE: {"smoke_cloud": True, "evasion": 100, "duration": 5.0, "charges": (15, 40)},
            FlaskType.GOLD: {"item_rarity": (20, 30), "duration": 3.0, "charges": (20, 50)},
        }
    
    def detect_flask_type(self, item_base: str) -> Optional[FlaskType]:
        """Detect flask type from item base name"""
        item_lower = item_base.lower()
        for flask_type in FlaskType:
            if flask_type.value.lower() in item_lower:
                return flask_type
        return None
    
    def get_available_modifiers(self, flask_type: FlaskType, item_level: int) -> Dict[str, List[FlaskModifier]]:
        """Get available modifiers for a flask based on type and item level"""
        available = {'prefix': [], 'suffix': []}
        
        for mod_type in ['prefix', 'suffix']:
            for modifier in self.flask_modifiers[mod_type]:
                if modifier.required_level <= item_level:
                    # Some modifiers are restricted to certain flask types
                    if self._is_modifier_valid_for_flask(modifier, flask_type):
                        available[mod_type].append(modifier)
        
        return available
    
    def _is_modifier_valid_for_flask(self, modifier: FlaskModifier, flask_type: FlaskType) -> bool:
        """Check if a modifier can appear on a specific flask type"""
        # Life/Mana recovery modifiers only on life/mana/hybrid flasks
        recovery_mods = ["instant_recovery", "recovery_rate", "instant_low_life", "instant_low_life_end", "recovery_when_hit"]
        if any(tag in modifier.tags for tag in recovery_mods if modifier.tags):
            return flask_type in [FlaskType.LIFE, FlaskType.MANA, FlaskType.HYBRID]
        
        # All other modifiers can appear on any flask
        return True
    
    def simulate_alteration_crafting(self, flask_type: FlaskType, target_modifiers: List[str], 
                                   budget: float, item_level: int = 85) -> FlaskCraftingResult:
        """Simulate alteration spam crafting for flasks"""
        currency_costs = {
            'Orb of Alteration': 0.1,
            'Orb of Augmentation': 0.5,
            'Orb of Transmutation': 0.2,
            'Glassblowers Bauble': 1.0
        }
        
        costs = {
            'Orb of Alteration': 0,
            'Orb of Augmentation': 0,
            'Orb of Transmutation': 1,  # Initial transmute
            'Glassblowers Bauble': 4    # 20% quality
        }
        
        attempts = 0
        max_attempts = int(budget / currency_costs['Orb of Alteration'])
        
        available_mods = self.get_available_modifiers(flask_type, item_level)
        final_modifiers = []
        
        while attempts < max_attempts:
            attempts += 1
            costs['Orb of Alteration'] += 1
            
            # Roll 1-2 modifiers
            num_mods = random.choices([1, 2], weights=[60, 40])[0]
            
            if num_mods == 1:
                # Roll single modifier
                mod_type = random.choice(['prefix', 'suffix'])
                modifier = self._roll_modifier(available_mods[mod_type])
                
                # Check if we hit a target
                if self._matches_target(modifier, target_modifiers):
                    # Try to augment for second mod
                    costs['Orb of Augmentation'] += 1
                    other_type = 'suffix' if mod_type == 'prefix' else 'prefix'
                    second_mod = self._roll_modifier(available_mods[other_type])
                    
                    final_modifiers = [modifier, second_mod]
                    if self._matches_target(second_mod, target_modifiers):
                        # Perfect roll!
                        break
            else:
                # Roll two modifiers
                prefix = self._roll_modifier(available_mods['prefix'])
                suffix = self._roll_modifier(available_mods['suffix'])
                
                prefix_match = self._matches_target(prefix, target_modifiers)
                suffix_match = self._matches_target(suffix, target_modifiers)
                
                if prefix_match and suffix_match:
                    final_modifiers = [prefix, suffix]
                    break
                elif prefix_match or suffix_match:
                    # Keep rolling for perfect combination
                    final_modifiers = [prefix, suffix]
        
        # Calculate total cost
        total_cost = sum(costs[currency] * currency_costs[currency] for currency in costs)
        
        # Generate final stats
        final_stats = self._calculate_flask_stats(flask_type, final_modifiers, quality=20)
        
        return FlaskCraftingResult(
            success=len(final_modifiers) > 0 and any(self._matches_target(mod, target_modifiers) for mod in final_modifiers),
            flask_type=flask_type,
            modifiers=final_modifiers,
            quality=20,
            cost=costs,
            attempts=attempts,
            final_stats=final_stats
        )
    
    def _roll_modifier(self, modifier_pool: List[FlaskModifier]) -> FlaskModifier:
        """Roll a random modifier from the pool with weighted selection"""
        if not modifier_pool:
            return None
        
        weights = [mod.weight for mod in modifier_pool]
        selected = random.choices(modifier_pool, weights=weights)[0]
        
        # Roll the value within the modifier's range
        if selected.min_roll != selected.max_roll:
            roll_value = random.uniform(selected.min_roll, selected.max_roll)
        else:
            roll_value = selected.min_roll
        
        # Create a copy with the rolled value
        rolled_mod = FlaskModifier(
            name=selected.name,
            tier=selected.tier,
            min_roll=roll_value,
            max_roll=roll_value,
            mod_type=selected.mod_type,
            weight=selected.weight,
            required_level=selected.required_level,
            tags=selected.tags
        )
        
        return rolled_mod
    
    def _matches_target(self, modifier: FlaskModifier, targets: List[str]) -> bool:
        """Check if a modifier matches any target modifier"""
        if not modifier:
            return False
        
        mod_lower = modifier.name.lower()
        for target in targets:
            target_lower = target.lower()
            # Check name match
            if target_lower in mod_lower or mod_lower in target_lower:
                return True
            # Check tag match
            if modifier.tags:
                for tag in modifier.tags:
                    if tag.lower() in target_lower:
                        return True
        
        return False
    
    def _calculate_flask_stats(self, flask_type: FlaskType, modifiers: List[FlaskModifier], quality: int) -> Dict[str, float]:
        """Calculate final flask statistics"""
        base_stats = self.flask_bases[flask_type].copy()
        final_stats = {}
        
        # Apply quality bonus (affects recovery amount and duration)
        quality_bonus = quality / 100.0
        
        # Apply base stats
        for stat, value in base_stats.items():
            if isinstance(value, tuple):
                # Use average for ranges
                final_stats[stat] = sum(value) / 2 * (1 + quality_bonus)
            elif isinstance(value, (int, float)):
                if stat == 'duration':
                    final_stats[stat] = value
                else:
                    final_stats[stat] = value * (1 + quality_bonus)
            else:
                final_stats[stat] = value
        
        # Apply modifiers
        for modifier in modifiers:
            if not modifier:
                continue
                
            # Apply modifier effects based on tags
            if modifier.tags:
                for tag in modifier.tags:
                    if tag == "increased_effect":
                        # Alchemist's increases effect
                        for stat in final_stats:
                            if stat not in ['duration', 'charges']:
                                final_stats[stat] *= (1 + modifier.min_roll / 100)
                    elif tag == "increased_duration":
                        # Experimenter's increases duration
                        final_stats['duration'] *= (1 + modifier.min_roll / 100)
                    elif tag == "reduced_charges":
                        # Chemist's reduces charges used
                        final_stats['charges_used'] = -(modifier.min_roll)
                    elif tag == "movement_speed":
                        final_stats['movement_speed_bonus'] = modifier.min_roll
                    # Add more modifier effects as needed
        
        return final_stats
    
    def generate_crafting_strategy(self, flask_type: FlaskType, target_modifiers: List[str], 
                                 budget: float, preferences: Dict = None) -> Dict:
        """Generate optimal crafting strategy for flasks"""
        strategy = {
            'method': 'alteration_spam',
            'expected_cost': 0,
            'success_probability': 0,
            'steps': [],
            'alternatives': [],
            'tips': []
        }
        
        # Calculate probability of hitting targets
        available_mods = self.get_available_modifiers(flask_type, 85)
        total_prefix_weight = sum(mod.weight for mod in available_mods['prefix'])
        total_suffix_weight = sum(mod.weight for mod in available_mods['suffix'])
        
        # Find target modifiers in the pool
        target_prefix_found = False
        target_suffix_found = False
        
        for target in target_modifiers:
            for prefix in available_mods['prefix']:
                if self._matches_target(prefix, [target]):
                    target_prefix_found = True
                    strategy['success_probability'] += prefix.weight / total_prefix_weight
            
            for suffix in available_mods['suffix']:
                if self._matches_target(suffix, [target]):
                    target_suffix_found = True
                    strategy['success_probability'] += suffix.weight / total_suffix_weight
        
        # Adjust probability for needing both
        if target_prefix_found and target_suffix_found:
            strategy['success_probability'] *= 0.4  # Chance of rolling 2 mods
        
        # Estimate cost based on probability
        if strategy['success_probability'] > 0:
            expected_attempts = 1 / strategy['success_probability']
            strategy['expected_cost'] = expected_attempts * 0.1 + 5  # Alts + quality
        else:
            strategy['expected_cost'] = float('inf')
        
        # Generate steps
        strategy['steps'] = [
            f"1. Acquire a {flask_type.value} (item level 85+ recommended)",
            "2. Use 4 Glassblower's Baubles to achieve 20% quality",
            "3. Use Orb of Transmutation to make the flask magic (blue)",
            f"4. Spam Orb of Alteration until you hit: {', '.join(target_modifiers)}",
            "5. If you get only one desired mod, use Orb of Augmentation",
            "6. Repeat steps 4-5 until you get the desired combination"
        ]
        
        # Add tips
        strategy['tips'] = [
            f"Expected attempts: {int(1/strategy['success_probability']) if strategy['success_probability'] > 0 else 'Unknown'}",
            "Consider buying flasks with one desired mod already rolled",
            "Quality improves recovery amount and effect duration",
            "Some modifiers are mutually exclusive (check prefix/suffix)",
            "Beast-crafting can add 'of Staunching' or 'of Heat' deterministically"
        ]
        
        return strategy


class FlaskCraftingOptimizer:
    """Optimizer for flask crafting strategies"""
    
    def __init__(self, crafting_engine: FlaskCraftingEngine):
        self.engine = crafting_engine
        self.market_data = {}
    
    def update_market_prices(self, prices: Dict[str, float]):
        """Update market prices for currency"""
        self.market_data = prices
    
    def find_optimal_strategy(self, flask_type: FlaskType, target_modifiers: List[str], 
                            constraints: Dict = None) -> Dict:
        """Find the most cost-effective crafting strategy"""
        constraints = constraints or {'budget': 1000, 'time': 'medium', 'risk': 'medium'}
        
        strategies = []
        
        # Strategy 1: Alteration spam
        alt_strategy = self._evaluate_alteration_strategy(flask_type, target_modifiers, constraints)
        strategies.append(alt_strategy)
        
        # Strategy 2: Buy and divine
        buy_strategy = self._evaluate_buy_strategy(flask_type, target_modifiers, constraints)
        strategies.append(buy_strategy)
        
        # Strategy 3: Beast crafting for specific mods
        beast_strategy = self._evaluate_beast_strategy(flask_type, target_modifiers, constraints)
        strategies.append(beast_strategy)
        
        # Sort by efficiency score
        strategies.sort(key=lambda x: x['efficiency_score'], reverse=True)
        
        return {
            'recommended': strategies[0],
            'alternatives': strategies[1:],
            'comparison': self._generate_comparison(strategies)
        }
    
    def _evaluate_alteration_strategy(self, flask_type: FlaskType, targets: List[str], constraints: Dict) -> Dict:
        """Evaluate alteration spam strategy"""
        strategy = self.engine.generate_crafting_strategy(flask_type, targets, constraints['budget'])
        
        # Calculate efficiency score
        time_factor = 0.5 if constraints['time'] == 'fast' else 1.0
        risk_factor = 1.2 if constraints['risk'] == 'low' else 1.0
        
        efficiency = (1 / strategy['expected_cost']) * strategy['success_probability'] * time_factor * risk_factor
        
        return {
            'name': 'Alteration Spam',
            'expected_cost': strategy['expected_cost'],
            'time_estimate': 'Medium (10-30 minutes)',
            'risk': 'Low',
            'efficiency_score': efficiency,
            'details': strategy
        }
    
    def _evaluate_buy_strategy(self, flask_type: FlaskType, targets: List[str], constraints: Dict) -> Dict:
        """Evaluate buying pre-rolled flask strategy"""
        # Estimate market price (simplified)
        base_price = 5.0
        mod_multiplier = len(targets) * 2.5
        estimated_price = base_price * mod_multiplier
        
        return {
            'name': 'Buy Pre-rolled',
            'expected_cost': estimated_price,
            'time_estimate': 'Fast (5 minutes)',
            'risk': 'Very Low',
            'efficiency_score': 1 / estimated_price * 2,  # Time bonus
            'details': {
                'steps': [
                    'Search trade site for the desired flask',
                    'Filter by your required modifiers',
                    'Compare prices and choose best value',
                    'Whisper seller and complete trade'
                ]
            }
        }
    
    def _evaluate_beast_strategy(self, flask_type: FlaskType, targets: List[str], constraints: Dict) -> Dict:
        """Evaluate beast crafting strategy"""
        # Check if any targets can be beast-crafted
        beast_mods = ['of Staunching', 'of Heat', 'of Dousing', 'of Grounding']
        applicable = any(mod in target for target in targets for mod in beast_mods)
        
        if not applicable:
            return {
                'name': 'Beast Crafting',
                'expected_cost': float('inf'),
                'time_estimate': 'N/A',
                'risk': 'N/A',
                'efficiency_score': 0,
                'details': {'steps': ['Not applicable for these modifiers']}
            }
        
        return {
            'name': 'Beast Crafting',
            'expected_cost': 10,  # Approximate beast cost
            'time_estimate': 'Fast (5 minutes)',
            'risk': 'Very Low',
            'efficiency_score': 0.8,
            'details': {
                'steps': [
                    'Acquire Einhar\'s beast for "of Staunching" or immunity suffix',
                    'Get a flask with desired prefix',
                    'Use beast crafting to add the suffix deterministically',
                    'This guarantees the suffix but requires good prefix first'
                ]
            }
        }
    
    def _generate_comparison(self, strategies: List[Dict]) -> Dict:
        """Generate comparison between strategies"""
        return {
            'cost_comparison': {s['name']: s['expected_cost'] for s in strategies},
            'time_comparison': {s['name']: s['time_estimate'] for s in strategies},
            'risk_comparison': {s['name']: s['risk'] for s in strategies},
            'recommendation_reason': f"Recommended {strategies[0]['name']} due to highest efficiency score"
        }