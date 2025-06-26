"""
AI-Based Crafting Strategy Optimizer
Advanced intelligence system for optimal crafting strategies using machine learning principles
"""

import numpy as np
import json
import math
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class CraftingScenario:
    """Data structure for crafting scenarios"""
    target_modifiers: List[str]
    item_base: str
    item_level: int
    budget: float
    league_meta: Dict[str, Any]
    user_preferences: Dict[str, Any]


@dataclass
class StrategyScore:
    """Scoring system for crafting strategies"""
    method: str
    success_probability: float
    expected_cost: float
    time_efficiency: float
    risk_factor: float
    overall_score: float
    confidence: float


class IntelligentCraftingAI:
    """AI-powered crafting strategy optimizer"""
    
    def __init__(self):
        self.strategy_weights = {
            'success_probability': 0.35,
            'cost_efficiency': 0.25,
            'time_efficiency': 0.15,
            'risk_tolerance': 0.15,
            'user_preference': 0.10
        }
        
        # Advanced modifier database with probability calculations
        self.modifier_complexity = {
            'Maximum Life': {'complexity': 0.3, 'weight_class': 'medium', 'meta_popularity': 0.9},
            'Maximum Energy Shield': {'complexity': 0.35, 'weight_class': 'medium', 'meta_popularity': 0.7},
            'Attack Speed': {'complexity': 0.4, 'weight_class': 'low', 'meta_popularity': 0.8},
            'Critical Strike Chance': {'complexity': 0.45, 'weight_class': 'low', 'meta_popularity': 0.6},
            'Elemental Damage': {'complexity': 0.5, 'weight_class': 'variable', 'meta_popularity': 0.7},
            'Movement Speed': {'complexity': 0.6, 'weight_class': 'very_low', 'meta_popularity': 0.9}
        }
        
        # Method efficiency profiles
        self.method_profiles = {
            'chaos_spam': {
                'base_success': 0.15,
                'cost_variance': 0.8,
                'time_factor': 0.9,
                'risk_level': 0.7,
                'modifier_scaling': lambda x: max(0.05, 0.15 - (x * 0.02))
            },
            'alt_regal': {
                'base_success': 0.65,
                'cost_variance': 0.4,
                'time_factor': 0.6,
                'risk_level': 0.3,
                'modifier_scaling': lambda x: max(0.3, 0.65 - (x * 0.15))
            },
            'essence': {
                'base_success': 0.8,
                'cost_variance': 0.3,
                'time_factor': 0.7,
                'risk_level': 0.2,
                'modifier_scaling': lambda x: max(0.6, 0.8 - (x * 0.05))
            },
            'fossil': {
                'base_success': 0.55,
                'cost_variance': 0.5,
                'time_factor': 0.8,
                'risk_level': 0.4,
                'modifier_scaling': lambda x: max(0.25, 0.55 - (x * 0.08))
            },
            'flask': {
                'base_success': 0.75,
                'cost_variance': 0.25,
                'time_factor': 0.5,
                'risk_level': 0.15,
                'modifier_scaling': lambda x: max(0.6, 0.75 - (x * 0.1))  # Flask crafting is easier
            }
        }
        
        # Learning data storage
        self.user_success_patterns = defaultdict(list)
        self.market_adaptation_factors = {}
        
    def analyze_crafting_scenario(self, scenario: CraftingScenario) -> List[StrategyScore]:
        """Analyze a crafting scenario and return ranked strategies"""
        strategies = []
        
        for method, profile in self.method_profiles.items():
            score = self._evaluate_strategy(method, profile, scenario)
            strategies.append(score)
        
        # Sort by overall score (descending)
        strategies.sort(key=lambda x: x.overall_score, reverse=True)
        
        return strategies
    
    def _evaluate_strategy(self, method: str, profile: Dict, scenario: CraftingScenario) -> StrategyScore:
        """Evaluate a specific crafting strategy"""
        
        # Calculate modifier complexity
        total_complexity = sum(
            self.modifier_complexity.get(mod, {'complexity': 0.5})['complexity']
            for mod in scenario.target_modifiers
        )
        
        mod_count = len(scenario.target_modifiers)
        
        # Base success probability with complexity scaling
        base_success = profile['modifier_scaling'](mod_count)
        complexity_penalty = min(0.3, total_complexity * 0.1)
        success_probability = max(0.01, base_success - complexity_penalty)
        
        # Item level factor
        ilvl_factor = min(1.0, scenario.item_level / 85.0)
        success_probability *= ilvl_factor
        
        # Expected cost calculation
        expected_attempts = 1.0 / success_probability
        base_cost_per_attempt = self._calculate_base_cost(method, scenario)
        expected_cost = expected_attempts * base_cost_per_attempt
        
        # Time efficiency (attempts needed vs time per attempt)
        time_efficiency = 1.0 / (expected_attempts * profile['time_factor'])
        
        # Risk factor (cost variance and success uncertainty)
        risk_factor = profile['risk_level'] * (1 + profile['cost_variance'])
        
        # Budget feasibility
        budget_ratio = scenario.budget / expected_cost if expected_cost > 0 else 0
        budget_factor = min(1.0, budget_ratio)
        
        # User preference factor
        user_pref_factor = scenario.user_preferences.get('method_preferences', {}).get(method, 0.5)
        
        # Meta game factor
        meta_factor = self._calculate_meta_factor(scenario.target_modifiers, scenario.league_meta)
        
        # Calculate overall score
        score_components = {
            'success': success_probability * self.strategy_weights['success_probability'],
            'cost': (1.0 / (expected_cost / scenario.budget)) * self.strategy_weights['cost_efficiency'] * budget_factor,
            'time': time_efficiency * self.strategy_weights['time_efficiency'],
            'risk': (1 - risk_factor) * self.strategy_weights['risk_tolerance'],
            'preference': user_pref_factor * self.strategy_weights['user_preference']
        }
        
        overall_score = sum(score_components.values()) * meta_factor
        
        # Confidence calculation based on data quality and scenario complexity
        confidence = self._calculate_confidence(scenario, method)
        
        return StrategyScore(
            method=method,
            success_probability=success_probability,
            expected_cost=expected_cost,
            time_efficiency=time_efficiency,
            risk_factor=risk_factor,
            overall_score=overall_score,
            confidence=confidence
        )
    
    def _calculate_base_cost(self, method: str, scenario: CraftingScenario) -> float:
        """Calculate base cost per attempt for a method"""
        # Simplified cost calculation - in practice, this would use real market data
        base_costs = {
            'chaos_spam': 50,
            'alt_regal': 25,
            'essence': 75,
            'fossil': 60,
            'flask': 15  # Flask crafting is much cheaper
        }
        
        modifier_cost_multiplier = 1 + (len(scenario.target_modifiers) * 0.2)
        return base_costs.get(method, 50) * modifier_cost_multiplier
    
    def _calculate_meta_factor(self, modifiers: List[str], league_meta: Dict) -> float:
        """Calculate meta game relevance factor"""
        if not league_meta:
            return 1.0
        
        meta_score = 0.0
        for mod in modifiers:
            mod_data = self.modifier_complexity.get(mod, {})
            meta_popularity = mod_data.get('meta_popularity', 0.5)
            meta_score += meta_popularity
        
        return min(1.2, max(0.8, meta_score / len(modifiers))) if modifiers else 1.0
    
    def _calculate_confidence(self, scenario: CraftingScenario, method: str) -> float:
        """Calculate confidence in the strategy recommendation"""
        base_confidence = 0.7
        
        # Reduce confidence for complex scenarios
        complexity_penalty = len(scenario.target_modifiers) * 0.05
        
        # Increase confidence for well-known methods
        method_confidence_bonus = {
            'chaos_spam': 0.1,
            'alt_regal': 0.15,
            'essence': 0.2,
            'fossil': 0.05
        }.get(method, 0.0)
        
        # Historical data availability (simulated)
        data_availability = 0.1  # Would be based on actual usage data
        
        confidence = base_confidence + method_confidence_bonus + data_availability - complexity_penalty
        return max(0.1, min(0.95, confidence))
    
    def optimize_budget_allocation(self, scenario: CraftingScenario, 
                                 strategies: List[StrategyScore]) -> Dict:
        """Optimize budget allocation across different strategies"""
        if not strategies:
            return {}
        
        best_strategy = strategies[0]
        budget = scenario.budget
        
        # Calculate optimal allocation
        primary_allocation = min(budget * 0.7, best_strategy.expected_cost * 1.5)
        backup_allocation = budget * 0.2
        emergency_allocation = budget * 0.1
        
        allocation = {
            'primary_method': {
                'method': best_strategy.method,
                'allocated_budget': primary_allocation,
                'expected_attempts': int(primary_allocation / (best_strategy.expected_cost / (1/best_strategy.success_probability))),
                'success_probability': best_strategy.success_probability
            },
            'backup_method': {
                'method': strategies[1].method if len(strategies) > 1 else 'chaos_spam',
                'allocated_budget': backup_allocation,
                'rationale': 'Fallback option if primary method fails'
            },
            'emergency_reserve': {
                'amount': emergency_allocation,
                'purpose': 'Unexpected costs and market fluctuations'
            },
            'total_allocated': primary_allocation + backup_allocation + emergency_allocation,
            'optimization_timestamp': datetime.now().isoformat()
        }
        
        return allocation
    
    def generate_adaptive_plan(self, scenario: CraftingScenario) -> Dict:
        """Generate an adaptive crafting plan with multiple contingencies"""
        strategies = self.analyze_crafting_scenario(scenario)
        budget_allocation = self.optimize_budget_allocation(scenario, strategies)
        
        # Generate step-by-step adaptive plan
        plan_steps = []
        
        primary_strategy = strategies[0]
        
        # Phase 1: Preparation  
        prep_budget = budget_allocation['primary_method']['allocated_budget']
        plan_steps.append({
            'phase': 'preparation',
            'description': f'Prepare for {primary_strategy.method} crafting',
            'actions': [
                f'OPEN PATH OF EXILE and navigate to your stash',
                f'GO TO TRADE WEBSITE and search for {scenario.item_base} with ilvl {scenario.item_level}+',
                f'BUY base item for approximately {int(prep_budget * 0.05)}c',
                f'PURCHASE all required currency (budget: {int(prep_budget)}c total)',
                'SET UP loot filter to highlight items with your target modifiers',
                'CLEAR inventory space for crafting materials and results'
            ],
            'estimated_time': '5-10 minutes',
            'budget_required': prep_budget * 0.1
        })
        
        # Phase 2: Primary execution
        plan_steps.append({
            'phase': 'primary_execution',
            'description': f'Execute {primary_strategy.method} strategy',
            'actions': self._generate_method_actions(primary_strategy.method, scenario),
            'success_probability': primary_strategy.success_probability,
            'max_attempts': budget_allocation['primary_method']['expected_attempts'],
            'budget_required': budget_allocation['primary_method']['allocated_budget']
        })
        
        # Phase 3: Contingency
        if len(strategies) > 1:
            backup_strategy = strategies[1]
            plan_steps.append({
                'phase': 'contingency',
                'description': f'Fallback to {backup_strategy.method} if primary fails',
                'trigger': 'Primary method exhausted or budget threshold reached',
                'actions': self._generate_method_actions(backup_strategy.method, scenario),
                'budget_required': budget_allocation['backup_method']['allocated_budget']
            })
        
        # Phase 4: Optimization
        plan_steps.append({
            'phase': 'optimization',
            'description': 'Final optimization and value perfection',
            'actions': [
                'Use Divine Orbs for value optimization',
                'Consider hybrid approaches for remaining modifiers',
                'Evaluate success against initial goals'
            ],
            'budget_required': budget_allocation['emergency_reserve']['amount']
        })
        
        return {
            'scenario_analysis': {
                'complexity_score': sum(self.modifier_complexity.get(mod, {'complexity': 0.5})['complexity'] 
                                      for mod in scenario.target_modifiers),
                'recommended_strategy': primary_strategy.method,
                'confidence_level': primary_strategy.confidence
            },
            'strategy_rankings': [
                {
                    'method': s.method,
                    'score': s.overall_score,
                    'success_rate': s.success_probability,
                    'expected_cost': s.expected_cost
                } for s in strategies
            ],
            'budget_allocation': budget_allocation,
            'adaptive_plan': plan_steps,
            'risk_assessment': {
                'primary_risk': primary_strategy.risk_factor,
                'mitigation_strategies': self._generate_risk_mitigations(scenario, strategies),
                'market_volatility_factor': 0.15  # Would be calculated from real market data
            },
            'generated_at': datetime.now().isoformat(),
            'ai_version': '1.0.0'
        }
    
    def _generate_method_actions(self, method: str, scenario: CraftingScenario) -> List[str]:
        """Generate specific actions for a crafting method"""
        # Calculate specific quantities based on budget
        budget = scenario.budget
        chaos_needed = max(50, int(budget * 0.8))
        divine_needed = max(3, int(budget * 0.05))
        
        actions = {
            'chaos_spam': [
                f'BUY exactly {chaos_needed} Chaos Orbs and {divine_needed} Divine Orbs from trade',
                f'ACQUIRE {scenario.item_base} base with item level {scenario.item_level}+ (must be RARE/yellow)',
                'RIGHT-CLICK Chaos Orb → LEFT-CLICK your item → CHECK modifiers',
                f'REPEAT previous step until you see: {", ".join(scenario.target_modifiers[:3])}',
                f'STOP when you get target mods OR used {int(chaos_needed * 0.9)} Chaos Orbs',
                'Use Divine Orbs to perfect numeric values of good modifiers'
            ],
            'alt_regal': [
                f'BUY {max(100, int(budget * 0.4))} Alteration Orbs, {max(20, int(budget * 0.1))} Augmentation Orbs, 5 Regal Orbs',
                f'ACQUIRE WHITE (normal) {scenario.item_base} with item level {scenario.item_level}+',
                'RIGHT-CLICK Orb of Transmutation → LEFT-CLICK item (makes it BLUE/magic)',
                f'SPAM Alteration Orbs until you get ONE of: {", ".join(scenario.target_modifiers[:2])}',
                'IF item has only 1 mod: RIGHT-CLICK Augmentation Orb → LEFT-CLICK item',
                'RIGHT-CLICK Regal Orb → LEFT-CLICK item (makes it YELLOW/rare)',
                'Use Exalted Orbs to add remaining target modifiers one by one'
            ],
            'essence': [
                'IDENTIFY which essence guarantees your most important modifier',
                f'BUY 10-20 of that essence type (budget: {int(budget * 0.6)}c)',
                f'ACQUIRE WHITE {scenario.item_base} with item level {scenario.item_level}+',
                'RIGHT-CLICK essence → LEFT-CLICK item (makes it RARE with guaranteed mod)',
                'CHECK if you got additional target modifiers from the essence',
                'Use Chaos Orbs or Exalted Orbs to complete remaining modifiers'
            ],
            'fossil': [
                'RESEARCH which fossils boost your target modifier types',
                f'BUY appropriate fossils and resonators (budget: {int(budget * 0.7)}c)',
                f'ACQUIRE {scenario.item_base} base with item level {scenario.item_level}+',
                'PUT fossils in resonator → RIGHT-CLICK resonator → LEFT-CLICK item',
                'CHECK results and repeat until you get target modifiers',
                'Use Divine Orbs to perfect values once you have good base'
            ],
            'flask': [
                f'BUY {max(50, int(budget * 0.4))} Alteration Orbs and {max(5, int(budget * 0.1))} Augmentation Orbs',
                f'BUY 5 Glassblower\'s Baubles for quality',
                f'ACQUIRE WHITE (normal) {scenario.item_base} flask',
                'RIGHT-CLICK Glassblower\'s Bauble → LEFT-CLICK flask (repeat until 20% quality)',
                'RIGHT-CLICK Orb of Transmutation → LEFT-CLICK flask (makes it BLUE/magic)',
                f'SPAM Alteration Orbs until you get ONE of: {", ".join(scenario.target_modifiers[:2])}',
                'IF flask has only 1 mod: RIGHT-CLICK Augmentation Orb → LEFT-CLICK flask',
                'REPEAT until you get both desired flask modifiers'
            ]
        }
        
        return actions.get(method, ['Execute crafting method', 'Monitor progress', 'Adjust as needed'])
    
    def _generate_risk_mitigations(self, scenario: CraftingScenario, 
                                 strategies: List[StrategyScore]) -> List[str]:
        """Generate risk mitigation strategies"""
        mitigations = []
        
        if scenario.budget < strategies[0].expected_cost * 1.5:
            mitigations.append('Budget is tight - consider spreading attempts over time to monitor market changes')
        
        if len(scenario.target_modifiers) >= 4:
            mitigations.append('High modifier count - prioritize most important modifiers first')
        
        complex_mods = [mod for mod in scenario.target_modifiers 
                       if self.modifier_complexity.get(mod, {'complexity': 0.5})['complexity'] > 0.4]
        if complex_mods:
            mitigations.append(f'Complex modifiers detected ({len(complex_mods)}) - consider essence crafting for guarantees')
        
        mitigations.append('Keep emergency budget for market price fluctuations')
        mitigations.append('Monitor success rate and switch methods if significantly underperforming')
        
        return mitigations
    
    def learn_from_session(self, scenario: CraftingScenario, actual_result: Dict):
        """Learn from crafting session results to improve future predictions"""
        method_used = actual_result.get('method_used')
        success = actual_result.get('success', False)
        actual_cost = actual_result.get('actual_cost', 0)
        attempts = actual_result.get('attempts', 1)
        
        if method_used and method_used in self.method_profiles:
            # Update success patterns
            session_data = {
                'scenario': scenario,
                'success': success,
                'cost': actual_cost,
                'attempts': attempts,
                'timestamp': datetime.now().isoformat()
            }
            
            self.user_success_patterns[method_used].append(session_data)
            
            # Adaptive learning - adjust method profiles based on outcomes
            if len(self.user_success_patterns[method_used]) >= 5:
                self._update_method_profile(method_used)
    
    def _update_method_profile(self, method: str):
        """Update method profile based on historical success data"""
        sessions = self.user_success_patterns[method][-10:]  # Last 10 sessions
        
        if len(sessions) < 3:
            return
        
        success_rate = sum(1 for s in sessions if s['success']) / len(sessions)
        avg_cost_ratio = np.mean([s['cost'] / s['scenario'].budget for s in sessions])
        
        # Gradually adjust base success rate
        current_base = self.method_profiles[method]['base_success']
        adjustment = (success_rate - current_base) * 0.1  # 10% adjustment
        
        self.method_profiles[method]['base_success'] = max(0.01, min(0.95, current_base + adjustment))
        
        print(f"Updated {method} profile: base_success = {self.method_profiles[method]['base_success']:.3f}")


# Global AI optimizer instance
ai_optimizer = IntelligentCraftingAI()