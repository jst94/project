"""
Real-time Strategy Adjustment Based on Market Conditions
Dynamic strategy optimization that adapts to changing market conditions in real-time
"""

import numpy as np
import json
import threading
import time
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import queue


@dataclass
class StrategyAdjustment:
    """Represents a strategy adjustment recommendation"""
    adjustment_type: str  # 'method_change', 'budget_adjust', 'timing_shift', 'modifier_priority'
    current_strategy: Dict[str, Any]
    recommended_strategy: Dict[str, Any]
    reasoning: List[str]
    urgency: str  # 'immediate', 'high', 'medium', 'low'
    confidence: float
    expected_impact: Dict[str, float]
    implementation_steps: List[str]
    timestamp: str


@dataclass
class MarketCondition:
    """Current market condition snapshot"""
    timestamp: str
    volatility_level: float
    trend_direction: str
    liquidity_score: float
    price_momentum: Dict[str, float]
    volume_changes: Dict[str, float]
    external_factors: List[str]
    stability_score: float


@dataclass
class ActiveStrategy:
    """Currently active crafting strategy"""
    strategy_id: str
    user_id: str
    target_modifiers: List[str]
    current_method: str
    allocated_budget: float
    spent_budget: float
    progress_status: str  # 'planning', 'active', 'paused', 'completed', 'abandoned'
    start_time: str
    last_update: str
    market_conditions_at_start: MarketCondition
    adjustments_made: List[StrategyAdjustment]


class RealTimeStrategyOptimizer:
    """Real-time strategy optimization system"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        
        # Active strategies tracking
        self.active_strategies = {}
        self.strategy_queue = queue.Queue()
        self.market_events_queue = queue.Queue()
        
        # Market monitoring
        self.current_market_conditions = None
        self.market_history = deque(maxlen=1000)
        self.volatility_threshold = 0.15
        self.adjustment_cooldown = 300  # 5 minutes between adjustments
        
        # Strategy adjustment triggers
        self.adjustment_triggers = {
            'price_change': 0.10,  # 10% price change
            'volatility_spike': 0.20,  # 20% volatility increase
            'volume_change': 0.25,  # 25% volume change
            'market_sentiment_shift': 0.15  # 15% sentiment change
        }
        
        # Performance tracking
        self.adjustment_effectiveness = defaultdict(list)
        self.strategy_outcomes = defaultdict(list)
        
        # Dependencies
        self.market_intelligence = None
        self.probability_engine = None
        self.recommendation_system = None
        
        # Start monitoring
        self.monitoring_active = True
        self.start_monitoring_threads()
    
    def set_dependencies(self, market_intelligence=None, probability_engine=None, 
                        recommendation_system=None):
        """Set dependencies on other systems"""
        self.market_intelligence = market_intelligence
        self.probability_engine = probability_engine
        self.recommendation_system = recommendation_system
    
    def register_active_strategy(self, strategy: ActiveStrategy) -> str:
        """Register a new active strategy for monitoring"""
        strategy_id = strategy.strategy_id
        self.active_strategies[strategy_id] = strategy
        
        # Initialize monitoring for this strategy
        self._initialize_strategy_monitoring(strategy)
        
        return strategy_id
    
    def _initialize_strategy_monitoring(self, strategy: ActiveStrategy):
        """Initialize monitoring for a specific strategy"""
        # Set up market condition baselines
        if self.market_intelligence:
            current_conditions = self._capture_current_market_conditions()
            strategy.market_conditions_at_start = current_conditions
        
        # Set up performance tracking
        self.strategy_outcomes[strategy.strategy_id] = []
        
        print(f"Initialized monitoring for strategy {strategy.strategy_id}")
    
    def update_strategy_progress(self, strategy_id: str, progress_data: Dict[str, Any]):
        """Update progress for an active strategy"""
        if strategy_id not in self.active_strategies:
            return False
        
        strategy = self.active_strategies[strategy_id]
        
        # Update strategy data
        strategy.spent_budget = progress_data.get('spent_budget', strategy.spent_budget)
        strategy.progress_status = progress_data.get('status', strategy.progress_status)
        strategy.last_update = datetime.now().isoformat()
        
        # Check if adjustment is needed
        self._evaluate_strategy_for_adjustment(strategy_id)
        
        return True
    
    def _evaluate_strategy_for_adjustment(self, strategy_id: str):
        """Evaluate if a strategy needs adjustment"""
        strategy = self.active_strategies[strategy_id]
        
        if strategy.progress_status not in ['planning', 'active']:
            return  # Don't adjust completed/abandoned strategies
        
        # Check cooldown
        if strategy.adjustments_made:
            last_adjustment_time = datetime.fromisoformat(strategy.adjustments_made[-1].timestamp)
            if (datetime.now() - last_adjustment_time).total_seconds() < self.adjustment_cooldown:
                return
        
        # Get current market conditions
        current_conditions = self._capture_current_market_conditions()
        if not current_conditions:
            return
        
        # Analyze market changes since strategy start
        market_changes = self._analyze_market_changes(
            strategy.market_conditions_at_start, current_conditions
        )
        
        # Generate adjustments based on changes
        adjustments = self._generate_strategy_adjustments(strategy, market_changes, current_conditions)
        
        # Apply high-priority adjustments
        for adjustment in adjustments:
            if adjustment.urgency in ['immediate', 'high']:
                self._apply_strategy_adjustment(strategy_id, adjustment)
    
    def _capture_current_market_conditions(self) -> Optional[MarketCondition]:
        """Capture current market conditions"""
        if not self.market_intelligence:
            return None
        
        try:
            # Get market forecast and trends
            forecast = self.market_intelligence.generate_market_forecast('1h')
            
            # Calculate volatility from recent price changes
            volatility_scores = []
            price_momentum = {}
            volume_changes = {}
            
            for currency in ['Chaos Orb', 'Divine Orb', 'Exalted Orb']:
                if currency in self.market_intelligence.trend_cache:
                    trend = self.market_intelligence.trend_cache[currency]
                    volatility_scores.append(trend.volatility_score)
                    price_momentum[currency] = trend.price_change_24h
                    volume_changes[currency] = 0.0  # Simplified
            
            avg_volatility = np.mean(volatility_scores) if volatility_scores else 0.1
            
            # Calculate stability score
            stability_score = 1.0 - min(1.0, avg_volatility * 2)
            
            # External factors (simplified)
            external_factors = []
            if avg_volatility > 0.2:
                external_factors.append("high_market_volatility")
            if forecast.market_conditions == 'uncertain':
                external_factors.append("market_uncertainty")
            
            condition = MarketCondition(
                timestamp=datetime.now().isoformat(),
                volatility_level=avg_volatility,
                trend_direction=forecast.market_conditions,
                liquidity_score=0.8,  # Simplified
                price_momentum=price_momentum,
                volume_changes=volume_changes,
                external_factors=external_factors,
                stability_score=stability_score
            )
            
            self.current_market_conditions = condition
            self.market_history.append(condition)
            
            return condition
            
        except Exception as e:
            print(f"Error capturing market conditions: {e}")
            return None
    
    def _analyze_market_changes(self, start_conditions: MarketCondition, 
                              current_conditions: MarketCondition) -> Dict[str, Any]:
        """Analyze changes in market conditions"""
        changes = {
            'volatility_change': current_conditions.volatility_level - start_conditions.volatility_level,
            'trend_shift': start_conditions.trend_direction != current_conditions.trend_direction,
            'stability_change': current_conditions.stability_score - start_conditions.stability_score,
            'significant_changes': [],
            'risk_factors': [],
            'opportunities': []
        }
        
        # Check for significant volatility changes
        volatility_change_pct = abs(changes['volatility_change']) / max(start_conditions.volatility_level, 0.01)
        if volatility_change_pct > self.adjustment_triggers['volatility_spike']:
            changes['significant_changes'].append('volatility_spike')
            if changes['volatility_change'] > 0:
                changes['risk_factors'].append('increased_volatility')
            else:
                changes['opportunities'].append('decreased_volatility')
        
        # Check for price momentum changes
        for currency, current_momentum in current_conditions.price_momentum.items():
            start_momentum = start_conditions.price_momentum.get(currency, 0)
            momentum_change = abs(current_momentum - start_momentum)
            
            if momentum_change > self.adjustment_triggers['price_change'] * 100:  # Convert to percentage
                changes['significant_changes'].append(f'{currency}_price_change')
                if current_momentum > start_momentum:
                    changes['risk_factors'].append(f'{currency}_price_increase')
                else:
                    changes['opportunities'].append(f'{currency}_price_decrease')
        
        # Check for trend direction changes
        if changes['trend_shift']:
            changes['significant_changes'].append('market_trend_shift')
            if current_conditions.trend_direction in ['bearish', 'uncertain']:
                changes['risk_factors'].append('negative_market_sentiment')
            else:
                changes['opportunities'].append('positive_market_sentiment')
        
        return changes
    
    def _generate_strategy_adjustments(self, strategy: ActiveStrategy, 
                                     market_changes: Dict[str, Any], 
                                     current_conditions: MarketCondition) -> List[StrategyAdjustment]:
        """Generate strategy adjustments based on market changes"""
        adjustments = []
        
        # Budget adjustments for price changes
        if 'increased_volatility' in market_changes['risk_factors']:
            adjustment = self._create_budget_adjustment(
                strategy, current_conditions, 
                "Increase budget due to market volatility",
                1.15,  # 15% increase
                'high'
            )
            adjustments.append(adjustment)
        
        # Method adjustments for market conditions
        if current_conditions.volatility_level > 0.25:  # High volatility
            if strategy.current_method == 'chaos_spam':
                adjustment = self._create_method_adjustment(
                    strategy, current_conditions,
                    "Switch to essence crafting for more predictable costs",
                    'essence',
                    'medium'
                )
                adjustments.append(adjustment)
        
        # Timing adjustments
        if 'negative_market_sentiment' in market_changes['risk_factors']:
            adjustment = self._create_timing_adjustment(
                strategy, current_conditions,
                "Consider pausing due to unfavorable market conditions",
                'pause',
                'medium'
            )
            adjustments.append(adjustment)
        elif 'positive_market_sentiment' in market_changes['opportunities']:
            adjustment = self._create_timing_adjustment(
                strategy, current_conditions,
                "Favorable conditions - consider accelerating",
                'accelerate',
                'low'
            )
            adjustments.append(adjustment)
        
        # Modifier priority adjustments
        expensive_currencies = []
        for currency, momentum in current_conditions.price_momentum.items():
            if momentum > 10:  # 10% price increase
                expensive_currencies.append(currency)
        
        if expensive_currencies:
            adjustment = self._create_modifier_priority_adjustment(
                strategy, current_conditions,
                f"Reprioritize modifiers due to {', '.join(expensive_currencies)} price increases",
                expensive_currencies,
                'medium'
            )
            adjustments.append(adjustment)
        
        return adjustments
    
    def _create_budget_adjustment(self, strategy: ActiveStrategy, conditions: MarketCondition,
                                reason: str, multiplier: float, urgency: str) -> StrategyAdjustment:
        """Create budget adjustment recommendation"""
        new_budget = strategy.allocated_budget * multiplier
        budget_increase = new_budget - strategy.allocated_budget
        
        return StrategyAdjustment(
            adjustment_type='budget_adjust',
            current_strategy={
                'allocated_budget': strategy.allocated_budget,
                'spent_budget': strategy.spent_budget
            },
            recommended_strategy={
                'allocated_budget': new_budget,
                'budget_increase': budget_increase
            },
            reasoning=[
                reason,
                f"Market volatility: {conditions.volatility_level:.2f}",
                f"Stability score: {conditions.stability_score:.2f}"
            ],
            urgency=urgency,
            confidence=0.8,
            expected_impact={
                'risk_reduction': 0.3,
                'success_probability_increase': 0.1,
                'cost_certainty': 0.4
            },
            implementation_steps=[
                f"Increase budget allocation by {budget_increase:.0f} chaos orbs",
                "Secure additional currency before prices rise further",
                "Adjust crafting timeline if needed"
            ],
            timestamp=datetime.now().isoformat()
        )
    
    def _create_method_adjustment(self, strategy: ActiveStrategy, conditions: MarketCondition,
                                reason: str, new_method: str, urgency: str) -> StrategyAdjustment:
        """Create method change recommendation"""
        return StrategyAdjustment(
            adjustment_type='method_change',
            current_strategy={
                'method': strategy.current_method
            },
            recommended_strategy={
                'method': new_method
            },
            reasoning=[
                reason,
                f"Current volatility: {conditions.volatility_level:.2f}",
                f"Market trend: {conditions.trend_direction}"
            ],
            urgency=urgency,
            confidence=0.7,
            expected_impact={
                'cost_predictability': 0.3,
                'risk_reduction': 0.2,
                'time_efficiency': -0.1  # Might take longer but more reliable
            },
            implementation_steps=[
                f"Switch from {strategy.current_method} to {new_method}",
                "Acquire necessary materials for new method",
                "Recalculate success probabilities"
            ],
            timestamp=datetime.now().isoformat()
        )
    
    def _create_timing_adjustment(self, strategy: ActiveStrategy, conditions: MarketCondition,
                                reason: str, timing_action: str, urgency: str) -> StrategyAdjustment:
        """Create timing adjustment recommendation"""
        return StrategyAdjustment(
            adjustment_type='timing_shift',
            current_strategy={
                'status': strategy.progress_status,
                'timing': 'proceeding'
            },
            recommended_strategy={
                'timing_action': timing_action
            },
            reasoning=[
                reason,
                f"Market stability: {conditions.stability_score:.2f}",
                f"External factors: {len(conditions.external_factors)}"
            ],
            urgency=urgency,
            confidence=0.6,
            expected_impact={
                'timing_advantage': 0.3 if timing_action == 'accelerate' else -0.2,
                'cost_optimization': 0.2 if timing_action == 'pause' else 0.0
            },
            implementation_steps=self._get_timing_steps(timing_action),
            timestamp=datetime.now().isoformat()
        )
    
    def _create_modifier_priority_adjustment(self, strategy: ActiveStrategy, conditions: MarketCondition,
                                          reason: str, expensive_currencies: List[str], 
                                          urgency: str) -> StrategyAdjustment:
        """Create modifier priority adjustment recommendation"""
        return StrategyAdjustment(
            adjustment_type='modifier_priority',
            current_strategy={
                'modifiers': strategy.target_modifiers,
                'priority': 'original_order'
            },
            recommended_strategy={
                'priority_adjustment': 'deprioritize_expensive',
                'affected_currencies': expensive_currencies
            },
            reasoning=[
                reason,
                f"Price momentum affecting: {', '.join(expensive_currencies)}",
                "Focus on cost-effective modifiers first"
            ],
            urgency=urgency,
            confidence=0.7,
            expected_impact={
                'immediate_cost_reduction': 0.15,
                'overall_cost_efficiency': 0.2
            },
            implementation_steps=[
                "Identify modifiers requiring expensive currencies",
                "Prioritize modifiers with stable currency requirements",
                "Consider delaying expensive modifiers until prices stabilize"
            ],
            timestamp=datetime.now().isoformat()
        )
    
    def _get_timing_steps(self, timing_action: str) -> List[str]:
        """Get implementation steps for timing adjustments"""
        steps = {
            'pause': [
                "Temporarily halt active crafting",
                "Monitor market conditions for improvement",
                "Set alerts for favorable condition changes",
                "Prepare to resume when conditions improve"
            ],
            'accelerate': [
                "Increase crafting session frequency",
                "Secure necessary currencies quickly",
                "Take advantage of current favorable conditions",
                "Monitor for condition changes"
            ],
            'delay': [
                "Postpone crafting start",
                "Continue market monitoring",
                "Prepare materials for optimal timing",
                "Set target conditions for execution"
            ]
        }
        return steps.get(timing_action, ["Implement timing adjustment", "Monitor results"])
    
    def _apply_strategy_adjustment(self, strategy_id: str, adjustment: StrategyAdjustment):
        """Apply a strategy adjustment"""
        if strategy_id not in self.active_strategies:
            return False
        
        strategy = self.active_strategies[strategy_id]
        
        # Add adjustment to strategy history
        strategy.adjustments_made.append(adjustment)
        
        # Apply the adjustment based on type
        if adjustment.adjustment_type == 'budget_adjust':
            new_budget = adjustment.recommended_strategy['allocated_budget']
            strategy.allocated_budget = new_budget
        
        elif adjustment.adjustment_type == 'method_change':
            new_method = adjustment.recommended_strategy['method']
            strategy.current_method = new_method
        
        elif adjustment.adjustment_type == 'timing_shift':
            timing_action = adjustment.recommended_strategy['timing_action']
            if timing_action == 'pause':
                strategy.progress_status = 'paused'
            elif timing_action == 'accelerate':
                # This would trigger more aggressive crafting
                pass
        
        # Update strategy timestamp
        strategy.last_update = datetime.now().isoformat()
        
        # Track adjustment effectiveness (placeholder)
        self.adjustment_effectiveness[adjustment.adjustment_type].append({
            'timestamp': adjustment.timestamp,
            'confidence': adjustment.confidence,
            'urgency': adjustment.urgency
        })
        
        print(f"Applied {adjustment.adjustment_type} adjustment to strategy {strategy_id}")
        return True
    
    def get_strategy_status(self, strategy_id: str) -> Dict[str, Any]:
        """Get current status of a strategy"""
        if strategy_id not in self.active_strategies:
            return {'error': 'Strategy not found'}
        
        strategy = self.active_strategies[strategy_id]
        
        return {
            'strategy_id': strategy_id,
            'progress_status': strategy.progress_status,
            'current_method': strategy.current_method,
            'budget_utilization': strategy.spent_budget / strategy.allocated_budget if strategy.allocated_budget > 0 else 0,
            'adjustments_count': len(strategy.adjustments_made),
            'last_adjustment': strategy.adjustments_made[-1].timestamp if strategy.adjustments_made else None,
            'market_stability': self.current_market_conditions.stability_score if self.current_market_conditions else 0.5,
            'recommendation': self._get_current_recommendation(strategy)
        }
    
    def _get_current_recommendation(self, strategy: ActiveStrategy) -> str:
        """Get current recommendation for a strategy"""
        if not self.current_market_conditions:
            return "Monitor market conditions"
        
        conditions = self.current_market_conditions
        
        if conditions.volatility_level > 0.3:
            return "High volatility - consider pausing or switching to safer methods"
        elif conditions.stability_score > 0.8:
            return "Stable conditions - proceed with confidence"
        elif strategy.spent_budget / strategy.allocated_budget > 0.8:
            return "Budget mostly spent - consider final push or cost review"
        else:
            return "Continue with current strategy"
    
    def start_monitoring_threads(self):
        """Start background monitoring threads"""
        
        def market_monitor():
            """Monitor market conditions continuously"""
            while self.monitoring_active:
                try:
                    self._capture_current_market_conditions()
                    time.sleep(60)  # Update every minute
                except Exception as e:
                    print(f"Market monitoring error: {e}")
                    time.sleep(30)
        
        def strategy_evaluator():
            """Evaluate strategies periodically"""
            while self.monitoring_active:
                try:
                    for strategy_id in list(self.active_strategies.keys()):
                        self._evaluate_strategy_for_adjustment(strategy_id)
                    time.sleep(300)  # Evaluate every 5 minutes
                except Exception as e:
                    print(f"Strategy evaluation error: {e}")
                    time.sleep(60)
        
        # Start threads
        market_thread = threading.Thread(target=market_monitor, daemon=True)
        strategy_thread = threading.Thread(target=strategy_evaluator, daemon=True)
        
        market_thread.start()
        strategy_thread.start()
        
        print("Real-time monitoring threads started")
    
    def stop_monitoring(self):
        """Stop all monitoring activities"""
        self.monitoring_active = False
        print("Real-time monitoring stopped")
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get system performance statistics"""
        return {
            'active_strategies': len(self.active_strategies),
            'total_adjustments': sum(len(s.adjustments_made) for s in self.active_strategies.values()),
            'market_data_points': len(self.market_history),
            'current_market_stability': self.current_market_conditions.stability_score if self.current_market_conditions else 0,
            'adjustment_effectiveness': {
                adj_type: {
                    'count': len(records),
                    'avg_confidence': np.mean([r['confidence'] for r in records]) if records else 0
                } for adj_type, records in self.adjustment_effectiveness.items()
            },
            'monitoring_status': 'active' if self.monitoring_active else 'stopped'
        }
    
    def export_strategy_data(self, file_path: str):
        """Export strategy and adjustment data"""
        export_data = {
            'active_strategies': {sid: asdict(strategy) for sid, strategy in self.active_strategies.items()},
            'market_history': [asdict(condition) for condition in list(self.market_history)[-100:]],
            'adjustment_effectiveness': dict(self.adjustment_effectiveness),
            'system_stats': self.get_system_statistics(),
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)


# Global real-time strategy optimizer instance
realtime_optimizer = RealTimeStrategyOptimizer()