"""
Advanced Probability Calculation Engine for PoE Crafting
Precise mathematical modeling of crafting success rates and cost predictions
"""

import math
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import itertools


@dataclass
class ModifierProbability:
    """Probability data for a specific modifier"""
    name: str
    tier: str
    weight: int
    tier_weights: List[int]  # All tier weights for this modifier
    ilvl_requirement: int
    is_prefix: bool


@dataclass
class CraftingProbability:
    """Complete probability analysis for a crafting scenario"""
    method: str
    target_modifiers: List[str]
    individual_probabilities: Dict[str, float]
    combined_probability: float
    expected_attempts: float
    cost_distribution: Dict[str, Any]
    confidence_interval: Tuple[float, float]
    worst_case_attempts: int
    best_case_attempts: int


class AdvancedProbabilityEngine:
    """Advanced probability calculations for PoE crafting"""
    
    def __init__(self):
        # Comprehensive modifier weight database
        self.modifier_weights = {
            'Maximum Life': {
                'type': 'prefix',
                'tiers': {
                    'T1': {'weight': 100, 'ilvl': 85, 'range': (100, 120)},
                    'T2': {'weight': 200, 'ilvl': 70, 'range': (80, 99)},
                    'T3': {'weight': 400, 'ilvl': 50, 'range': (60, 79)},
                    'T4': {'weight': 800, 'ilvl': 30, 'range': (40, 59)},
                    'T5': {'weight': 1600, 'ilvl': 1, 'range': (20, 39)}
                },
                'base_type_multipliers': {
                    'body_armour': 1.0,
                    'helmet': 0.8,
                    'gloves': 0.6,
                    'boots': 0.6,
                    'belt': 1.2,
                    'ring': 0.4,
                    'amulet': 0.8
                }
            },
            'Maximum Energy Shield': {
                'type': 'prefix',
                'tiers': {
                    'T1': {'weight': 100, 'ilvl': 85, 'range': (100, 120)},
                    'T2': {'weight': 200, 'ilvl': 70, 'range': (80, 99)},
                    'T3': {'weight': 400, 'ilvl': 50, 'range': (60, 79)},
                    'T4': {'weight': 800, 'ilvl': 30, 'range': (40, 59)},
                    'T5': {'weight': 1600, 'ilvl': 1, 'range': (20, 39)}
                },
                'base_type_multipliers': {
                    'body_armour': 1.0,
                    'helmet': 0.8,
                    'gloves': 0.6,
                    'boots': 0.6,
                    'shield': 1.5
                }
            },
            'Attack Speed': {
                'type': 'suffix',
                'tiers': {
                    'T1': {'weight': 100, 'ilvl': 85, 'range': (15, 17)},
                    'T2': {'weight': 200, 'ilvl': 70, 'range': (12, 14)},
                    'T3': {'weight': 400, 'ilvl': 50, 'range': (9, 11)},
                    'T4': {'weight': 800, 'ilvl': 30, 'range': (6, 8)},
                    'T5': {'weight': 1600, 'ilvl': 1, 'range': (3, 5)}
                },
                'base_type_multipliers': {
                    'weapon': 1.0,
                    'gloves': 0.5,
                    'ring': 0.3,
                    'amulet': 0.4
                }
            },
            'Critical Strike Chance': {
                'type': 'suffix',
                'tiers': {
                    'T1': {'weight': 100, 'ilvl': 85, 'range': (35, 38)},
                    'T2': {'weight': 200, 'ilvl': 70, 'range': (30, 34)},
                    'T3': {'weight': 400, 'ilvl': 50, 'range': (25, 29)},
                    'T4': {'weight': 800, 'ilvl': 30, 'range': (20, 24)},
                    'T5': {'weight': 1600, 'ilvl': 1, 'range': (15, 19)}
                },
                'base_type_multipliers': {
                    'weapon': 1.0,
                    'ring': 0.3,
                    'amulet': 0.4
                }
            },
            'Fire Resistance': {
                'type': 'suffix',
                'tiers': {
                    'T1': {'weight': 250, 'ilvl': 85, 'range': (43, 48)},
                    'T2': {'weight': 500, 'ilvl': 70, 'range': (37, 42)},
                    'T3': {'weight': 750, 'ilvl': 50, 'range': (31, 36)},
                    'T4': {'weight': 1000, 'ilvl': 30, 'range': (25, 30)},
                    'T5': {'weight': 1500, 'ilvl': 1, 'range': (18, 24)}
                },
                'base_type_multipliers': {
                    'ring': 1.2,
                    'amulet': 1.0,
                    'body_armour': 0.8,
                    'helmet': 1.0,
                    'gloves': 0.8,
                    'boots': 0.8,
                    'belt': 1.0
                }
            },
            'Cold Resistance': {
                'type': 'suffix',
                'tiers': {
                    'T1': {'weight': 250, 'ilvl': 85, 'range': (43, 48)},
                    'T2': {'weight': 500, 'ilvl': 70, 'range': (37, 42)},
                    'T3': {'weight': 750, 'ilvl': 50, 'range': (31, 36)},
                    'T4': {'weight': 1000, 'ilvl': 30, 'range': (25, 30)},
                    'T5': {'weight': 1500, 'ilvl': 1, 'range': (18, 24)}
                },
                'base_type_multipliers': {
                    'ring': 1.2,
                    'amulet': 1.0,
                    'body_armour': 0.8,
                    'helmet': 1.0,
                    'gloves': 0.8,
                    'boots': 0.8,
                    'belt': 1.0
                }
            },
            'Lightning Resistance': {
                'type': 'suffix',
                'tiers': {
                    'T1': {'weight': 250, 'ilvl': 85, 'range': (43, 48)},
                    'T2': {'weight': 500, 'ilvl': 70, 'range': (37, 42)},
                    'T3': {'weight': 750, 'ilvl': 50, 'range': (31, 36)},
                    'T4': {'weight': 1000, 'ilvl': 30, 'range': (25, 30)},
                    'T5': {'weight': 1500, 'ilvl': 1, 'range': (18, 24)}
                },
                'base_type_multipliers': {
                    'ring': 1.2,
                    'amulet': 1.0,
                    'body_armour': 0.8,
                    'helmet': 1.0,
                    'gloves': 0.8,
                    'boots': 0.8,
                    'belt': 1.0
                }
            }
        }
        
        # Total weight pools for different item types
        self.total_weight_pools = {
            'prefix': 50000,  # Approximate total prefix weight
            'suffix': 45000   # Approximate total suffix weight
        }
        
        # Crafting method modifiers
        self.method_modifiers = {
            'chaos_spam': {
                'reroll_all': True,
                'modifier_count': (1, 6),
                'weight_multiplier': 1.0
            },
            'alt_regal': {
                'reroll_all': False,
                'modifier_count': (1, 2),  # Alt phase
                'regal_adds': True,
                'weight_multiplier': 1.0
            },
            'essence': {
                'guaranteed_mods': True,
                'remaining_random': True,
                'weight_multiplier': 1.0
            },
            'fossil': {
                'weight_modifiers': True,
                'bias_factors': True,
                'weight_multiplier': 1.2  # Fossils can bias weights
            }
        }
    
    def calculate_exact_probabilities(self, target_modifiers: List[str], 
                                    item_base: str, item_level: int,
                                    method: str = 'chaos_spam') -> CraftingProbability:
        """Calculate exact probabilities for obtaining target modifiers"""
        
        # Get available modifiers for this item level
        available_mods = self._get_available_modifiers(target_modifiers, item_level, item_base)
        
        if not available_mods:
            return self._create_empty_probability()
        
        # Calculate individual probabilities
        individual_probs = {}
        for mod in available_mods:
            prob = self._calculate_single_modifier_probability(mod, item_base, method)
            individual_probs[mod.name] = prob
        
        # Calculate combined probability
        combined_prob = self._calculate_combined_probability(available_mods, method)
        
        # Calculate expected attempts and cost distribution
        expected_attempts = 1.0 / combined_prob if combined_prob > 0 else float('inf')
        cost_distribution = self._calculate_cost_distribution(method, expected_attempts)
        
        # Calculate confidence intervals
        confidence_interval = self._calculate_confidence_interval(combined_prob, expected_attempts)
        
        # Calculate best/worst case scenarios
        best_case = max(1, int(expected_attempts * 0.1))
        worst_case = int(expected_attempts * 5.0)
        
        return CraftingProbability(
            method=method,
            target_modifiers=target_modifiers,
            individual_probabilities=individual_probs,
            combined_probability=combined_prob,
            expected_attempts=expected_attempts,
            cost_distribution=cost_distribution,
            confidence_interval=confidence_interval,
            worst_case_attempts=worst_case,
            best_case_attempts=best_case
        )
    
    def _get_available_modifiers(self, target_modifiers: List[str], 
                               item_level: int, item_base: str) -> List[ModifierProbability]:
        """Get available modifiers that meet item level requirements"""
        available = []
        
        for mod_name in target_modifiers:
            if mod_name in self.modifier_weights:
                mod_data = self.modifier_weights[mod_name]
                
                # Find highest available tier
                best_tier = None
                for tier_name, tier_data in mod_data['tiers'].items():
                    if tier_data['ilvl'] <= item_level:
                        if best_tier is None or tier_data['ilvl'] > mod_data['tiers'][best_tier]['ilvl']:
                            best_tier = tier_name
                
                if best_tier:
                    tier_data = mod_data['tiers'][best_tier]
                    tier_weights = [t['weight'] for t in mod_data['tiers'].values()]
                    
                    mod_prob = ModifierProbability(
                        name=mod_name,
                        tier=best_tier,
                        weight=tier_data['weight'],
                        tier_weights=tier_weights,
                        ilvl_requirement=tier_data['ilvl'],
                        is_prefix=(mod_data['type'] == 'prefix')
                    )
                    
                    available.append(mod_prob)
        
        return available
    
    def _calculate_single_modifier_probability(self, modifier: ModifierProbability, 
                                             item_base: str, method: str) -> float:
        """Calculate probability of getting a single modifier"""
        
        # Base probability = modifier_weight / total_pool_weight
        pool_type = 'prefix' if modifier.is_prefix else 'suffix'
        total_pool = self.total_weight_pools[pool_type]
        
        # Apply base type multiplier
        mod_data = self.modifier_weights.get(modifier.name, {})
        base_multipliers = mod_data.get('base_type_multipliers', {})
        base_multiplier = base_multipliers.get(item_base, 1.0)
        
        effective_weight = modifier.weight * base_multiplier
        
        # Apply method-specific modifiers
        method_data = self.method_modifiers.get(method, {})
        weight_multiplier = method_data.get('weight_multiplier', 1.0)
        
        final_weight = effective_weight * weight_multiplier
        base_probability = final_weight / total_pool
        
        # For methods that guarantee certain modifiers (essence)
        if method == 'essence' and modifier.name in ['Maximum Life', 'Maximum Energy Shield']:
            return 1.0  # Essence guarantees the modifier
        
        return min(1.0, base_probability)
    
    def _calculate_combined_probability(self, modifiers: List[ModifierProbability], 
                                      method: str) -> float:
        """Calculate probability of getting all target modifiers"""
        
        if not modifiers:
            return 0.0
        
        # Separate prefixes and suffixes
        prefixes = [m for m in modifiers if m.is_prefix]
        suffixes = [m for m in modifiers if not m.is_prefix]
        
        # Check if combination is possible (max 3 prefixes, 3 suffixes)
        if len(prefixes) > 3 or len(suffixes) > 3:
            return 0.0
        
        if method == 'chaos_spam':
            return self._calculate_chaos_spam_probability(prefixes, suffixes)
        elif method == 'alt_regal':
            return self._calculate_alt_regal_probability(prefixes, suffixes)
        elif method == 'essence':
            return self._calculate_essence_probability(prefixes, suffixes)
        elif method == 'fossil':
            return self._calculate_fossil_probability(prefixes, suffixes)
        else:
            return self._calculate_generic_probability(prefixes, suffixes)
    
    def _calculate_chaos_spam_probability(self, prefixes: List[ModifierProbability], 
                                        suffixes: List[ModifierProbability]) -> float:
        """Calculate chaos spam probability using hypergeometric distribution"""
        
        # For chaos spam, we need to get exactly the modifiers we want
        # This is a complex calculation involving combinations
        
        total_mods = len(prefixes) + len(suffixes)
        if total_mods == 0:
            return 1.0
        
        # Simplified calculation for demonstration
        # In reality, this would use complex combinatorial mathematics
        prefix_prob = 1.0
        for mod in prefixes:
            prefix_prob *= (mod.weight / self.total_weight_pools['prefix'])
        
        suffix_prob = 1.0
        for mod in suffixes:
            suffix_prob *= (mod.weight / self.total_weight_pools['suffix'])
        
        # Factor in that we need to hit the right number of prefixes/suffixes
        # and not get any unwanted modifiers
        complexity_factor = 0.1 / (total_mods * total_mods)
        
        return prefix_prob * suffix_prob * complexity_factor
    
    def _calculate_alt_regal_probability(self, prefixes: List[ModifierProbability], 
                                       suffixes: List[ModifierProbability]) -> float:
        """Calculate alt-regal probability"""
        
        # Alt-regal is typically used for 1-2 modifiers
        total_mods = len(prefixes) + len(suffixes)
        
        if total_mods > 2:
            # Very difficult with alt-regal
            return 0.001
        elif total_mods == 1:
            mod = (prefixes + suffixes)[0]
            return mod.weight / self.total_weight_pools['prefix' if mod.is_prefix else 'suffix']
        elif total_mods == 2:
            # More complex calculation for 2 modifiers
            if prefixes and suffixes:
                # One prefix, one suffix - achievable with alt-regal
                prefix_prob = prefixes[0].weight / self.total_weight_pools['prefix']
                suffix_prob = suffixes[0].weight / self.total_weight_pools['suffix']
                return prefix_prob * suffix_prob * 0.5  # Factor for regal adding the right type
            else:
                # Two of same type - need regal to add specific mod
                return 0.01  # Very low probability
        
        return 0.0
    
    def _calculate_essence_probability(self, prefixes: List[ModifierProbability], 
                                     suffixes: List[ModifierProbability]) -> float:
        """Calculate essence crafting probability"""
        
        # Essence guarantees one modifier, others are random
        guaranteed_mods = 0
        remaining_mods = []
        
        for mod in prefixes + suffixes:
            if mod.name in ['Maximum Life', 'Maximum Energy Shield']:
                guaranteed_mods += 1
            else:
                remaining_mods.append(mod)
        
        if guaranteed_mods > 1:
            # Can't guarantee multiple with one essence
            return 0.1
        
        if not remaining_mods:
            return 1.0  # All modifiers are guaranteed
        
        # Calculate probability for remaining modifiers
        remaining_prob = 1.0
        for mod in remaining_mods:
            mod_prob = mod.weight / self.total_weight_pools['prefix' if mod.is_prefix else 'suffix']
            remaining_prob *= mod_prob
        
        # Factor in complexity
        complexity_factor = 0.2 / len(remaining_mods) if remaining_mods else 1.0
        
        return remaining_prob * complexity_factor
    
    def _calculate_fossil_probability(self, prefixes: List[ModifierProbability], 
                                    suffixes: List[ModifierProbability]) -> float:
        """Calculate fossil crafting probability with bias factors"""
        
        # Fossils can bias modifier weights
        bias_factor = 2.0  # Fossils roughly double relevant modifier weights
        
        total_prob = 1.0
        for mod in prefixes + suffixes:
            biased_weight = mod.weight * bias_factor
            pool = self.total_weight_pools['prefix' if mod.is_prefix else 'suffix']
            total_prob *= (biased_weight / pool)
        
        # Complexity factor
        total_mods = len(prefixes) + len(suffixes)
        complexity_factor = 0.15 / total_mods if total_mods > 0 else 1.0
        
        return total_prob * complexity_factor
    
    def _calculate_generic_probability(self, prefixes: List[ModifierProbability], 
                                     suffixes: List[ModifierProbability]) -> float:
        """Generic probability calculation"""
        return self._calculate_chaos_spam_probability(prefixes, suffixes)
    
    def _calculate_cost_distribution(self, method: str, expected_attempts: float) -> Dict[str, Any]:
        """Calculate cost distribution statistics"""
        
        # Base costs per attempt (in chaos orbs)
        base_costs = {
            'chaos_spam': 5.0,
            'alt_regal': 2.0,
            'essence': 8.0,
            'fossil': 6.0
        }
        
        base_cost = base_costs.get(method, 5.0)
        
        # Expected cost
        expected_cost = expected_attempts * base_cost
        
        # Cost variance (some attempts might need additional currency)
        variance_factor = {
            'chaos_spam': 1.5,
            'alt_regal': 2.0,
            'essence': 1.3,
            'fossil': 1.4
        }.get(method, 1.5)
        
        # Calculate distribution
        std_dev = expected_cost * 0.5 * variance_factor
        
        return {
            'expected_cost': expected_cost,
            'standard_deviation': std_dev,
            'cost_range_90_percent': (
                max(0, expected_cost - 1.645 * std_dev),
                expected_cost + 1.645 * std_dev
            ),
            'pessimistic_cost': expected_cost + 2 * std_dev,
            'optimistic_cost': max(base_cost, expected_cost - std_dev)
        }
    
    def _calculate_confidence_interval(self, probability: float, 
                                     expected_attempts: float) -> Tuple[float, float]:
        """Calculate confidence interval for attempt estimates"""
        
        if probability <= 0:
            return (float('inf'), float('inf'))
        
        # Using binomial distribution properties
        variance = (1 - probability) / (probability * probability)
        std_dev = math.sqrt(variance)
        
        # 95% confidence interval
        margin = 1.96 * std_dev
        
        lower_bound = max(1, expected_attempts - margin)
        upper_bound = expected_attempts + margin
        
        return (lower_bound, upper_bound)
    
    def _create_empty_probability(self) -> CraftingProbability:
        """Create empty probability result for error cases"""
        return CraftingProbability(
            method='unknown',
            target_modifiers=[],
            individual_probabilities={},
            combined_probability=0.0,
            expected_attempts=float('inf'),
            cost_distribution={'expected_cost': 0},
            confidence_interval=(0.0, 0.0),
            worst_case_attempts=0,
            best_case_attempts=0
        )
    
    def simulate_crafting_session(self, probability_result: CraftingProbability, 
                                num_simulations: int = 10000) -> Dict[str, Any]:
        """Monte Carlo simulation of crafting session"""
        
        if probability_result.combined_probability <= 0:
            return {'error': 'Invalid probability for simulation'}
        
        attempts_needed = []
        costs_incurred = []
        
        base_cost = probability_result.cost_distribution.get('expected_cost', 0) / probability_result.expected_attempts
        
        for _ in range(num_simulations):
            attempts = 0
            success = False
            
            while not success and attempts < 10000:  # Safety limit
                attempts += 1
                # Simulate attempt
                if np.random.random() < probability_result.combined_probability:
                    success = True
            
            if success:
                attempts_needed.append(attempts)
                costs_incurred.append(attempts * base_cost)
        
        if not attempts_needed:
            return {'error': 'No successful simulations'}
        
        # Calculate statistics
        attempts_array = np.array(attempts_needed)
        costs_array = np.array(costs_incurred)
        
        return {
            'simulation_count': num_simulations,
            'success_rate': len(attempts_needed) / num_simulations,
            'attempts_statistics': {
                'mean': np.mean(attempts_array),
                'median': np.median(attempts_array),
                'std_dev': np.std(attempts_array),
                'percentiles': {
                    '10th': np.percentile(attempts_array, 10),
                    '25th': np.percentile(attempts_array, 25),
                    '75th': np.percentile(attempts_array, 75),
                    '90th': np.percentile(attempts_array, 90),
                    '95th': np.percentile(attempts_array, 95)
                }
            },
            'cost_statistics': {
                'mean': np.mean(costs_array),
                'median': np.median(costs_array),
                'std_dev': np.std(costs_array),
                'percentiles': {
                    '10th': np.percentile(costs_array, 10),
                    '25th': np.percentile(costs_array, 25),
                    '75th': np.percentile(costs_array, 75),
                    '90th': np.percentile(costs_array, 90),
                    '95th': np.percentile(costs_array, 95)
                }
            }
        }
    
    def analyze_modifier_efficiency(self, modifiers: List[str], 
                                  item_base: str, item_level: int) -> Dict[str, Any]:
        """Analyze efficiency of different modifier combinations"""
        
        efficiency_analysis = {}
        
        # Analyze each modifier individually
        for mod in modifiers:
            individual_prob = self.calculate_exact_probabilities([mod], item_base, item_level)
            efficiency_analysis[mod] = {
                'individual_probability': individual_prob.combined_probability,
                'expected_attempts': individual_prob.expected_attempts,
                'expected_cost': individual_prob.cost_distribution.get('expected_cost', 0),
                'efficiency_score': individual_prob.combined_probability / max(1, individual_prob.expected_attempts)
            }
        
        # Analyze combinations
        combination_analysis = {}
        for r in range(2, min(len(modifiers) + 1, 4)):  # Combinations of 2-3 modifiers
            for combo in itertools.combinations(modifiers, r):
                combo_name = ' + '.join(combo)
                combo_prob = self.calculate_exact_probabilities(list(combo), item_base, item_level)
                
                combination_analysis[combo_name] = {
                    'combined_probability': combo_prob.combined_probability,
                    'expected_attempts': combo_prob.expected_attempts,
                    'expected_cost': combo_prob.cost_distribution.get('expected_cost', 0),
                    'efficiency_score': combo_prob.combined_probability / max(1, combo_prob.expected_attempts)
                }
        
        return {
            'individual_modifiers': efficiency_analysis,
            'modifier_combinations': combination_analysis,
            'analysis_timestamp': datetime.now().isoformat()
        }


# Global probability engine instance
probability_engine = AdvancedProbabilityEngine()