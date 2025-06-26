"""
Intelligent Recommendation System Based on User History and Meta Trends
Advanced recommendation engine that learns from user behavior and meta game analysis
"""

import numpy as np
import json
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import sqlite3
import os


@dataclass
class RecommendationContext:
    """Context for generating recommendations"""
    user_id: str
    current_modifiers: List[str]
    item_base: str
    item_level: int
    budget: float
    league: str
    build_goal: Optional[str] = None
    risk_tolerance: float = 0.5
    time_preference: str = "balanced"  # "fast", "balanced", "optimal"


@dataclass
class Recommendation:
    """Single recommendation with detailed reasoning"""
    type: str  # "modifier", "method", "budget", "timing", "alternative"
    title: str
    description: str
    confidence: float
    priority: str  # "high", "medium", "low"
    reasoning: List[str]
    data: Dict[str, Any]
    expected_outcome: Dict[str, Any]
    implementation_steps: List[str]


@dataclass
class RecommendationSet:
    """Complete set of recommendations for a scenario"""
    context: RecommendationContext
    recommendations: List[Recommendation]
    meta_insights: Dict[str, Any]
    user_insights: Dict[str, Any]
    market_timing: Dict[str, Any]
    overall_strategy: str
    confidence_score: float
    generated_at: str


class IntelligentRecommendationSystem:
    """Advanced recommendation engine with user learning and meta analysis"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.recommendations_db_path = os.path.join(data_dir, "recommendations.db")
        
        # Recommendation components
        self.user_profiles = {}
        self.meta_trends = {}
        self.recommendation_history = defaultdict(list)
        self.success_tracking = defaultdict(list)
        
        # Recommendation weights
        self.weight_factors = {
            'user_history': 0.25,
            'meta_trends': 0.20,
            'market_conditions': 0.15,
            'build_synergy': 0.15,
            'success_probability': 0.15,
            'cost_efficiency': 0.10
        }
        
        # Success tracking
        self.recommendation_outcomes = defaultdict(lambda: {'accepted': 0, 'rejected': 0, 'success': 0, 'failure': 0})
        
        # Initialize systems
        self.init_recommendations_database()
        self.load_recommendation_data()
        
        # Import other systems
        self.learning_system = None
        self.market_intelligence = None
        self.modifier_database = None
        self.probability_engine = None
    
    def set_dependencies(self, learning_system=None, market_intelligence=None, 
                        modifier_database=None, probability_engine=None):
        """Set dependencies on other systems"""
        self.learning_system = learning_system
        self.market_intelligence = market_intelligence
        self.modifier_database = modifier_database
        self.probability_engine = probability_engine
    
    def init_recommendations_database(self):
        """Initialize recommendations database"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        with sqlite3.connect(self.recommendations_db_path) as conn:
            cursor = conn.cursor()
            
            # User profiles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id TEXT PRIMARY KEY,
                    preferences TEXT NOT NULL,
                    success_patterns TEXT NOT NULL,
                    recommendation_history TEXT NOT NULL,
                    learning_score REAL NOT NULL,
                    last_updated TEXT NOT NULL
                )
            ''')
            
            # Recommendation history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recommendation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    recommendation_type TEXT NOT NULL,
                    recommendation_data TEXT NOT NULL,
                    context TEXT NOT NULL,
                    user_action TEXT,
                    outcome TEXT,
                    feedback_score REAL,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            # Meta trends table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS meta_trends (
                    trend_id TEXT PRIMARY KEY,
                    trend_type TEXT NOT NULL,
                    trend_data TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    impact_score REAL NOT NULL,
                    last_updated TEXT NOT NULL
                )
            ''')
            
            # Recommendation effectiveness table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recommendation_effectiveness (
                    recommendation_type TEXT NOT NULL,
                    context_category TEXT NOT NULL,
                    success_rate REAL NOT NULL,
                    total_recommendations INTEGER NOT NULL,
                    last_updated TEXT NOT NULL,
                    PRIMARY KEY (recommendation_type, context_category)
                )
            ''')
            
            conn.commit()
    
    def generate_comprehensive_recommendations(self, context: RecommendationContext) -> RecommendationSet:
        """Generate comprehensive recommendations for a crafting scenario"""
        
        recommendations = []
        
        # Get user profile for personalization
        user_profile = self.get_user_profile(context.user_id)
        
        # Generate different types of recommendations
        modifier_recs = self._generate_modifier_recommendations(context, user_profile)
        method_recs = self._generate_method_recommendations(context, user_profile)
        budget_recs = self._generate_budget_recommendations(context, user_profile)
        timing_recs = self._generate_timing_recommendations(context, user_profile)
        alternative_recs = self._generate_alternative_recommendations(context, user_profile)
        
        recommendations.extend(modifier_recs)
        recommendations.extend(method_recs)
        recommendations.extend(budget_recs)
        recommendations.extend(timing_recs)
        recommendations.extend(alternative_recs)
        
        # Sort by priority and confidence
        recommendations.sort(key=lambda r: (r.priority == 'high', r.confidence), reverse=True)
        
        # Generate insights
        meta_insights = self._generate_meta_insights(context)
        user_insights = self._generate_user_insights(context, user_profile)
        market_timing = self._generate_market_timing_insights(context)
        
        # Determine overall strategy
        overall_strategy = self._determine_overall_strategy(context, recommendations)
        
        # Calculate confidence score
        confidence_score = self._calculate_overall_confidence(recommendations)
        
        recommendation_set = RecommendationSet(
            context=context,
            recommendations=recommendations[:15],  # Top 15 recommendations
            meta_insights=meta_insights,
            user_insights=user_insights,
            market_timing=market_timing,
            overall_strategy=overall_strategy,
            confidence_score=confidence_score,
            generated_at=datetime.now().isoformat()
        )
        
        # Store recommendation set
        self._store_recommendation_set(recommendation_set)
        
        return recommendation_set
    
    def _generate_modifier_recommendations(self, context: RecommendationContext, 
                                         user_profile: Dict) -> List[Recommendation]:
        """Generate modifier-specific recommendations"""
        recommendations = []
        
        if not self.modifier_database:
            return recommendations
        
        # Analyze current modifier combination
        analysis = self.modifier_database.analyze_modifier_combination(
            context.current_modifiers, context.item_base
        )
        
        # Get complementary modifier suggestions
        suggestions = self.modifier_database.suggest_complementary_modifiers(
            context.current_modifiers, context.item_base
        )
        
        # Filter suggestions based on user preferences
        user_preferred_categories = user_profile.get('preferred_categories', {})
        
        for suggestion in suggestions[:5]:  # Top 5 suggestions
            modifier_name = suggestion['modifier']
            score = suggestion['score']
            
            # Adjust score based on user preferences
            category = suggestion['category']
            if category in user_preferred_categories:
                score *= (1 + user_preferred_categories[category] * 0.3)
            
            # Check user success history with this modifier
            user_success = user_profile.get('modifier_success', {}).get(modifier_name, 0.5)
            score *= (0.8 + user_success * 0.4)
            
            if score > 0.6:  # High confidence threshold
                rec = Recommendation(
                    type="modifier",
                    title=f"Add {modifier_name}",
                    description=f"Consider adding {modifier_name} to your item",
                    confidence=min(0.95, score),
                    priority="high" if score > 0.8 else "medium",
                    reasoning=[
                        suggestion['reason'],
                        f"Matches your {category} preferences" if category in user_preferred_categories else None,
                        f"You have {user_success*100:.0f}% success rate with this modifier" if user_success > 0.6 else None
                    ],
                    data={
                        'modifier': modifier_name,
                        'type': suggestion['type'],
                        'category': category,
                        'meta_rating': suggestion['meta_rating'],
                        'crafting_difficulty': suggestion['crafting_difficulty']
                    },
                    expected_outcome={
                        'probability_increase': 0.1,
                        'cost_impact': suggestion['crafting_difficulty'] * 50,
                        'meta_relevance': suggestion['meta_rating']
                    },
                    implementation_steps=[
                        f"Ensure you have {3 - analysis['prefix_count'] if suggestion['type'] == 'prefix' else 3 - analysis['suffix_count']} available {suggestion['type']} slots",
                        f"Use {'essence' if modifier_name in ['Maximum Life', 'Maximum Energy Shield'] else 'chaos spam'} method",
                        "Monitor market prices for optimal timing"
                    ]
                )
                
                # Filter out None reasons
                rec.reasoning = [r for r in rec.reasoning if r is not None]
                recommendations.append(rec)
        
        return recommendations
    
    def _generate_method_recommendations(self, context: RecommendationContext, 
                                       user_profile: Dict) -> List[Recommendation]:
        """Generate crafting method recommendations"""
        recommendations = []
        
        if not self.probability_engine:
            return recommendations
        
        # Analyze different methods
        methods = ['chaos_spam', 'alt_regal', 'essence', 'fossil']
        method_analyses = []
        
        for method in methods:
            prob_analysis = self.probability_engine.calculate_exact_probabilities(
                context.current_modifiers, context.item_base, context.item_level, method
            )
            
            # Get user success rate with this method
            user_method_success = user_profile.get('method_success', {}).get(method, 0.5)
            
            # Calculate recommendation score
            score = (
                prob_analysis.combined_probability * 0.4 +
                (1 - prob_analysis.cost_distribution.get('expected_cost', 1000) / context.budget) * 0.3 +
                user_method_success * 0.3
            )
            
            method_analyses.append({
                'method': method,
                'probability': prob_analysis.combined_probability,
                'expected_cost': prob_analysis.cost_distribution.get('expected_cost', 0),
                'user_success': user_method_success,
                'score': score,
                'prob_analysis': prob_analysis
            })
        
        # Sort by score and recommend top methods
        method_analyses.sort(key=lambda x: x['score'], reverse=True)
        
        for i, method_data in enumerate(method_analyses[:3]):
            method = method_data['method']
            prob_analysis = method_data['prob_analysis']
            
            priority = "high" if i == 0 else "medium" if i == 1 else "low"
            
            rec = Recommendation(
                type="method",
                title=f"Use {method.replace('_', ' ').title()} Method",
                description=f"{method.replace('_', ' ').title()} is recommended for your goals",
                confidence=method_data['score'],
                priority=priority,
                reasoning=[
                    f"{prob_analysis.combined_probability*100:.2f}% success probability",
                    f"Expected cost: {method_data['expected_cost']:.0f} chaos orbs",
                    f"Your success rate with this method: {method_data['user_success']*100:.0f}%"
                ],
                data={
                    'method': method,
                    'probability': prob_analysis.combined_probability,
                    'expected_cost': method_data['expected_cost'],
                    'expected_attempts': prob_analysis.expected_attempts
                },
                expected_outcome={
                    'success_probability': prob_analysis.combined_probability,
                    'cost_range': prob_analysis.cost_distribution.get('cost_range_90_percent', (0, 0)),
                    'time_estimate': self._estimate_time_for_method(method, prob_analysis.expected_attempts)
                },
                implementation_steps=self._get_method_implementation_steps(method, context)
            )
            
            recommendations.append(rec)
        
        return recommendations
    
    def _generate_budget_recommendations(self, context: RecommendationContext, 
                                       user_profile: Dict) -> List[Recommendation]:
        """Generate budget optimization recommendations"""
        recommendations = []
        
        user_budget_patterns = user_profile.get('budget_patterns', {})
        typical_overspend = user_budget_patterns.get('overspend_factor', 1.2)
        
        # Market-adjusted budget recommendation
        if self.market_intelligence:
            market_insights = self.market_intelligence.get_crafting_market_insights(
                context.current_modifiers, 'chaos_spam', context.budget
            )
            
            recommended_multiplier = market_insights.get('recommended_budget_multiplier', 1.0)
            
            if recommended_multiplier > 1.1:
                rec = Recommendation(
                    type="budget",
                    title="Increase Budget Due to Market Conditions",
                    description=f"Consider increasing budget by {(recommended_multiplier-1)*100:.1f}%",
                    confidence=0.8,
                    priority="medium",
                    reasoning=[
                        f"Currency prices trending upward",
                        f"Market timing score: {market_insights.get('market_timing_score', 0):.2f}",
                        f"Your typical overspend factor: {typical_overspend:.1f}x"
                    ],
                    data={
                        'original_budget': context.budget,
                        'recommended_budget': context.budget * recommended_multiplier,
                        'market_factor': recommended_multiplier,
                        'user_factor': typical_overspend
                    },
                    expected_outcome={
                        'risk_reduction': 0.3,
                        'success_probability_increase': 0.15,
                        'cost_predictability': 0.8
                    },
                    implementation_steps=[
                        f"Increase budget to {context.budget * recommended_multiplier:.0f} chaos orbs",
                        "Monitor currency prices for optimal entry points",
                        "Set aside emergency reserve for market volatility"
                    ]
                )
                recommendations.append(rec)
        
        # Risk-based budget recommendation
        user_risk_tolerance = user_profile.get('risk_tolerance', 0.5)
        
        if user_risk_tolerance < 0.4:  # Conservative user
            safe_budget = context.budget * 1.5
            rec = Recommendation(
                type="budget",
                title="Conservative Budget Approach",
                description="Increase budget for safer crafting approach",
                confidence=0.7,
                priority="medium",
                reasoning=[
                    "Your profile shows conservative approach preference",
                    "Higher budget reduces risk of partial completion",
                    "Allows for backup strategies"
                ],
                data={
                    'risk_profile': 'conservative',
                    'recommended_budget': safe_budget,
                    'safety_margin': 0.5
                },
                expected_outcome={
                    'completion_probability': 0.9,
                    'stress_level': 'low',
                    'backup_options': 'multiple'
                },
                implementation_steps=[
                    f"Set budget to {safe_budget:.0f} chaos orbs",
                    "Plan primary and backup crafting methods",
                    "Start with lower-risk approaches"
                ]
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _generate_timing_recommendations(self, context: RecommendationContext, 
                                       user_profile: Dict) -> List[Recommendation]:
        """Generate timing-based recommendations"""
        recommendations = []
        
        if not self.market_intelligence:
            return recommendations
        
        # Get market forecast
        forecast = self.market_intelligence.generate_market_forecast('24h')
        
        # Analyze timing based on market conditions
        if forecast.market_conditions == 'bullish':
            rec = Recommendation(
                type="timing",
                title="Craft Soon - Favorable Market",
                description="Current market conditions favor immediate crafting",
                confidence=0.75,
                priority="medium",
                reasoning=[
                    f"Market conditions: {forecast.market_conditions}",
                    f"Opportunity score: {forecast.opportunity_score:.2f}",
                    "Currency prices expected to rise"
                ],
                data={
                    'market_conditions': forecast.market_conditions,
                    'opportunity_score': forecast.opportunity_score,
                    'recommended_window': '24-48 hours'
                },
                expected_outcome={
                    'cost_savings': 0.1,
                    'availability': 'high',
                    'timing_advantage': 'strong'
                },
                implementation_steps=[
                    "Begin crafting within 24-48 hours",
                    "Secure necessary currencies now",
                    "Monitor market for any sudden changes"
                ]
            )
            recommendations.append(rec)
        
        elif forecast.market_conditions == 'bearish':
            rec = Recommendation(
                type="timing",
                title="Wait for Better Market Conditions",
                description="Consider delaying crafting for better prices",
                confidence=0.7,
                priority="low",
                reasoning=[
                    f"Market conditions: {forecast.market_conditions}",
                    "Currency prices trending downward",
                    "Better opportunities likely in 2-7 days"
                ],
                data={
                    'market_conditions': forecast.market_conditions,
                    'wait_period': '2-7 days',
                    'potential_savings': 0.15
                },
                expected_outcome={
                    'cost_savings': 0.15,
                    'timing_advantage': 'moderate',
                    'patience_required': 'high'
                },
                implementation_steps=[
                    "Monitor market conditions daily",
                    "Set price alerts for key currencies",
                    "Prepare crafting plan for when conditions improve"
                ]
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _generate_alternative_recommendations(self, context: RecommendationContext, 
                                            user_profile: Dict) -> List[Recommendation]:
        """Generate alternative approach recommendations"""
        recommendations = []
        
        if not self.modifier_database:
            return recommendations
        
        # Suggest alternative modifier combinations
        analysis = self.modifier_database.analyze_modifier_combination(
            context.current_modifiers, context.item_base
        )
        
        if analysis.get('crafting_difficulty', 0) > 0.7:  # High difficulty
            rec = Recommendation(
                type="alternative",
                title="Consider Simpler Modifier Combination",
                description="Your current goal is very challenging - consider alternatives",
                confidence=0.6,
                priority="medium",
                reasoning=[
                    f"Current difficulty score: {analysis.get('crafting_difficulty', 0):.2f}",
                    "Simpler combinations have higher success rates",
                    "You can upgrade gradually"
                ],
                data={
                    'current_difficulty': analysis.get('crafting_difficulty', 0),
                    'alternative_approach': 'gradual_upgrade',
                    'risk_reduction': 0.4
                },
                expected_outcome={
                    'initial_success_rate': 0.8,
                    'upgrade_path': 'available',
                    'total_cost': 'potentially_lower'
                },
                implementation_steps=[
                    "Start with 2-3 core modifiers",
                    "Complete initial item successfully",
                    "Use Divine Orbs or additional crafting for upgrades"
                ]
            )
            recommendations.append(rec)
        
        # Suggest build archetype matches
        if analysis.get('build_archetype_matches'):
            best_match = analysis['build_archetype_matches'][0]
            
            if best_match['match_score'] < 0.8:  # Not a perfect match
                rec = Recommendation(
                    type="alternative",
                    title=f"Align with {best_match['archetype']} Build",
                    description=f"Consider adjusting modifiers to match popular build archetype",
                    confidence=0.65,
                    priority="low",
                    reasoning=[
                        f"Current match: {best_match['match_score']*100:.0f}%",
                        f"Archetype popularity: {best_match['popularity']*100:.0f}%",
                        "Better market support and guides available"
                    ],
                    data={
                        'target_archetype': best_match['archetype'],
                        'missing_modifiers': best_match['missing_mods'],
                        'current_match': best_match['match_score']
                    },
                    expected_outcome={
                        'build_synergy': 'high',
                        'community_support': 'excellent',
                        'upgrade_path': 'well_defined'
                    },
                    implementation_steps=[
                        f"Add missing modifiers: {', '.join(best_match['missing_mods'][:3])}",
                        "Research build guides for optimization tips",
                        "Consider gear synergies with other items"
                    ]
                )
                recommendations.append(rec)
        
        return recommendations
    
    def _generate_meta_insights(self, context: RecommendationContext) -> Dict[str, Any]:
        """Generate meta game insights"""
        if not self.modifier_database:
            return {}
        
        meta_analysis = self.modifier_database.generate_meta_analysis(context.league)
        
        insights = {
            'trending_modifiers': meta_analysis.top_modifiers[:5],
            'emerging_trends': meta_analysis.emerging_trends[:3],
            'your_modifiers_rank': [],
            'meta_alignment_score': 0.0
        }
        
        # Calculate how well user's modifiers align with meta
        top_mod_names = [mod[0] for mod in meta_analysis.top_modifiers[:20]]
        user_meta_mods = [mod for mod in context.current_modifiers if mod in top_mod_names]
        
        if context.current_modifiers:
            insights['meta_alignment_score'] = len(user_meta_mods) / len(context.current_modifiers)
        
        for mod in context.current_modifiers:
            rank = next((i for i, (name, _) in enumerate(meta_analysis.top_modifiers) if name == mod), None)
            if rank is not None:
                insights['your_modifiers_rank'].append((mod, rank + 1))
        
        return insights
    
    def _generate_user_insights(self, context: RecommendationContext, 
                              user_profile: Dict) -> Dict[str, Any]:
        """Generate user-specific insights"""
        insights = {
            'experience_level': user_profile.get('experience_level', 'intermediate'),
            'success_rate_history': user_profile.get('overall_success_rate', 0.5),
            'preferred_methods': user_profile.get('method_preferences', {}),
            'risk_profile': user_profile.get('risk_tolerance', 0.5),
            'learning_progress': user_profile.get('learning_score', 0.3),
            'recommendations_followed': user_profile.get('recommendations_followed', 0),
            'personalization_confidence': min(1.0, user_profile.get('data_points', 0) / 20)
        }
        
        return insights
    
    def _generate_market_timing_insights(self, context: RecommendationContext) -> Dict[str, Any]:
        """Generate market timing insights"""
        if not self.market_intelligence:
            return {}
        
        market_insights = self.market_intelligence.get_crafting_market_insights(
            context.current_modifiers, 'chaos_spam', context.budget
        )
        
        return {
            'market_timing_score': market_insights.get('market_timing_score', 0),
            'cost_trend': market_insights.get('cost_trend_direction', 'stable'),
            'recommendations': market_insights.get('recommendations', []),
            'currency_analysis': market_insights.get('currency_analysis', {}),
            'optimal_window': self._calculate_optimal_timing_window(market_insights)
        }
    
    def _calculate_optimal_timing_window(self, market_insights: Dict) -> str:
        """Calculate optimal timing window for crafting"""
        timing_score = market_insights.get('market_timing_score', 0)
        cost_trend = market_insights.get('cost_trend_direction', 'stable')
        
        if timing_score > 0.7 and cost_trend != 'increasing':
            return "immediate"
        elif timing_score > 0.3:
            return "within_24h"
        elif cost_trend == 'decreasing':
            return "wait_2_7_days"
        else:
            return "monitor_closely"
    
    def _determine_overall_strategy(self, context: RecommendationContext, 
                                  recommendations: List[Recommendation]) -> str:
        """Determine overall crafting strategy"""
        high_priority_recs = [r for r in recommendations if r.priority == 'high']
        
        if not high_priority_recs:
            return "standard_approach"
        
        # Analyze recommendation types
        rec_types = Counter(r.type for r in high_priority_recs)
        
        if rec_types.get('timing', 0) > 0:
            return "timing_focused"
        elif rec_types.get('alternative', 0) > 0:
            return "alternative_approach"
        elif rec_types.get('budget', 0) > 0:
            return "budget_optimized"
        elif rec_types.get('method', 0) > 0:
            return "method_focused"
        else:
            return "modifier_focused"
    
    def _calculate_overall_confidence(self, recommendations: List[Recommendation]) -> float:
        """Calculate overall confidence in recommendations"""
        if not recommendations:
            return 0.0
        
        high_priority = [r.confidence for r in recommendations if r.priority == 'high']
        medium_priority = [r.confidence for r in recommendations if r.priority == 'medium']
        
        if high_priority:
            return np.mean(high_priority)
        elif medium_priority:
            return np.mean(medium_priority) * 0.8
        else:
            return np.mean([r.confidence for r in recommendations]) * 0.6
    
    def _estimate_time_for_method(self, method: str, expected_attempts: float) -> str:
        """Estimate time required for crafting method"""
        time_per_attempt = {
            'chaos_spam': 30,  # seconds
            'alt_regal': 60,
            'essence': 45,
            'fossil': 90
        }
        
        total_seconds = expected_attempts * time_per_attempt.get(method, 45)
        
        if total_seconds < 300:  # 5 minutes
            return "5-10 minutes"
        elif total_seconds < 1800:  # 30 minutes
            return "15-30 minutes"
        elif total_seconds < 3600:  # 1 hour
            return "30-60 minutes"
        else:
            return "1+ hours"
    
    def _get_method_implementation_steps(self, method: str, context: RecommendationContext) -> List[str]:
        """Get implementation steps for a crafting method"""
        steps = {
            'chaos_spam': [
                "Start with a rare base item or use Orb of Alchemy",
                "Use Chaos Orbs repeatedly until desired modifiers appear",
                "Use Divine Orbs to optimize values if successful",
                "Have Orb of Annulment ready for unwanted modifiers"
            ],
            'alt_regal': [
                "Start with white base item",
                "Use Orb of Transmutation to make magic",
                "Use Alteration Orbs for desired modifier",
                "Use Regal Orb to upgrade to rare",
                "Continue with Exalted Orbs if needed"
            ],
            'essence': [
                "Identify required essences for guaranteed modifiers",
                "Start with white base item",
                "Use appropriate essence to guarantee key modifier",
                "Continue crafting for remaining modifiers"
            ],
            'fossil': [
                "Select fossils that bias toward target modifiers",
                "Acquire appropriate resonators",
                "Apply fossil combination to base item",
                "Repeat until satisfactory result"
            ]
        }
        
        return steps.get(method, ["Execute crafting method", "Monitor progress", "Adjust as needed"])
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get or create user profile"""
        if user_id in self.user_profiles:
            return self.user_profiles[user_id]
        
        # Create default profile
        default_profile = {
            'experience_level': 'intermediate',
            'overall_success_rate': 0.5,
            'method_preferences': {},
            'modifier_success': {},
            'risk_tolerance': 0.5,
            'preferred_categories': {},
            'budget_patterns': {'overspend_factor': 1.2},
            'learning_score': 0.3,
            'data_points': 0,
            'recommendations_followed': 0
        }
        
        self.user_profiles[user_id] = default_profile
        return default_profile
    
    def record_recommendation_feedback(self, user_id: str, recommendation_id: str, 
                                     action: str, outcome: Optional[str] = None, 
                                     feedback_score: Optional[float] = None):
        """Record user feedback on recommendations"""
        timestamp = datetime.now().isoformat()
        
        # Update recommendation outcomes
        self.recommendation_outcomes[recommendation_id]['accepted' if action == 'accepted' else 'rejected'] += 1
        
        if outcome:
            self.recommendation_outcomes[recommendation_id][outcome] += 1
        
        # Update user profile
        user_profile = self.get_user_profile(user_id)
        user_profile['data_points'] += 1
        
        if action == 'accepted':
            user_profile['recommendations_followed'] += 1
        
        if feedback_score is not None:
            # Adjust learning score
            user_profile['learning_score'] = min(1.0, user_profile['learning_score'] + 0.05)
        
        # Store in database
        with sqlite3.connect(self.recommendations_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO recommendation_history 
                (user_id, recommendation_type, recommendation_data, context, 
                 user_action, outcome, feedback_score, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, "feedback", recommendation_id, "{}", action, outcome, feedback_score, timestamp))
            conn.commit()
    
    def _store_recommendation_set(self, recommendation_set: RecommendationSet):
        """Store recommendation set for learning"""
        # This would store the recommendation set for later analysis
        user_id = recommendation_set.context.user_id
        self.recommendation_history[user_id].append(recommendation_set)
        
        # Keep only recent recommendations
        if len(self.recommendation_history[user_id]) > 50:
            self.recommendation_history[user_id] = self.recommendation_history[user_id][-50:]
    
    def load_recommendation_data(self):
        """Load existing recommendation data"""
        try:
            with sqlite3.connect(self.recommendations_db_path) as conn:
                cursor = conn.cursor()
                
                # Load user profiles
                cursor.execute('SELECT user_id, preferences FROM user_profiles')
                for row in cursor.fetchall():
                    user_id, preferences = row
                    self.user_profiles[user_id] = json.loads(preferences)
                    
        except Exception as e:
            print(f"Error loading recommendation data: {e}")
    
    def export_recommendations_data(self, file_path: str):
        """Export recommendations data"""
        export_data = {
            'user_profiles': self.user_profiles,
            'recommendation_outcomes': dict(self.recommendation_outcomes),
            'weight_factors': self.weight_factors,
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2)


# Global intelligent recommendations instance
intelligent_recommendations = IntelligentRecommendationSystem()