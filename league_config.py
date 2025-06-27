"""
Centralized League Configuration System
Manages current league settings across all components
"""

from typing import Optional
import json
import os
import logging
from dataclasses import dataclass


@dataclass
class LeagueConfig:
    """Configuration for current league"""
    name: str
    display_name: str
    api_name: str
    is_current: bool = True
    
    
class LeagueManager:
    """Centralized league configuration management"""
    
    # Known league mappings
    LEAGUE_MAPPINGS = {
        "Secrets of the Atlas": {
            "display_name": "Secrets of the Atlas",
            "api_name": "Secrets"
        },
        "Settlers of Kalguur": {
            "display_name": "Settlers of Kalguur",
            "api_name": "Settlers"
        },
        "Settlers": {
            "display_name": "Settlers of Kalguur", 
            "api_name": "Settlers"
        },
        "Necropolis": {
            "display_name": "Necropolis",
            "api_name": "Necropolis"
        },
        "Standard": {
            "display_name": "Standard",
            "api_name": "Standard"
        },
        "Hardcore": {
            "display_name": "Hardcore",
            "api_name": "Hardcore"
        }
    }
    
    def __init__(self, preferences_path: str = "data/user_preferences.json"):
        self.preferences_path = preferences_path
        self._current_league = None
        
    def get_current_league(self) -> LeagueConfig:
        """Get current league configuration"""
        if self._current_league is None:
            self._load_league_from_preferences()
        return self._current_league
        
    def _load_league_from_preferences(self):
        """Load league from user preferences"""
        league_name = self._get_league_from_file()
        
        # Normalize league name
        if league_name in self.LEAGUE_MAPPINGS:
            mapping = self.LEAGUE_MAPPINGS[league_name]
            self._current_league = LeagueConfig(
                name=league_name,
                display_name=mapping["display_name"],
                api_name=mapping["api_name"]
            )
        else:
            # Fallback for unknown leagues
            self._current_league = LeagueConfig(
                name=league_name,
                display_name=league_name,
                api_name=league_name
            )
    
    def _get_league_from_file(self) -> str:
        """Get league name from preferences file"""
        try:
            if os.path.exists(self.preferences_path):
                with open(self.preferences_path, 'r') as f:
                    data = json.load(f)
                    return data.get('league_name', 'Settlers of Kalguur')
        except Exception as e:
            logging.error(f"Error loading league from preferences: {e}")
        
        return 'Settlers of Kalguur'  # Default fallback
    
    def get_display_name(self) -> str:
        """Get formatted display name for UI"""
        return self.get_current_league().display_name
        
    def get_api_name(self) -> str:
        """Get name for API calls"""
        return self.get_current_league().api_name
        
    def refresh(self):
        """Force refresh league configuration"""
        self._current_league = None
        self._load_league_from_preferences()
        

# Global league manager instance
league_manager = LeagueManager()


def get_current_league_name() -> str:
    """Convenience function to get current league display name"""
    return league_manager.get_display_name()


def get_current_league_api_name() -> str:
    """Convenience function to get current league API name"""
    return league_manager.get_api_name()


def refresh_league_config():
    """Convenience function to refresh league configuration"""
    league_manager.refresh()