"""
Crafting Session Tracking and User Preferences
Tracks crafting sessions, saves preferences, and provides analytics
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sqlite3
from dataclasses import dataclass, asdict
import threading


@dataclass
class CraftingSession:
    """Data class for crafting session"""
    session_id: str
    start_time: float
    end_time: Optional[float]
    item_base: str
    target_modifiers: List[str]
    method_used: str
    budget_allocated: float
    actual_cost: Optional[float]
    success: Optional[bool]
    notes: str
    timestamp: str


@dataclass
class UserPreferences:
    """Data class for user preferences"""
    default_budget: float
    preferred_method: str
    overlay_opacity: float
    overlay_position: str
    auto_refresh_prices: bool
    price_update_interval: int
    show_budget_optimization: bool
    league_name: str
    ui_theme: str
    auto_detect_items: bool


class SessionTracker:
    """Tracks crafting sessions and manages user data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "crafting_sessions.db")
        self.preferences_path = os.path.join(data_dir, "user_preferences.json")
        self.current_session = None
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize database
        self.init_database()
        
        # Load user preferences
        self.preferences = self.load_preferences()
        
    def init_database(self):
        """Initialize SQLite database for session tracking"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    start_time REAL NOT NULL,
                    end_time REAL,
                    item_base TEXT NOT NULL,
                    target_modifiers TEXT NOT NULL,
                    method_used TEXT NOT NULL,
                    budget_allocated REAL NOT NULL,
                    actual_cost REAL,
                    success INTEGER,
                    notes TEXT,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            # Analytics table for aggregated data
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analytics (
                    date TEXT PRIMARY KEY,
                    total_sessions INTEGER DEFAULT 0,
                    successful_sessions INTEGER DEFAULT 0,
                    total_cost REAL DEFAULT 0,
                    average_cost REAL DEFAULT 0,
                    most_used_method TEXT,
                    most_crafted_base TEXT
                )
            ''')
            
            conn.commit()
            
    def start_session(self, item_base: str, target_modifiers: List[str], 
                     method: str, budget: float) -> str:
        """Start a new crafting session"""
        session_id = f"session_{int(time.time())}_{hash(item_base)%10000}"
        
        self.current_session = CraftingSession(
            session_id=session_id,
            start_time=time.time(),
            end_time=None,
            item_base=item_base,
            target_modifiers=target_modifiers,
            method_used=method,
            budget_allocated=budget,
            actual_cost=None,
            success=None,
            notes="",
            timestamp=datetime.now().isoformat()
        )
        
        return session_id
        
    def end_session(self, actual_cost: Optional[float] = None, 
                   success: Optional[bool] = None, notes: str = "") -> bool:
        """End the current crafting session"""
        if not self.current_session:
            return False
            
        self.current_session.end_time = time.time()
        self.current_session.actual_cost = actual_cost
        self.current_session.success = success
        self.current_session.notes = notes
        
        # Save to database
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    self.current_session.session_id,
                    self.current_session.start_time,
                    self.current_session.end_time,
                    self.current_session.item_base,
                    json.dumps(self.current_session.target_modifiers),
                    self.current_session.method_used,
                    self.current_session.budget_allocated,
                    self.current_session.actual_cost,
                    1 if self.current_session.success else 0,
                    self.current_session.notes,
                    self.current_session.timestamp
                ))
                conn.commit()
                
            # Update analytics
            self.update_analytics()
            
            self.current_session = None
            return True
            
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
            
    def get_session_history(self, limit: int = 50) -> List[Dict]:
        """Get recent crafting session history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM sessions 
                    ORDER BY start_time DESC 
                    LIMIT ?
                ''', (limit,))
                
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                sessions = []
                for row in rows:
                    session_dict = dict(zip(columns, row))
                    session_dict['target_modifiers'] = json.loads(session_dict['target_modifiers'])
                    session_dict['success'] = bool(session_dict['success']) if session_dict['success'] is not None else None
                    sessions.append(session_dict)
                    
                return sessions
                
        except Exception as e:
            print(f"Error loading session history: {e}")
            return []
            
    def get_analytics(self, days: int = 30) -> Dict:
        """Get crafting analytics for the specified period"""
        try:
            cutoff_time = time.time() - (days * 24 * 60 * 60)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total sessions
                cursor.execute('''
                    SELECT COUNT(*) FROM sessions WHERE start_time > ?
                ''', (cutoff_time,))
                total_sessions = cursor.fetchone()[0]
                
                # Successful sessions
                cursor.execute('''
                    SELECT COUNT(*) FROM sessions 
                    WHERE start_time > ? AND success = 1
                ''', (cutoff_time,))
                successful_sessions = cursor.fetchone()[0]
                
                # Total and average cost
                cursor.execute('''
                    SELECT SUM(actual_cost), AVG(actual_cost) 
                    FROM sessions 
                    WHERE start_time > ? AND actual_cost IS NOT NULL
                ''', (cutoff_time,))
                cost_data = cursor.fetchone()
                total_cost = cost_data[0] if cost_data[0] else 0
                avg_cost = cost_data[1] if cost_data[1] else 0
                
                # Most used method
                cursor.execute('''
                    SELECT method_used, COUNT(*) as count 
                    FROM sessions 
                    WHERE start_time > ? 
                    GROUP BY method_used 
                    ORDER BY count DESC 
                    LIMIT 1
                ''', (cutoff_time,))
                method_data = cursor.fetchone()
                most_used_method = method_data[0] if method_data else "None"
                
                # Most crafted base
                cursor.execute('''
                    SELECT item_base, COUNT(*) as count 
                    FROM sessions 
                    WHERE start_time > ? 
                    GROUP BY item_base 
                    ORDER BY count DESC 
                    LIMIT 1
                ''', (cutoff_time,))
                base_data = cursor.fetchone()
                most_crafted_base = base_data[0] if base_data else "None"
                
                success_rate = (successful_sessions / total_sessions * 100) if total_sessions > 0 else 0
                
                return {
                    'period_days': days,
                    'total_sessions': total_sessions,
                    'successful_sessions': successful_sessions,
                    'success_rate': success_rate,
                    'total_cost': total_cost,
                    'average_cost': avg_cost,
                    'most_used_method': most_used_method,
                    'most_crafted_base': most_crafted_base,
                    'generated_at': datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"Error generating analytics: {e}")
            return {}
            
    def update_analytics(self):
        """Update daily analytics"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            analytics = self.get_analytics(1)  # Get today's data
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO analytics 
                    (date, total_sessions, successful_sessions, total_cost, 
                     average_cost, most_used_method, most_crafted_base)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    today,
                    analytics.get('total_sessions', 0),
                    analytics.get('successful_sessions', 0),
                    analytics.get('total_cost', 0),
                    analytics.get('average_cost', 0),
                    analytics.get('most_used_method', ''),
                    analytics.get('most_crafted_base', '')
                ))
                conn.commit()
                
        except Exception as e:
            print(f"Error updating analytics: {e}")
            
    def load_preferences(self) -> UserPreferences:
        """Load user preferences from file"""
        default_prefs = UserPreferences(
            default_budget=1000.0,
            preferred_method="chaos_spam",
            overlay_opacity=0.95,
            overlay_position="top-right",
            auto_refresh_prices=True,
            price_update_interval=300,
            show_budget_optimization=True,
            league_name="Secrets of the Atlas",
            ui_theme="dark",
            auto_detect_items=False
        )
        
        try:
            if os.path.exists(self.preferences_path):
                with open(self.preferences_path, 'r') as f:
                    data = json.load(f)
                    return UserPreferences(**data)
        except Exception as e:
            print(f"Error loading preferences: {e}")
            
        return default_prefs
        
    def save_preferences(self, preferences: UserPreferences) -> bool:
        """Save user preferences to file"""
        try:
            with open(self.preferences_path, 'w') as f:
                json.dump(asdict(preferences), f, indent=2)
            self.preferences = preferences
            return True
        except Exception as e:
            print(f"Error saving preferences: {e}")
            return False
            
    def export_session_data(self, output_path: str, format: str = 'json') -> bool:
        """Export session data to file"""
        try:
            sessions = self.get_session_history(limit=1000)
            analytics = self.get_analytics(30)
            
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'preferences': asdict(self.preferences),
                'analytics': analytics,
                'sessions': sessions
            }
            
            if format.lower() == 'json':
                with open(output_path, 'w') as f:
                    json.dump(export_data, f, indent=2)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
            return True
            
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
            
    def get_recommendations(self) -> Dict:
        """Get personalized recommendations based on session history"""
        try:
            analytics = self.get_analytics(30)
            sessions = self.get_session_history(20)
            
            recommendations = []
            
            # Success rate recommendations
            if analytics.get('success_rate', 0) < 50:
                recommendations.append({
                    'type': 'success_rate',
                    'message': 'Your success rate is below 50%. Consider using more reliable methods like essence crafting.',
                    'priority': 'high'
                })
                
            # Cost efficiency recommendations
            if analytics.get('average_cost', 0) > self.preferences.default_budget * 1.5:
                recommendations.append({
                    'type': 'cost_efficiency',
                    'message': 'Your average costs exceed budget by 50%. Consider using the budget optimizer.',
                    'priority': 'medium'
                })
                
            # Method recommendations
            if analytics.get('most_used_method') == 'chaos_spam':
                recommendations.append({
                    'type': 'method_diversity',
                    'message': 'Try using alt-regal or essence methods for better cost efficiency on specific modifiers.',
                    'priority': 'low'
                })
                
            return {
                'recommendations': recommendations,
                'generated_at': datetime.now().isoformat(),
                'based_on_sessions': len(sessions)
            }
            
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return {'recommendations': [], 'error': str(e)}


# Global session tracker instance
session_tracker = SessionTracker()