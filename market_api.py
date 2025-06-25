"""
Real-time Path of Exile Market API Integration
Provides live currency exchange rates and market data
"""

import requests
import json
import time
import threading
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import logging


class POEMarketAPI:
    """Real-time Path of Exile market data integration"""
    
    def __init__(self, league: str = "Necropolis"):
        self.league = league
        self.base_url = "https://poe.ninja/api/data"
        self.currency_data = {}
        self.essence_data = {}
        self.fossil_data = {}
        self.last_update = None
        self.update_interval = 300  # 5 minutes
        self.cache_duration = 600   # 10 minutes
        
        # Default fallback prices (in chaos orbs)
        self.fallback_prices = {
            'Chaos Orb': 1.0,
            'Exalted Orb': 200.0,
            'Divine Orb': 15.0,
            'Orb of Annulment': 8.0,
            'Orb of Scouring': 0.5,
            'Orb of Alteration': 0.1,
            'Orb of Augmentation': 0.05,
            'Regal Orb': 2.0,
            'Orb of Alchemy': 0.5,
            'Orb of Transmutation': 0.02,
            'Blessed Orb': 0.5,
            'Chromatic Orb': 0.1,
            'Orb of Jewellers': 0.1,
            'Orb of Fusing': 0.1,
            'Eternal Orb': 500.0,
            'Essence': 5.0,
            'Fossil': 3.0,
            'Resonator': 2.0
        }
        
        # Start background price updater
        self.start_background_updater()
        
    def start_background_updater(self):
        """Start background thread to update prices periodically"""
        def update_loop():
            while True:
                try:
                    self.update_all_prices()
                    time.sleep(self.update_interval)
                except Exception as e:
                    logging.error(f"Error updating prices: {e}")
                    time.sleep(60)  # Wait 1 minute on error
                    
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()
        
    def update_all_prices(self) -> bool:
        """Update all market prices from API"""
        try:
            # Update currency exchange rates
            currency_success = self.update_currency_prices()
            
            # Update essence prices
            essence_success = self.update_essence_prices()
            
            # Update fossil prices  
            fossil_success = self.update_fossil_prices()
            
            if currency_success or essence_success or fossil_success:
                self.last_update = datetime.now()
                logging.info("Market prices updated successfully")
                return True
                
        except Exception as e:
            logging.error(f"Failed to update market prices: {e}")
            
        return False
        
    def update_currency_prices(self) -> bool:
        """Fetch current currency exchange rates"""
        try:
            url = f"{self.base_url}/currencyoverview"
            params = {
                'league': self.league,
                'type': 'Currency'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Process currency data
            currency_map = {}
            for item in data.get('lines', []):
                currency_name = item.get('currencyTypeName', '')
                chaos_value = item.get('chaosEquivalent', 0)
                
                if chaos_value > 0:
                    currency_map[currency_name] = chaos_value
                    
            # Map to our currency names
            self.currency_data = {
                'Exalted Orb': currency_map.get('Exalted Orb', self.fallback_prices['Exalted Orb']),
                'Divine Orb': currency_map.get('Divine Orb', self.fallback_prices['Divine Orb']),  
                'Orb of Annulment': currency_map.get('Orb of Annulment', self.fallback_prices['Orb of Annulment']),
                'Orb of Scouring': currency_map.get('Orb of Scouring', self.fallback_prices['Orb of Scouring']),
                'Orb of Alteration': currency_map.get('Orb of Alteration', self.fallback_prices['Orb of Alteration']),
                'Orb of Augmentation': currency_map.get('Orb of Augmentation', self.fallback_prices['Orb of Augmentation']),
                'Regal Orb': currency_map.get('Regal Orb', self.fallback_prices['Regal Orb']),
                'Orb of Alchemy': currency_map.get('Orb of Alchemy', self.fallback_prices['Orb of Alchemy']),
                'Orb of Transmutation': currency_map.get('Orb of Transmutation', self.fallback_prices['Orb of Transmutation']),
                'Blessed Orb': currency_map.get('Blessed Orb', self.fallback_prices['Blessed Orb']),
                'Chromatic Orb': currency_map.get('Chromatic Orb', self.fallback_prices['Chromatic Orb']),
                'Orb of Jewellers': currency_map.get('Orb of Jewellers', self.fallback_prices['Orb of Jewellers']),
                'Orb of Fusing': currency_map.get('Orb of Fusing', self.fallback_prices['Orb of Fusing']),
                'Chaos Orb': 1.0,  # Base currency
            }
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to update currency prices: {e}")
            return False
            
    def update_essence_prices(self) -> bool:
        """Fetch current essence prices"""
        try:
            url = f"{self.base_url}/itemoverview"
            params = {
                'league': self.league,
                'type': 'Essence'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Calculate average essence price
            total_value = 0
            count = 0
            
            for item in data.get('lines', []):
                chaos_value = item.get('chaosValue', 0)
                if chaos_value > 0:
                    total_value += chaos_value
                    count += 1
                    
            if count > 0:
                self.essence_data['average_price'] = total_value / count
            else:
                self.essence_data['average_price'] = self.fallback_prices['Essence']
                
            return True
            
        except Exception as e:
            logging.error(f"Failed to update essence prices: {e}")
            return False
            
    def update_fossil_prices(self) -> bool:
        """Fetch current fossil prices"""
        try:
            url = f"{self.base_url}/itemoverview"
            params = {
                'league': self.league,
                'type': 'Fossil'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Calculate average fossil price
            total_value = 0
            count = 0
            
            for item in data.get('lines', []):
                chaos_value = item.get('chaosValue', 0)
                if chaos_value > 0:
                    total_value += chaos_value
                    count += 1
                    
            if count > 0:
                self.fossil_data['average_price'] = total_value / count
                # Resonators typically cost similar to fossils
                self.fossil_data['resonator_price'] = self.fossil_data['average_price'] * 0.7
            else:
                self.fossil_data['average_price'] = self.fallback_prices['Fossil']
                self.fossil_data['resonator_price'] = self.fallback_prices['Resonator']
                
            return True
            
        except Exception as e:
            logging.error(f"Failed to update fossil prices: {e}")
            return False
            
    def get_currency_price(self, currency_name: str) -> float:
        """Get current price for a specific currency"""
        # Check if data is fresh
        if self.is_data_stale():
            self.update_all_prices()
            
        # Return live price if available
        if currency_name in self.currency_data:
            return self.currency_data[currency_name]
            
        # Handle special cases
        if currency_name == 'Essence':
            return self.essence_data.get('average_price', self.fallback_prices['Essence'])
        elif currency_name == 'Fossil':
            return self.fossil_data.get('average_price', self.fallback_prices['Fossil'])
        elif currency_name == 'Resonator':
            return self.fossil_data.get('resonator_price', self.fallback_prices['Resonator'])
            
        # Return fallback price
        return self.fallback_prices.get(currency_name, 1.0)
        
    def get_all_currency_prices(self) -> Dict[str, float]:
        """Get all current currency prices"""
        prices = {}
        
        for currency in self.fallback_prices.keys():
            prices[currency] = self.get_currency_price(currency)
            
        return prices
        
    def is_data_stale(self) -> bool:
        """Check if cached data is stale"""
        if self.last_update is None:
            return True
            
        return datetime.now() - self.last_update > timedelta(seconds=self.cache_duration)
        
    def get_market_trend(self, currency_name: str, days: int = 7) -> Dict:
        """Get price trend for a currency (placeholder for future implementation)"""
        # This would require storing historical data
        return {
            'currency': currency_name,
            'current_price': self.get_currency_price(currency_name),
            'trend': 'stable',  # 'rising', 'falling', 'stable'
            'change_percent': 0.0,
            'days': days
        }
        
    def get_api_status(self) -> Dict:
        """Get API connection status and last update info"""
        return {
            'connected': self.last_update is not None,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'data_age_seconds': (datetime.now() - self.last_update).total_seconds() if self.last_update else None,
            'is_stale': self.is_data_stale(),
            'league': self.league
        }


class DynamicPriceOptimizer:
    """Dynamic cost optimization and budget planning"""
    
    def __init__(self, market_api: POEMarketAPI):
        self.market_api = market_api
        
    def optimize_crafting_budget(self, target_modifiers: List[str], base_budget: float) -> Dict:
        """Optimize crafting budget allocation based on current market prices"""
        current_prices = self.market_api.get_all_currency_prices()
        
        # Calculate optimal currency allocation
        allocation = {}
        remaining_budget = base_budget
        
        # Prioritize by cost efficiency
        currency_efficiency = {}
        for currency, price in current_prices.items():
            if currency == 'Chaos Orb':
                continue
            # Simple efficiency metric (lower is better)
            currency_efficiency[currency] = price
            
        # Sort by efficiency (cheapest first for high-volume currencies)
        sorted_currencies = sorted(currency_efficiency.items(), key=lambda x: x[1])
        
        for currency, price in sorted_currencies:
            if remaining_budget <= 0:
                break
                
            # Allocate percentage of budget based on currency type
            if currency in ['Orb of Alteration', 'Orb of Augmentation', 'Orb of Transmutation']:
                # High-volume currencies get larger allocation
                allocation_percent = 0.3
            elif currency in ['Regal Orb', 'Orb of Alchemy', 'Orb of Scouring']:
                # Medium-volume currencies
                allocation_percent = 0.2
            else:
                # Low-volume, high-value currencies
                allocation_percent = 0.1
                
            allocation_amount = min(remaining_budget * allocation_percent, remaining_budget)
            allocation[currency] = {
                'chaos_allocated': allocation_amount,
                'currency_amount': allocation_amount / price,
                'price_per_unit': price
            }
            remaining_budget -= allocation_amount
            
        return {
            'total_budget': base_budget,
            'allocation': allocation,
            'remaining_budget': remaining_budget,
            'optimization_timestamp': datetime.now().isoformat()
        }
        
    def calculate_method_cost_efficiency(self, crafting_methods: List[Dict]) -> List[Dict]:
        """Calculate cost efficiency for different crafting methods"""
        current_prices = self.market_api.get_all_currency_prices()
        
        for method in crafting_methods:
            total_cost = 0
            for currency, amount in method.get('currency_requirements', {}).items():
                currency_price = current_prices.get(currency, 1.0)
                total_cost += amount * currency_price
                
            method['current_total_cost'] = total_cost
            method['cost_efficiency'] = method.get('success_probability', 0.1) / max(total_cost, 0.1)
            method['price_timestamp'] = datetime.now().isoformat()
            
        # Sort by cost efficiency (higher is better)
        return sorted(crafting_methods, key=lambda x: x.get('cost_efficiency', 0), reverse=True)


# Global market API instance
poe_market = POEMarketAPI()
price_optimizer = DynamicPriceOptimizer(poe_market)