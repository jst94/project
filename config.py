"""
Configuration settings for the PoE Craft Helper
Centralizes all hardcoded values for easy maintenance
"""

# UI Configuration
UI_CONFIG = {
    'window_size': '800x700',
    'default_opacity': 0.95,
    'topmost': True,
    'fonts': {
        'default': ('Arial', 9),
        'bold': ('Arial', 10, 'bold'),
        'title': ('Arial', 12, 'bold')
    }
}

# Market API Configuration
MARKET_CONFIG = {
    'price_update_interval': 300,  # 5 minutes
    'price_update_retry_interval': 60,  # 1 minute
    'cache_duration': 600,  # 10 minutes
    'api_timeout': 10,  # seconds
    'max_retries': 3,
    'base_url': 'https://poe.ninja/api/data'
}

# Default Currency Prices (fallback values in chaos orbs)
DEFAULT_PRICES = {
    'Chaos Orb': 1.0,
    'Exalted Orb': 200.0,
    'Divine Orb': 15.0,
    'Orb of Annulment': 8.0,
    'Orb of Scouring': 0.5,
    'Orb of Alteration': 0.1,
    'Orb of Augmentation': 0.5,
    'Regal Orb': 2.0,
    'Orb of Transmutation': 0.2,
    'Glassblowers Bauble': 1.0,
    'Essence': 5.0,
    'Fossil': 3.0,
    'Resonator': 2.0
}

# Crafting Configuration
CRAFTING_CONFIG = {
    'default_budget': 1000.0,
    'default_item_level': 85,
    'max_modifiers': 6,
    'max_prefixes': 3,
    'max_suffixes': 3,
    'min_item_level': 1,
    'max_item_level': 100
}

# Database Configuration
DATABASE_CONFIG = {
    'session_db_name': 'crafting_sessions.db',
    'preferences_file': 'user_preferences.json',
    'backup_interval': 3600,  # 1 hour
    'max_session_history': 1000
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'thread_pool_size': 4,
    'ui_update_interval': 100,  # milliseconds
    'background_processing_delay': 50,  # milliseconds
    'max_concurrent_api_calls': 3
}

# AI Optimizer Configuration
AI_CONFIG = {
    'confidence_threshold': 0.7,
    'max_strategies_analyzed': 10,
    'learning_rate': 0.1,
    'success_pattern_memory': 100,  # number of sessions to remember
    'strategy_weights': {
        'success_probability': 0.35,
        'cost_efficiency': 0.25,
        'time_efficiency': 0.15,
        'risk_tolerance': 0.15,
        'user_preference': 0.10
    }
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'poe_craft_helper.log',
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# League Configuration
LEAGUE_CONFIG = {
    'default_league': 'Secrets of the Atlas',
    'auto_detect_league': True,
    'league_api_mappings': {
        "Secrets of the Atlas": "Secrets",
        "Settlers of Kalguur": "Settlers", 
        "Necropolis": "Necropolis",
        "Standard": "Standard",
        "Hardcore": "Hardcore"
    }
}

# Application Metadata
APP_CONFIG = {
    'name': 'Intelligent PoE Craft Helper',
    'version': '3.26.0',
    'author': 'PoE Community',
    'description': 'AI-powered Path of Exile crafting assistant'
}