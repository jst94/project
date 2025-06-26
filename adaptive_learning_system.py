"""
Adaptive Learning System for PoE Craft Helper
Learns from user behavior, crafting success patterns, and continuously improves recommendations
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import sqlite3
import os


@dataclass
class LearningEvent:
    """Represents a learning event in the system"""
    event_type: str  # 'crafting_session', 'user_feedback', 'method_success', 'prediction_accuracy'
    timestamp: str
    session_id: str
    context: Dict[str, Any]
    outcome: Dict[str, Any]
    feedback_score: Optional[float] = None


@dataclass
class UserPattern:
    """Represents learned user behavior patterns"""
    user_id: str
    preferred_methods: Dict[str, float]
    risk_tolerance: float
    budget_patterns: Dict[str, float]
    time_preferences: Dict[str, float]
    success_patterns: Dict[str, List[float]]
    confidence: float


class AdaptiveLearningSystem:
    """Main learning system that adapts to user behavior and improves predictions"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.learning_db_path = os.path.join(data_dir, "learning_system.db")
        
        # Learning parameters
        self.learning_rate = 0.1
        self.memory_decay = 0.95
        self.confidence_threshold = 0.7
        self.min_samples_for_learning = 5
        
        # Learning data structures
        self.user_patterns = {}
        self.method_performance = defaultdict(lambda: {'successes': 0, 'attempts': 0, 'costs': []})
        self.prediction_accuracy = defaultdict(list)
        self.recent_events = deque(maxlen=1000)
        
        # Adaptive weights for different factors
        self.adaptive_weights = {
            'user_preference': 0.3,
            'historical_success': 0.25,
            'market_conditions': 0.2,
            'modifier_complexity': 0.15,
            'recent_performance': 0.1
        }
        
        # Initialize database
        self.init_learning_database()
        
        # Load existing learning data
        self.load_learning_data()
    
    def init_learning_database(self):
        """Initialize SQLite database for learning data"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        with sqlite3.connect(self.learning_db_path) as conn:
            cursor = conn.cursor()
            
            # Learning events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learning_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    session_id TEXT,
                    context TEXT NOT NULL,
                    outcome TEXT NOT NULL,
                    feedback_score REAL
                )
            ''')
            
            # User patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_patterns (
                    user_id TEXT PRIMARY KEY,
                    preferred_methods TEXT NOT NULL,
                    risk_tolerance REAL NOT NULL,
                    budget_patterns TEXT NOT NULL,
                    time_preferences TEXT NOT NULL,
                    success_patterns TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    last_updated TEXT NOT NULL
                )
            ''')
            
            # Method performance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS method_performance (
                    method TEXT NOT NULL,
                    modifier_combination TEXT NOT NULL,
                    successes INTEGER DEFAULT 0,
                    attempts INTEGER DEFAULT 0,
                    average_cost REAL DEFAULT 0,
                    last_updated TEXT NOT NULL,
                    PRIMARY KEY (method, modifier_combination)
                )
            ''')
            
            # Prediction accuracy table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prediction_accuracy (
                    prediction_type TEXT NOT NULL,
                    predicted_value REAL NOT NULL,
                    actual_value REAL NOT NULL,
                    accuracy_score REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            conn.commit()
    
    def record_learning_event(self, event: LearningEvent):
        """Record a learning event"""
        self.recent_events.append(event)
        
        # Store in database
        with sqlite3.connect(self.learning_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO learning_events 
                (event_type, timestamp, session_id, context, outcome, feedback_score)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                event.event_type,
                event.timestamp,
                event.session_id,
                json.dumps(event.context),
                json.dumps(event.outcome),
                event.feedback_score
            ))
            conn.commit()
        
        # Process the event for learning
        self.process_learning_event(event)
    
    def process_learning_event(self, event: LearningEvent):
        """Process a learning event to update models"""
        if event.event_type == 'crafting_session':
            self.learn_from_crafting_session(event)
        elif event.event_type == 'user_feedback':
            self.learn_from_user_feedback(event)
        elif event.event_type == 'method_success':
            self.learn_from_method_performance(event)
        elif event.event_type == 'prediction_accuracy':
            self.learn_from_prediction_accuracy(event)
    
    def learn_from_crafting_session(self, event: LearningEvent):
        """Learn from completed crafting sessions"""
        context = event.context
        outcome = event.outcome
        
        method = context.get('method', 'unknown')
        modifiers = context.get('target_modifiers', [])
        budget = context.get('budget', 0)
        success = outcome.get('success', False)
        actual_cost = outcome.get('actual_cost', 0)
        attempts = outcome.get('attempts', 1)
        
        # Update method performance
        mod_combo = '+'.join(sorted(modifiers))
        self.method_performance[method]['attempts'] += 1
        if success:
            self.method_performance[method]['successes'] += 1
        self.method_performance[method]['costs'].append(actual_cost)
        
        # Update user patterns
        user_id = context.get('user_id', 'default')
        if user_id not in self.user_patterns:
            self.user_patterns[user_id] = UserPattern(
                user_id=user_id,
                preferred_methods={},
                risk_tolerance=0.5,
                budget_patterns={},
                time_preferences={},
                success_patterns={},
                confidence=0.1
            )
        
        user_pattern = self.user_patterns[user_id]
        
        # Update method preference based on success
        if method not in user_pattern.preferred_methods:
            user_pattern.preferred_methods[method] = 0.5
        
        preference_change = 0.1 if success else -0.05
        user_pattern.preferred_methods[method] = max(0.1, min(1.0, 
            user_pattern.preferred_methods[method] + preference_change))
        
        # Update risk tolerance
        cost_ratio = actual_cost / max(budget, 1)
        if cost_ratio > 1.5:  # Went significantly over budget
            user_pattern.risk_tolerance = max(0.1, user_pattern.risk_tolerance - 0.05)
        elif cost_ratio < 0.5:  # Very conservative spending
            user_pattern.risk_tolerance = min(1.0, user_pattern.risk_tolerance + 0.02)
        
        # Update success patterns
        if mod_combo not in user_pattern.success_patterns:
            user_pattern.success_patterns[mod_combo] = []
        
        user_pattern.success_patterns[mod_combo].append(1.0 if success else 0.0)
        # Keep only recent results
        if len(user_pattern.success_patterns[mod_combo]) > 20:
            user_pattern.success_patterns[mod_combo] = user_pattern.success_patterns[mod_combo][-20:]
        
        # Update confidence
        user_pattern.confidence = min(1.0, user_pattern.confidence + 0.02)
        
        # Save updated patterns
        self.save_user_pattern(user_pattern)
    
    def learn_from_user_feedback(self, event: LearningEvent):
        """Learn from explicit user feedback"""
        feedback_score = event.feedback_score
        context = event.context
        
        prediction_type = context.get('prediction_type', 'unknown')
        predicted_value = context.get('predicted_value', 0)
        user_rating = feedback_score  # 0-1 scale
        
        # Update prediction accuracy tracking
        self.prediction_accuracy[prediction_type].append(user_rating)
        
        # Adjust adaptive weights based on feedback
        if prediction_type in self.adaptive_weights and len(self.prediction_accuracy[prediction_type]) >= 5:
            recent_accuracy = np.mean(self.prediction_accuracy[prediction_type][-5:])
            
            # If this prediction type is performing well, increase its weight
            if recent_accuracy > 0.7:
                self.adaptive_weights[prediction_type] = min(0.5, 
                    self.adaptive_weights[prediction_type] * 1.05)
            elif recent_accuracy < 0.4:
                self.adaptive_weights[prediction_type] = max(0.05, 
                    self.adaptive_weights[prediction_type] * 0.95)
        
        # Store in database
        with sqlite3.connect(self.learning_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO prediction_accuracy 
                (prediction_type, predicted_value, actual_value, accuracy_score, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                prediction_type,
                predicted_value,
                feedback_score,
                feedback_score,
                event.timestamp
            ))
            conn.commit()
    
    def learn_from_method_performance(self, event: LearningEvent):
        """Learn from method performance data"""
        context = event.context
        outcome = event.outcome
        
        method = context.get('method', 'unknown')
        predicted_success_rate = context.get('predicted_success_rate', 0)
        actual_success_rate = outcome.get('actual_success_rate', 0)
        
        # Calculate prediction accuracy
        accuracy = 1.0 - abs(predicted_success_rate - actual_success_rate)
        
        # Update method-specific learning
        if method not in self.prediction_accuracy:
            self.prediction_accuracy[method] = []
        
        self.prediction_accuracy[method].append(accuracy)
        
        # Keep only recent predictions
        if len(self.prediction_accuracy[method]) > 50:
            self.prediction_accuracy[method] = self.prediction_accuracy[method][-50:]
    
    def learn_from_prediction_accuracy(self, event: LearningEvent):
        """Learn from prediction accuracy measurements"""
        context = event.context
        outcome = event.outcome
        
        prediction_type = context.get('prediction_type', 'cost')
        predicted_value = context.get('predicted_value', 0)
        actual_value = outcome.get('actual_value', 0)
        
        # Calculate accuracy score
        if prediction_type == 'cost':
            # Cost predictions - use relative error
            relative_error = abs(predicted_value - actual_value) / max(actual_value, 1)
            accuracy = max(0, 1.0 - relative_error)
        elif prediction_type == 'attempts':
            # Attempt predictions - use relative error with cap
            relative_error = abs(predicted_value - actual_value) / max(actual_value, 1)
            accuracy = max(0, 1.0 - min(2.0, relative_error))
        else:
            # Generic accuracy
            accuracy = 1.0 - abs(predicted_value - actual_value)
        
        # Update prediction tracking
        self.prediction_accuracy[prediction_type].append(accuracy)
        
        # Adjust learning parameters based on accuracy trends
        if len(self.prediction_accuracy[prediction_type]) >= 10:
            recent_trend = np.mean(self.prediction_accuracy[prediction_type][-10:])
            older_trend = np.mean(self.prediction_accuracy[prediction_type][-20:-10]) if len(self.prediction_accuracy[prediction_type]) >= 20 else recent_trend
            
            # If accuracy is improving, be more aggressive with learning
            if recent_trend > older_trend + 0.1:
                self.learning_rate = min(0.2, self.learning_rate * 1.1)
            elif recent_trend < older_trend - 0.1:
                self.learning_rate = max(0.05, self.learning_rate * 0.9)
    
    def get_adaptive_recommendations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get adaptive recommendations based on learned patterns"""
        user_id = context.get('user_id', 'default')
        target_modifiers = context.get('target_modifiers', [])
        budget = context.get('budget', 1000)
        item_base = context.get('item_base', 'unknown')
        
        # Get user pattern
        user_pattern = self.user_patterns.get(user_id)
        if not user_pattern or user_pattern.confidence < self.confidence_threshold:
            return self.get_default_recommendations(context)
        
        # Calculate method recommendations based on learned preferences
        method_scores = {}
        for method, preference in user_pattern.preferred_methods.items():
            # Base score from user preference
            score = preference * self.adaptive_weights['user_preference']
            
            # Add historical success rate
            mod_combo = '+'.join(sorted(target_modifiers))
            if mod_combo in user_pattern.success_patterns:
                success_rate = np.mean(user_pattern.success_patterns[mod_combo])
                score += success_rate * self.adaptive_weights['historical_success']
            
            # Add method performance
            if method in self.method_performance:
                perf = self.method_performance[method]
                if perf['attempts'] > 0:
                    method_success_rate = perf['successes'] / perf['attempts']
                    score += method_success_rate * self.adaptive_weights['recent_performance']
            
            method_scores[method] = score
        
        # Get top recommendation
        recommended_method = max(method_scores.items(), key=lambda x: x[1]) if method_scores else ('chaos_spam', 0.5)
        
        # Calculate adaptive budget recommendation
        budget_multiplier = 1.0
        if user_pattern.risk_tolerance > 0.7:
            budget_multiplier = 1.2  # User is willing to spend more
        elif user_pattern.risk_tolerance < 0.3:
            budget_multiplier = 0.8  # User is conservative
        
        recommended_budget = budget * budget_multiplier
        
        # Calculate confidence in recommendation
        recommendation_confidence = (
            user_pattern.confidence * 0.4 +
            max(method_scores.values()) * 0.6
        ) if method_scores else 0.3
        
        return {
            'recommended_method': recommended_method[0],
            'method_confidence': recommended_method[1],
            'recommended_budget': recommended_budget,
            'budget_reasoning': f"Adjusted based on risk tolerance: {user_pattern.risk_tolerance:.2f}",
            'overall_confidence': recommendation_confidence,
            'learning_insights': {
                'user_sessions': sum(len(patterns) for patterns in user_pattern.success_patterns.values()),
                'method_preferences': user_pattern.preferred_methods,
                'risk_profile': 'Conservative' if user_pattern.risk_tolerance < 0.4 else 'Aggressive' if user_pattern.risk_tolerance > 0.7 else 'Balanced'
            },
            'adaptive_weights': self.adaptive_weights.copy()
        }
    
    def get_default_recommendations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get default recommendations for new users or low confidence situations"""
        return {
            'recommended_method': 'chaos_spam',
            'method_confidence': 0.3,
            'recommended_budget': context.get('budget', 1000),
            'budget_reasoning': "Default recommendation for new users",
            'overall_confidence': 0.3,
            'learning_insights': {
                'user_sessions': 0,
                'method_preferences': {},
                'risk_profile': 'Unknown - learning in progress'
            },
            'adaptive_weights': self.adaptive_weights.copy()
        }
    
    def update_prediction_accuracy(self, prediction_type: str, predicted: float, actual: float):
        """Update prediction accuracy tracking"""
        event = LearningEvent(
            event_type='prediction_accuracy',
            timestamp=datetime.now().isoformat(),
            session_id='',
            context={'prediction_type': prediction_type, 'predicted_value': predicted},
            outcome={'actual_value': actual}
        )
        self.record_learning_event(event)
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get comprehensive learning system statistics"""
        stats = {
            'system_maturity': {
                'total_events': len(self.recent_events),
                'learning_confidence': np.mean([up.confidence for up in self.user_patterns.values()]) if self.user_patterns else 0.0,
                'data_points': sum(len(events) for events in self.prediction_accuracy.values())
            },
            'prediction_accuracy': {},
            'method_performance': {},
            'user_insights': {
                'total_users': len(self.user_patterns),
                'active_learners': len([up for up in self.user_patterns.values() if up.confidence > 0.5])
            },
            'adaptive_weights': self.adaptive_weights.copy()
        }
        
        # Calculate prediction accuracy stats
        for pred_type, accuracies in self.prediction_accuracy.items():
            if accuracies:
                stats['prediction_accuracy'][pred_type] = {
                    'mean_accuracy': np.mean(accuracies),
                    'recent_accuracy': np.mean(accuracies[-10:]) if len(accuracies) >= 10 else np.mean(accuracies),
                    'total_predictions': len(accuracies),
                    'trend': 'improving' if len(accuracies) >= 20 and np.mean(accuracies[-10:]) > np.mean(accuracies[-20:-10]) else 'stable'
                }
        
        # Method performance stats
        for method, perf in self.method_performance.items():
            if perf['attempts'] > 0:
                stats['method_performance'][method] = {
                    'success_rate': perf['successes'] / perf['attempts'],
                    'total_attempts': perf['attempts'],
                    'average_cost': np.mean(perf['costs']) if perf['costs'] else 0,
                    'cost_variance': np.std(perf['costs']) if len(perf['costs']) > 1 else 0
                }
        
        return stats
    
    def save_user_pattern(self, user_pattern: UserPattern):
        """Save user pattern to database"""
        with sqlite3.connect(self.learning_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO user_patterns 
                (user_id, preferred_methods, risk_tolerance, budget_patterns, 
                 time_preferences, success_patterns, confidence, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_pattern.user_id,
                json.dumps(user_pattern.preferred_methods),
                user_pattern.risk_tolerance,
                json.dumps(user_pattern.budget_patterns),
                json.dumps(user_pattern.time_preferences),
                json.dumps(user_pattern.success_patterns),
                user_pattern.confidence,
                datetime.now().isoformat()
            ))
            conn.commit()
    
    def load_learning_data(self):
        """Load existing learning data from database"""
        try:
            with sqlite3.connect(self.learning_db_path) as conn:
                cursor = conn.cursor()
                
                # Load user patterns
                cursor.execute('SELECT * FROM user_patterns')
                for row in cursor.fetchall():
                    user_id = row[0]
                    self.user_patterns[user_id] = UserPattern(
                        user_id=user_id,
                        preferred_methods=json.loads(row[1]),
                        risk_tolerance=row[2],
                        budget_patterns=json.loads(row[3]),
                        time_preferences=json.loads(row[4]),
                        success_patterns=json.loads(row[5]),
                        confidence=row[6]
                    )
                
                # Load method performance
                cursor.execute('SELECT * FROM method_performance')
                for row in cursor.fetchall():
                    method = row[0]
                    self.method_performance[method] = {
                        'successes': row[2],
                        'attempts': row[3],
                        'costs': [row[4]] if row[4] > 0 else []
                    }
                
                # Load recent prediction accuracy
                cursor.execute('''
                    SELECT prediction_type, accuracy_score 
                    FROM prediction_accuracy 
                    WHERE timestamp > datetime('now', '-30 days')
                    ORDER BY timestamp DESC
                ''')
                for row in cursor.fetchall():
                    pred_type, accuracy = row
                    self.prediction_accuracy[pred_type].append(accuracy)
                
        except Exception as e:
            print(f"Error loading learning data: {e}")
    
    def export_learning_model(self, file_path: str):
        """Export the complete learning model"""
        model_data = {
            'user_patterns': {uid: asdict(pattern) for uid, pattern in self.user_patterns.items()},
            'method_performance': dict(self.method_performance),
            'prediction_accuracy': dict(self.prediction_accuracy),
            'adaptive_weights': self.adaptive_weights,
            'learning_parameters': {
                'learning_rate': self.learning_rate,
                'memory_decay': self.memory_decay,
                'confidence_threshold': self.confidence_threshold
            },
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(file_path, 'w') as f:
            json.dump(model_data, f, indent=2)


# Global learning system instance
learning_system = AdaptiveLearningSystem()