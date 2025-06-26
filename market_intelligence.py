"""
Market Intelligence System with Trend Analysis and Price Prediction
Advanced market data analysis with predictive modeling for PoE economy
"""

import numpy as np
import json
import time
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import sqlite3
import os
import requests

# Try to import scipy, fall back to basic stats if not available
try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("scipy not available - using basic statistical methods")


@dataclass
class PriceDataPoint:
    """Single price data point"""
    currency: str
    price: float
    timestamp: str
    confidence: float
    volume: Optional[int] = None
    league: str = "Standard"


@dataclass
class MarketTrend:
    """Market trend analysis result"""
    currency: str
    trend_direction: str  # 'rising', 'falling', 'stable', 'volatile'
    trend_strength: float  # 0-1 scale
    price_change_24h: float
    price_change_7d: float
    volatility_score: float
    predicted_price_24h: float
    prediction_confidence: float
    volume_trend: str
    seasonal_pattern: Optional[str] = None


@dataclass
class MarketForecast:
    """Market forecast for planning purposes"""
    timeframe: str  # '1h', '6h', '24h', '7d'
    currency_forecasts: Dict[str, float]
    market_conditions: str  # 'bullish', 'bearish', 'neutral', 'uncertain'
    risk_factors: List[str]
    opportunity_score: float
    generated_at: str


class MarketIntelligenceSystem:
    """Advanced market intelligence with trend analysis and price prediction"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.market_db_path = os.path.join(data_dir, "market_intelligence.db")
        
        # Price history storage (in-memory for fast access)
        self.price_history = defaultdict(lambda: deque(maxlen=1000))
        self.trend_cache = {}
        self.forecast_cache = {}
        
        # Market analysis parameters
        self.trend_window_short = 24  # hours
        self.trend_window_long = 168  # 7 days
        self.volatility_threshold = 0.15
        self.trend_strength_threshold = 0.1
        
        # Prediction models
        self.price_models = {}
        self.seasonal_patterns = {}
        
        # Market event tracking
        self.market_events = deque(maxlen=100)
        
        # Currency importance weights for market impact
        self.currency_importance = {
            'Divine Orb': 1.0,
            'Exalted Orb': 0.9,
            'Chaos Orb': 0.8,
            'Orb of Annulment': 0.7,
            'Orb of Scouring': 0.5,
            'Orb of Alteration': 0.4,
            'Regal Orb': 0.6,
            'Essence': 0.5,
            'Fossil': 0.4
        }
        
        # Initialize database
        self.init_market_database()
        
        # Load historical data
        self.load_market_data()
        
        # Start background market monitoring
        self.start_market_monitoring()
    
    def init_market_database(self):
        """Initialize market intelligence database"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        with sqlite3.connect(self.market_db_path) as conn:
            cursor = conn.cursor()
            
            # Price history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    currency TEXT NOT NULL,
                    price REAL NOT NULL,
                    timestamp TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    volume INTEGER,
                    league TEXT DEFAULT 'Standard',
                    source TEXT DEFAULT 'poe.ninja'
                )
            ''')
            
            # Market trends table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS market_trends (
                    currency TEXT NOT NULL,
                    trend_direction TEXT NOT NULL,
                    trend_strength REAL NOT NULL,
                    price_change_24h REAL NOT NULL,
                    price_change_7d REAL NOT NULL,
                    volatility_score REAL NOT NULL,
                    predicted_price_24h REAL NOT NULL,
                    prediction_confidence REAL NOT NULL,
                    volume_trend TEXT,
                    timestamp TEXT NOT NULL,
                    PRIMARY KEY (currency, timestamp)
                )
            ''')
            
            # Market events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS market_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    impact_score REAL NOT NULL,
                    affected_currencies TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            # Seasonal patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS seasonal_patterns (
                    currency TEXT NOT NULL,
                    pattern_type TEXT NOT NULL,
                    pattern_data TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    last_updated TEXT NOT NULL,
                    PRIMARY KEY (currency, pattern_type)
                )
            ''')
            
            conn.commit()
    
    def record_price_data(self, currency: str, price: float, confidence: float = 1.0, 
                         volume: Optional[int] = None, league: str = "Standard"):
        """Record new price data point"""
        timestamp = datetime.now().isoformat()
        
        # Store in memory
        data_point = PriceDataPoint(currency, price, timestamp, confidence, volume, league)
        self.price_history[currency].append(data_point)
        
        # Store in database
        with sqlite3.connect(self.market_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO price_history 
                (currency, price, timestamp, confidence, volume, league)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (currency, price, timestamp, confidence, volume, league))
            conn.commit()
        
        # Trigger trend analysis if enough data
        if len(self.price_history[currency]) >= 10:
            self.analyze_currency_trend(currency)
    
    def analyze_currency_trend(self, currency: str) -> MarketTrend:
        """Analyze trend for a specific currency"""
        history = list(self.price_history[currency])
        
        if len(history) < 5:
            return self._create_default_trend(currency)
        
        # Extract price arrays
        prices = np.array([p.price for p in history])
        timestamps = [datetime.fromisoformat(p.timestamp) for p in history]
        
        # Calculate time-based changes
        now = datetime.now()
        
        # 24h change
        prices_24h = [p.price for p in history if (now - datetime.fromisoformat(p.timestamp)).total_seconds() <= 86400]
        change_24h = ((prices[-1] - prices_24h[0]) / prices_24h[0] * 100) if len(prices_24h) >= 2 else 0
        
        # 7d change
        prices_7d = [p.price for p in history if (now - datetime.fromisoformat(p.timestamp)).total_seconds() <= 604800]
        change_7d = ((prices[-1] - prices_7d[0]) / prices_7d[0] * 100) if len(prices_7d) >= 2 else 0
        
        # Volatility calculation
        if len(prices) >= 10:
            returns = np.diff(np.log(prices))
            volatility = np.std(returns) * np.sqrt(24)  # Annualized volatility
        else:
            volatility = 0.1
        
        # Trend direction and strength
        if len(prices) >= 5:
            x = np.arange(len(prices))
            
            if SCIPY_AVAILABLE:
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, prices)
                trend_strength = abs(r_value)
                p_threshold = 0.05
            else:
                # Basic linear regression fallback
                slope, r_value = self._basic_linear_regression(x, prices)
                trend_strength = abs(r_value)
                p_threshold = 0.1  # More lenient without proper p-value
                p_value = 0.01  # Assume significant for basic implementation
            
            if slope > self.trend_strength_threshold and p_value < p_threshold:
                trend_direction = 'rising'
            elif slope < -self.trend_strength_threshold and p_value < p_threshold:
                trend_direction = 'falling'
            elif volatility > self.volatility_threshold:
                trend_direction = 'volatile'
            else:
                trend_direction = 'stable'
        else:
            trend_direction = 'stable'
            trend_strength = 0.0
        
        # Price prediction using simple linear extrapolation + seasonal adjustment
        predicted_price = self._predict_next_price(currency, prices, timestamps)
        prediction_confidence = min(0.95, trend_strength * 0.8 + (1 - volatility) * 0.2)
        
        # Volume trend (simplified)
        volume_trend = 'unknown'
        volumes = [p.volume for p in history if p.volume is not None]
        if len(volumes) >= 5:
            recent_volume = np.mean(volumes[-5:])
            older_volume = np.mean(volumes[-10:-5]) if len(volumes) >= 10 else recent_volume
            
            if recent_volume > older_volume * 1.2:
                volume_trend = 'increasing'
            elif recent_volume < older_volume * 0.8:
                volume_trend = 'decreasing'
            else:
                volume_trend = 'stable'
        
        # Seasonal pattern detection
        seasonal_pattern = self._detect_seasonal_pattern(currency, history)
        
        trend = MarketTrend(
            currency=currency,
            trend_direction=trend_direction,
            trend_strength=trend_strength,
            price_change_24h=change_24h,
            price_change_7d=change_7d,
            volatility_score=volatility,
            predicted_price_24h=predicted_price,
            prediction_confidence=prediction_confidence,
            volume_trend=volume_trend,
            seasonal_pattern=seasonal_pattern
        )
        
        # Cache the trend
        self.trend_cache[currency] = trend
        
        # Store in database
        self._save_trend_to_db(trend)
        
        return trend
    
    def _basic_linear_regression(self, x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
        """Basic linear regression implementation when scipy is not available"""
        n = len(x)
        if n < 2:
            return 0.0, 0.0
        
        # Calculate means
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        
        # Calculate slope
        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sum((x - x_mean) ** 2)
        
        if denominator == 0:
            return 0.0, 0.0
        
        slope = numerator / denominator
        
        # Calculate correlation coefficient
        x_std = np.std(x)
        y_std = np.std(y)
        
        if x_std == 0 or y_std == 0:
            r_value = 0.0
        else:
            r_value = numerator / (np.sqrt(denominator) * np.sqrt(np.sum((y - y_mean) ** 2)))
        
        return slope, r_value
    
    def _predict_next_price(self, currency: str, prices: np.ndarray, timestamps: List[datetime]) -> float:
        """Predict next price using multiple models"""
        if len(prices) < 3:
            return prices[-1] if len(prices) > 0 else 1.0
        
        # Model 1: Linear trend extrapolation
        x = np.arange(len(prices))
        if SCIPY_AVAILABLE:
            slope, intercept, r_value, _, _ = stats.linregress(x, prices)
            linear_pred = slope * len(prices) + intercept
        else:
            slope, r_value = self._basic_linear_regression(x, prices)
            # Calculate intercept manually
            x_mean = np.mean(x)
            y_mean = np.mean(prices)
            intercept = y_mean - slope * x_mean
            linear_pred = slope * len(prices) + intercept
        
        # Model 2: Exponential moving average
        alpha = 0.3
        ema = prices[0]
        for price in prices[1:]:
            ema = alpha * price + (1 - alpha) * ema
        ema_pred = ema
        
        # Model 3: Mean reversion
        mean_price = np.mean(prices[-20:]) if len(prices) >= 20 else np.mean(prices)
        current_price = prices[-1]
        reversion_factor = 0.1
        mean_reversion_pred = current_price + reversion_factor * (mean_price - current_price)
        
        # Model 4: Seasonal adjustment
        seasonal_adj = self._get_seasonal_adjustment(currency, timestamps[-1])
        
        # Weighted combination of models
        weights = [0.4, 0.3, 0.2, 0.1]  # Linear, EMA, Mean Reversion, Seasonal
        predictions = [linear_pred, ema_pred, mean_reversion_pred, current_price * (1 + seasonal_adj)]
        
        final_prediction = np.average(predictions, weights=weights)
        
        # Sanity check - limit extreme predictions
        max_change = 0.5  # 50% max change
        final_prediction = max(current_price * (1 - max_change), 
                             min(current_price * (1 + max_change), final_prediction))
        
        return max(0.001, final_prediction)  # Ensure positive price
    
    def _detect_seasonal_pattern(self, currency: str, history: List[PriceDataPoint]) -> Optional[str]:
        """Detect seasonal patterns in price data"""
        if len(history) < 50:  # Need substantial data for pattern detection
            return None
        
        # Extract hourly patterns
        hourly_prices = defaultdict(list)
        daily_prices = defaultdict(list)
        
        for data_point in history:
            dt = datetime.fromisoformat(data_point.timestamp)
            hourly_prices[dt.hour].append(data_point.price)
            daily_prices[dt.weekday()].append(data_point.price)
        
        # Analyze hourly patterns
        hourly_avg = {hour: np.mean(prices) for hour, prices in hourly_prices.items() if len(prices) >= 3}
        if len(hourly_avg) >= 12:  # At least half day coverage
            max_hour = max(hourly_avg, key=hourly_avg.get)
            min_hour = min(hourly_avg, key=hourly_avg.get)
            
            if hourly_avg[max_hour] > hourly_avg[min_hour] * 1.1:  # 10% difference
                return f"daily_peak_hour_{max_hour}"
        
        # Analyze weekly patterns
        daily_avg = {day: np.mean(prices) for day, prices in daily_prices.items() if len(prices) >= 3}
        if len(daily_avg) >= 5:  # Most days covered
            weekend_avg = np.mean([daily_avg.get(5, 0), daily_avg.get(6, 0)])
            weekday_avg = np.mean([daily_avg.get(i, 0) for i in range(5)])
            
            if weekend_avg > weekday_avg * 1.05:
                return "weekend_premium"
            elif weekday_avg > weekend_avg * 1.05:
                return "weekday_premium"
        
        return None
    
    def _get_seasonal_adjustment(self, currency: str, timestamp: datetime) -> float:
        """Get seasonal adjustment factor for prediction"""
        pattern = self.seasonal_patterns.get(currency)
        if not pattern:
            return 0.0
        
        # Simple hourly adjustment
        if pattern.startswith('daily_peak_hour_'):
            peak_hour = int(pattern.split('_')[-1])
            current_hour = timestamp.hour
            
            # Higher prices expected near peak hour
            hour_diff = min(abs(current_hour - peak_hour), 24 - abs(current_hour - peak_hour))
            if hour_diff <= 2:
                return 0.02  # 2% increase near peak
            elif hour_diff >= 10:
                return -0.02  # 2% decrease far from peak
        
        # Weekly pattern adjustment
        elif pattern == "weekend_premium":
            if timestamp.weekday() >= 5:  # Weekend
                return 0.03  # 3% weekend premium
            else:
                return -0.01  # Slight weekday discount
        
        elif pattern == "weekday_premium":
            if timestamp.weekday() < 5:  # Weekday
                return 0.02  # 2% weekday premium
            else:
                return -0.02  # Weekend discount
        
        return 0.0
    
    def generate_market_forecast(self, timeframe: str = '24h') -> MarketForecast:
        """Generate comprehensive market forecast"""
        
        # Analyze all currencies
        currency_forecasts = {}
        risk_factors = []
        opportunity_indicators = []
        
        for currency in self.currency_importance.keys():
            if currency in self.trend_cache:
                trend = self.trend_cache[currency]
                currency_forecasts[currency] = trend.predicted_price_24h
                
                # Identify risk factors
                if trend.volatility_score > 0.2:
                    risk_factors.append(f"High volatility in {currency}")
                
                if abs(trend.price_change_24h) > 10:
                    risk_factors.append(f"Rapid price movement in {currency} ({trend.price_change_24h:+.1f}%)")
                
                # Identify opportunities
                if trend.trend_direction == 'rising' and trend.trend_strength > 0.7:
                    opportunity_indicators.append(f"Strong uptrend in {currency}")
                elif trend.trend_direction == 'falling' and trend.trend_strength > 0.7:
                    opportunity_indicators.append(f"Potential buying opportunity in {currency}")
        
        # Calculate overall market conditions
        market_sentiment_score = self._calculate_market_sentiment()
        
        if market_sentiment_score > 0.6:
            market_conditions = 'bullish'
        elif market_sentiment_score < 0.4:
            market_conditions = 'bearish'
        elif len(risk_factors) > 3:
            market_conditions = 'uncertain'
        else:
            market_conditions = 'neutral'
        
        # Calculate opportunity score
        opportunity_score = len(opportunity_indicators) / max(len(currency_forecasts), 1)
        opportunity_score = min(1.0, opportunity_score + (market_sentiment_score - 0.5))
        
        forecast = MarketForecast(
            timeframe=timeframe,
            currency_forecasts=currency_forecasts,
            market_conditions=market_conditions,
            risk_factors=risk_factors[:5],  # Top 5 risks
            opportunity_score=opportunity_score,
            generated_at=datetime.now().isoformat()
        )
        
        # Cache forecast
        self.forecast_cache[timeframe] = forecast
        
        return forecast
    
    def _calculate_market_sentiment(self) -> float:
        """Calculate overall market sentiment score (0-1)"""
        sentiment_scores = []
        
        for currency, importance in self.currency_importance.items():
            if currency in self.trend_cache:
                trend = self.trend_cache[currency]
                
                # Score based on trend direction and strength
                if trend.trend_direction == 'rising':
                    score = 0.7 + trend.trend_strength * 0.3
                elif trend.trend_direction == 'falling':
                    score = 0.3 - trend.trend_strength * 0.3
                elif trend.trend_direction == 'volatile':
                    score = 0.4  # Neutral but uncertain
                else:  # stable
                    score = 0.5
                
                # Adjust for volatility (high volatility reduces sentiment)
                score *= (1 - trend.volatility_score * 0.3)
                
                # Weight by currency importance
                sentiment_scores.append(score * importance)
        
        return np.mean(sentiment_scores) if sentiment_scores else 0.5
    
    def get_crafting_market_insights(self, target_modifiers: List[str], 
                                   crafting_method: str, budget: float) -> Dict[str, Any]:
        """Get market insights specific to crafting scenario"""
        
        # Map modifiers to relevant currencies
        modifier_currency_map = {
            'Maximum Life': ['Essence', 'Chaos Orb'],
            'Maximum Energy Shield': ['Essence', 'Chaos Orb'],
            'Attack Speed': ['Fossil', 'Chaos Orb'],
            'Critical Strike Chance': ['Fossil', 'Chaos Orb'],
            'Resistance': ['Essence', 'Chaos Orb']
        }
        
        method_currency_map = {
            'chaos_spam': ['Chaos Orb', 'Divine Orb', 'Orb of Annulment'],
            'alt_regal': ['Orb of Alteration', 'Regal Orb', 'Exalted Orb'],
            'essence': ['Essence', 'Chaos Orb', 'Orb of Annulment'],
            'fossil': ['Fossil', 'Chaos Orb']
        }
        
        # Get relevant currencies
        relevant_currencies = set(method_currency_map.get(crafting_method, ['Chaos Orb']))
        for modifier in target_modifiers:
            relevant_currencies.update(modifier_currency_map.get(modifier, ['Chaos Orb']))
        
        # Analyze trends for relevant currencies
        currency_analysis = {}
        total_cost_trend = 0
        market_timing_score = 0
        
        for currency in relevant_currencies:
            if currency in self.trend_cache:
                trend = self.trend_cache[currency]
                currency_analysis[currency] = {
                    'current_trend': trend.trend_direction,
                    'price_change_24h': trend.price_change_24h,
                    'predicted_change': ((trend.predicted_price_24h / self.get_latest_price(currency)) - 1) * 100,
                    'volatility': trend.volatility_score,
                    'recommendation': self._get_currency_recommendation(trend)
                }
                
                # Calculate cost trend impact
                importance = self.currency_importance.get(currency, 0.5)
                if trend.trend_direction == 'rising':
                    total_cost_trend += importance * trend.trend_strength
                elif trend.trend_direction == 'falling':
                    total_cost_trend -= importance * trend.trend_strength
                
                # Market timing score
                if trend.trend_direction == 'falling' and trend.trend_strength > 0.5:
                    market_timing_score += importance  # Good time to buy
                elif trend.trend_direction == 'rising' and trend.trend_strength > 0.5:
                    market_timing_score -= importance * 0.5  # Bad time to buy
        
        # Generate recommendations
        recommendations = []
        
        if total_cost_trend > 0.3:
            recommendations.append("Currency costs are trending upward - consider crafting soon")
        elif total_cost_trend < -0.3:
            recommendations.append("Currency costs are falling - you might wait for better prices")
        
        if market_timing_score > 0.5:
            recommendations.append("Market conditions favor crafting now")
        elif market_timing_score < -0.5:
            recommendations.append("Consider delaying crafting due to high currency prices")
        
        # Budget adequacy analysis
        forecast = self.forecast_cache.get('24h') or self.generate_market_forecast('24h')
        budget_buffer = 1.0
        
        for currency in relevant_currencies:
            if currency in forecast.currency_forecasts:
                predicted_price = forecast.currency_forecasts[currency]
                current_price = self.get_latest_price(currency)
                price_increase = (predicted_price / current_price) - 1
                budget_buffer *= (1 + price_increase)
        
        if budget_buffer > 1.1:
            recommendations.append(f"Consider increasing budget by {(budget_buffer-1)*100:.1f}% due to price trends")
        
        return {
            'currency_analysis': currency_analysis,
            'market_timing_score': market_timing_score,
            'cost_trend_direction': 'increasing' if total_cost_trend > 0.1 else 'decreasing' if total_cost_trend < -0.1 else 'stable',
            'recommended_budget_multiplier': budget_buffer,
            'recommendations': recommendations,
            'market_conditions': forecast.market_conditions,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _get_currency_recommendation(self, trend: MarketTrend) -> str:
        """Get specific recommendation for a currency based on its trend"""
        if trend.trend_direction == 'rising' and trend.trend_strength > 0.6:
            return "Buy soon - price increasing"
        elif trend.trend_direction == 'falling' and trend.trend_strength > 0.6:
            return "Wait - price decreasing"
        elif trend.trend_direction == 'volatile':
            return "Monitor closely - high volatility"
        else:
            return "Neutral - stable pricing"
    
    def get_latest_price(self, currency: str) -> float:
        """Get latest price for a currency"""
        if currency in self.price_history and self.price_history[currency]:
            return self.price_history[currency][-1].price
        return 1.0  # Default fallback
    
    def start_market_monitoring(self):
        """Start background market data collection"""
        import threading
        
        def monitor_loop():
            while True:
                try:
                    # This would integrate with actual market APIs
                    # For now, simulate price updates
                    self._simulate_market_data_update()
                    time.sleep(300)  # Update every 5 minutes
                except Exception as e:
                    print(f"Market monitoring error: {e}")
                    time.sleep(60)
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
    
    def _simulate_market_data_update(self):
        """Simulate market data updates (placeholder for real API integration)"""
        # This would be replaced with actual poe.ninja API calls
        for currency in self.currency_importance.keys():
            if currency in self.price_history and self.price_history[currency]:
                last_price = self.price_history[currency][-1].price
                # Simulate small price changes
                change = np.random.normal(0, 0.02)  # 2% volatility
                new_price = max(0.001, last_price * (1 + change))
                self.record_price_data(currency, new_price, confidence=0.8)
    
    def _create_default_trend(self, currency: str) -> MarketTrend:
        """Create default trend for currencies with insufficient data"""
        return MarketTrend(
            currency=currency,
            trend_direction='stable',
            trend_strength=0.0,
            price_change_24h=0.0,
            price_change_7d=0.0,
            volatility_score=0.1,
            predicted_price_24h=self.get_latest_price(currency),
            prediction_confidence=0.3,
            volume_trend='unknown'
        )
    
    def _save_trend_to_db(self, trend: MarketTrend):
        """Save trend analysis to database"""
        with sqlite3.connect(self.market_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO market_trends VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                trend.currency,
                trend.trend_direction,
                trend.trend_strength,
                trend.price_change_24h,
                trend.price_change_7d,
                trend.volatility_score,
                trend.predicted_price_24h,
                trend.prediction_confidence,
                trend.volume_trend,
                datetime.now().isoformat()
            ))
            conn.commit()
    
    def load_market_data(self):
        """Load historical market data from database"""
        try:
            with sqlite3.connect(self.market_db_path) as conn:
                cursor = conn.cursor()
                
                # Load recent price history
                cursor.execute('''
                    SELECT currency, price, timestamp, confidence, volume, league
                    FROM price_history 
                    WHERE timestamp > datetime('now', '-7 days')
                    ORDER BY timestamp
                ''')
                
                for row in cursor.fetchall():
                    currency, price, timestamp, confidence, volume, league = row
                    data_point = PriceDataPoint(currency, price, timestamp, confidence, volume, league)
                    self.price_history[currency].append(data_point)
                
                # Load seasonal patterns
                cursor.execute('SELECT currency, pattern_type, pattern_data FROM seasonal_patterns')
                for row in cursor.fetchall():
                    currency, pattern_type, pattern_data = row
                    self.seasonal_patterns[currency] = pattern_type
                    
        except Exception as e:
            print(f"Error loading market data: {e}")
    
    def export_market_intelligence(self, file_path: str):
        """Export market intelligence data"""
        intelligence_data = {
            'trends': {currency: asdict(trend) for currency, trend in self.trend_cache.items()},
            'forecasts': {tf: asdict(forecast) for tf, forecast in self.forecast_cache.items()},
            'seasonal_patterns': self.seasonal_patterns,
            'market_events': list(self.market_events),
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(file_path, 'w') as f:
            json.dump(intelligence_data, f, indent=2)


# Global market intelligence instance
market_intelligence = MarketIntelligenceSystem()