import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
import random
import threading
import time
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from market_api import poe_market, price_optimizer
from ocr_analyzer import ItemDetectionGUI
from session_tracker import session_tracker
from performance_optimizer import initialize_performance_optimizer, optimize_tkinter_performance
from ai_crafting_optimizer import ai_optimizer, CraftingScenario
from intelligent_ocr import intelligent_ocr
from probability_engine import probability_engine
from market_intelligence import market_intelligence
from enhanced_modifier_database import enhanced_modifier_db
from intelligent_recommendations import intelligent_recommendations
from adaptive_learning_system import learning_system
from realtime_strategy_optimizer import realtime_optimizer
from league_config import get_current_league_name
from config import UI_CONFIG, CRAFTING_CONFIG, APP_CONFIG

class IntelligentPOECraftHelper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_CONFIG['name']} - {get_current_league_name()}")
        self.root.geometry(UI_CONFIG['window_size'])
        self.root.attributes('-topmost', UI_CONFIG['topmost'])
        self.root.attributes('-alpha', UI_CONFIG['default_opacity'])
        
        # Comprehensive modifier database
        self.modifier_database = self.load_modifier_database()
        
        # Dynamic currency costs (updated from market API)
        self.market_api = poe_market
        self.price_optimizer = price_optimizer
        self.currency_costs = self.market_api.get_all_currency_prices()
        self.last_price_update = datetime.now()
        
        # Start price update timer
        self.start_price_updater()
        
        # Initialize OCR functionality
        self.item_detection = ItemDetectionGUI(self)
        self.intelligent_ocr = intelligent_ocr
        
        # Initialize AI optimizer
        self.ai_optimizer = ai_optimizer
        
        # Initialize probability engine
        self.probability_engine = probability_engine
        
        # Initialize advanced intelligence systems
        self.market_intelligence = market_intelligence
        self.enhanced_modifier_db = enhanced_modifier_db
        self.intelligent_recommendations = intelligent_recommendations
        self.learning_system = learning_system
        self.realtime_optimizer = realtime_optimizer
        
        # Set up system dependencies
        self._setup_system_dependencies()
        
        # Initialize session tracking
        self.session_tracker = session_tracker
        self.current_session_id = None
        
        # Load user preferences
        self.load_user_preferences()
        
        # Initialize performance optimization
        optimize_tkinter_performance(self.root)
        self.performance_optimizer = initialize_performance_optimizer(self)
        
        self.setup_ui()
    
    def start_price_updater(self):
        """Start background price updater for real-time market data"""
        def update_prices():
            while True:
                try:
                    # Update currency prices every 5 minutes
                    self.currency_costs = self.market_api.get_all_currency_prices()
                    self.last_price_update = datetime.now()
                    
                    # Update UI status if needed
                    self.root.after(0, self.update_price_status)
                    
                    time.sleep(300)  # 5 minutes
                except Exception as e:
                    print(f"Price update error: {e}")
                    time.sleep(60)  # Retry in 1 minute on error
                    
        thread = threading.Thread(target=update_prices, daemon=True)
        thread.start()
    
    def update_price_status(self):
        """Update price status in UI"""
        if hasattr(self, 'status_label'):
            api_status = self.market_api.get_api_status()
            if api_status['connected']:
                status_text = f"Market: Live • Updated: {self.last_price_update.strftime('%H:%M')}"
                self.status_label.config(text=status_text, fg='green')
            else:
                self.status_label.config(text="Market: Offline • Using fallback prices", fg='orange')
        
    def load_modifier_database(self) -> Dict:
        """Load comprehensive modifier database with enhanced recognition patterns"""
        return {
            # Life modifiers
            'Maximum Life': {
                'type': 'prefix',
                'tiers': [
                    {'name': 'T1', 'value': '+100 to +120', 'weight': 100, 'ilvl': 85},
                    {'name': 'T2', 'value': '+80 to +99', 'weight': 200, 'ilvl': 70},
                    {'name': 'T3', 'value': '+60 to +79', 'weight': 400, 'ilvl': 50},
                    {'name': 'T4', 'value': '+40 to +59', 'weight': 800, 'ilvl': 30},
                    {'name': 'T5', 'value': '+20 to +39', 'weight': 1600, 'ilvl': 1}
                ],
                'methods': ['chaos_spam', 'essence', 'fossil', 'alt_regal'],
                'essence': 'Essence of Life',
                'fossils': ['Prismatic Fossil']
            },
            
            # ES modifiers
            'Maximum Energy Shield': {
                'type': 'prefix',
                'tiers': [
                    {'name': 'T1', 'value': '+100 to +120', 'weight': 100, 'ilvl': 85},
                    {'name': 'T2', 'value': '+80 to +99', 'weight': 200, 'ilvl': 70},
                    {'name': 'T3', 'value': '+60 to +79', 'weight': 400, 'ilvl': 50},
                    {'name': 'T4', 'value': '+40 to +59', 'weight': 800, 'ilvl': 30},
                    {'name': 'T5', 'value': '+20 to +39', 'weight': 1600, 'ilvl': 1}
                ],
                'methods': ['chaos_spam', 'essence', 'fossil', 'alt_regal'],
                'essence': 'Essence of Woe',
                'fossils': ['Dense Fossil']
            },
            
            # Attack Speed
            'Attack Speed': {
                'type': 'suffix',
                'aliases': ['increased attack speed', 'attack speed increased', 'AS', 'ias', 'increased ias', 'attack speed %', '% attack speed', 'local attack speed', 'weapon attack speed'],
                'patterns': [r'attack\s*speed', r'\+\d+%?\s*attack\s*speed', r'increased\s*attack\s*speed', r'\bias\b', r'ias\s*\+?\d*%?'],
                'tiers': [
                    {'name': 'T1', 'value': '+15% to +17%', 'weight': 100, 'ilvl': 85},
                    {'name': 'T2', 'value': '+12% to +14%', 'weight': 200, 'ilvl': 70},
                    {'name': 'T3', 'value': '+9% to +11%', 'weight': 400, 'ilvl': 50},
                    {'name': 'T4', 'value': '+6% to +8%', 'weight': 800, 'ilvl': 30},
                    {'name': 'T5', 'value': '+3% to +5%', 'weight': 1600, 'ilvl': 1}
                ],
                'methods': ['chaos_spam', 'essence', 'fossil', 'alt_regal'],
                'essence': 'Essence of Speed',
                'fossils': ['Serrated Fossil']
            },
            
            # Critical Strike Chance
            'Critical Strike Chance': {
                'type': 'suffix',
                'aliases': ['critical strike chance', 'crit chance', 'critical chance', 'crit', 'increased critical strike chance', 'crit strike chance', '% critical strike chance', 'critical strike chance %', 'local critical strike chance'],
                'patterns': [r'crit(?:ical)?\s*(?:strike)?\s*chance', r'\+\d+%?\s*crit(?:ical)?\s*(?:strike)?\s*chance', r'increased\s*crit(?:ical)?\s*(?:strike)?\s*chance', r'\bcrit\b', r'critical\s*strike'],
                'tiers': [
                    {'name': 'T1', 'value': '+35% to +38%', 'weight': 100, 'ilvl': 85},
                    {'name': 'T2', 'value': '+30% to +34%', 'weight': 200, 'ilvl': 70},
                    {'name': 'T3', 'value': '+25% to +29%', 'weight': 400, 'ilvl': 50},
                    {'name': 'T4', 'value': '+20% to +24%', 'weight': 800, 'ilvl': 30},
                    {'name': 'T5', 'value': '+15% to +19%', 'weight': 1600, 'ilvl': 1}
                ],
                'methods': ['chaos_spam', 'essence', 'fossil', 'alt_regal'],
                'essence': 'Essence of Spite',
                'fossils': ['Aetheric Fossil']
            },
            
            # Elemental Damage
            'Elemental Damage': {
                'type': 'prefix',
                'tiers': [
                    {'name': 'T1', 'value': '+25% to +30%', 'weight': 100, 'ilvl': 85},
                    {'name': 'T2', 'value': '+20% to +24%', 'weight': 200, 'ilvl': 70},
                    {'name': 'T3', 'value': '+15% to +19%', 'weight': 400, 'ilvl': 50},
                    {'name': 'T4', 'value': '+10% to +14%', 'weight': 800, 'ilvl': 30},
                    {'name': 'T5', 'value': '+5% to +9%', 'weight': 1600, 'ilvl': 1}
                ],
                'methods': ['chaos_spam', 'essence', 'fossil', 'alt_regal'],
                'essence': 'Essence of Wrath',
                'fossils': ['Corroded Fossil']
            },
            
            # Movement Speed
            'Movement Speed': {
                'type': 'suffix',
                'tiers': [
                    {'name': 'T1', 'value': '+25% to +30%', 'weight': 100, 'ilvl': 85},
                    {'name': 'T2', 'value': '+20% to +24%', 'weight': 200, 'ilvl': 70},
                    {'name': 'T3', 'value': '+15% to +19%', 'weight': 400, 'ilvl': 50},
                    {'name': 'T4', 'value': '+10% to +14%', 'weight': 800, 'ilvl': 30},
                    {'name': 'T5', 'value': '+5% to +9%', 'weight': 1600, 'ilvl': 1}
                ],
                'methods': ['chaos_spam', 'essence', 'fossil', 'alt_regal'],
                'essence': 'Essence of Speed',
                'fossils': ['Jagged Fossil']
            }
        }
    
    def normalize_modifier_name(self, input_modifier: str) -> str:
        """Enhanced modifier name recognition with fuzzy matching"""
        import re
        
        input_lower = input_modifier.lower().strip()
        
        # Direct match first
        for mod_name, mod_data in self.modifier_database.items():
            if input_lower == mod_name.lower():
                return mod_name
        
        # Check aliases
        for mod_name, mod_data in self.modifier_database.items():
            if 'aliases' in mod_data:
                for alias in mod_data['aliases']:
                    if input_lower == alias.lower():
                        return mod_name
        
        # Pattern matching with regex
        for mod_name, mod_data in self.modifier_database.items():
            if 'patterns' in mod_data:
                for pattern in mod_data['patterns']:
                    if re.search(pattern, input_lower, re.IGNORECASE):
                        return mod_name
        
        # Fuzzy partial matching for common variations
        for mod_name, mod_data in self.modifier_database.items():
            mod_words = set(mod_name.lower().split())
            input_words = set(input_lower.split())
            
            # If significant word overlap, consider it a match
            if len(mod_words.intersection(input_words)) >= min(len(mod_words), 2):
                return mod_name
        
        # Return original if no match found
        return input_modifier
    
    def detect_required_essences(self, target_mods: List[str]) -> Dict:
        """Automatically detect which essences are needed for target modifiers"""
        essence_requirements = {
            'guaranteed_mods': [],
            'required_essences': [],
            'essence_priorities': [],
            'non_essence_mods': []
        }
        
        for mod_name in target_mods:
            normalized_mod = self.normalize_modifier_name(mod_name)
            
            if normalized_mod in self.modifier_database:
                mod_data = self.modifier_database[normalized_mod]
                
                if 'essence' in mod_data:
                    essence_requirements['guaranteed_mods'].append({
                        'modifier': normalized_mod,
                        'essence': mod_data['essence'],
                        'type': mod_data['type']
                    })
                    
                    if mod_data['essence'] not in essence_requirements['required_essences']:
                        essence_requirements['required_essences'].append(mod_data['essence'])
                else:
                    essence_requirements['non_essence_mods'].append(normalized_mod)
        
        # Prioritize essences by modifier importance
        essence_requirements['essence_priorities'] = self._prioritize_essences(essence_requirements['guaranteed_mods'])
        
        return essence_requirements
    
    def _prioritize_essences(self, guaranteed_mods: List[Dict]) -> List[Dict]:
        """Prioritize essences based on modifier importance and rarity"""
        priority_order = {
            'Maximum Life': 1,
            'Maximum Energy Shield': 2,
            'Attack Speed': 3,
            'Critical Strike Chance': 4,
            'Elemental Damage': 5,
            'Movement Speed': 6
        }
        
        prioritized = sorted(guaranteed_mods, 
                           key=lambda x: priority_order.get(x['modifier'], 999))
        
        return prioritized
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="Intelligent Path of Exile Craft Helper", 
                              font=("Arial", 16, "bold"), fg='#2E86AB')
        title_label.pack(pady=10)
        
        # Market status label
        self.status_label = tk.Label(self.root, text="Market: Connecting...", 
                                   font=("Arial", 9), fg='orange')
        self.status_label.pack()
        
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel
        left_panel = tk.Frame(main_frame)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Item base input
        base_frame = tk.Frame(left_panel)
        base_frame.pack(fill='x', pady=5)
        tk.Label(base_frame, text="Item Base:", font=("Arial", 10, "bold")).pack(anchor='w')
        self.base_entry = tk.Entry(base_frame, width=30, font=("Arial", 10))
        self.base_entry.pack(fill='x')
        
        # Item level input
        ilvl_frame = tk.Frame(left_panel)
        ilvl_frame.pack(fill='x', pady=5)
        tk.Label(ilvl_frame, text="Item Level:", font=("Arial", 10, "bold")).pack(anchor='w')
        self.ilvl_entry = tk.Entry(ilvl_frame, width=30, font=("Arial", 10))
        self.ilvl_entry.insert(0, str(CRAFTING_CONFIG['default_item_level']))
        self.ilvl_entry.pack(fill='x')
        
        # Target modifiers input
        target_frame = tk.Frame(left_panel)
        target_frame.pack(fill='x', pady=5)
        tk.Label(target_frame, text="Target Modifiers (one per line):", font=("Arial", 10, "bold")).pack(anchor='w')
        self.target_text = scrolledtext.ScrolledText(target_frame, height=8, width=40, font=("Arial", 9))
        self.target_text.pack(fill='x')
        
        # Modifier suggestions
        suggest_frame = tk.Frame(left_panel)
        suggest_frame.pack(fill='x', pady=5)
        tk.Button(suggest_frame, text="Suggest Modifiers", 
                 command=self.suggest_modifiers, bg='#4CAF50', fg='white',
                 font=("Arial", 10, "bold")).pack(fill='x')
        
        # Right panel
        right_panel = tk.Frame(main_frame)
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Crafting method selection
        method_frame = tk.Frame(right_panel)
        method_frame.pack(fill='x', pady=5)
        tk.Label(method_frame, text="Crafting Method:", font=("Arial", 10, "bold")).pack(anchor='w')
        self.method_var = tk.StringVar(value="auto")
        methods = [
            ("Auto-Select Best Method", "auto"),
            ("Chaos Spam", "chaos_spam"),
            ("Alt + Regal", "alt_regal"),
            ("Essence Crafting", "essence"),
            ("Fossil Crafting", "fossil"),
            ("Flask Crafting", "flask"),
            ("Mastercraft", "mastercraft")
        ]
        for text, value in methods:
            tk.Radiobutton(method_frame, text=text, variable=self.method_var, 
                          value=value, font=("Arial", 9)).pack(anchor='w')
        
        # Budget input
        budget_frame = tk.Frame(right_panel)
        budget_frame.pack(fill='x', pady=5)
        tk.Label(budget_frame, text="Budget (Chaos Orbs):", font=("Arial", 10, "bold")).pack(anchor='w')
        self.budget_entry = tk.Entry(budget_frame, width=30, font=("Arial", 10))
        self.budget_entry.insert(0, str(int(CRAFTING_CONFIG['default_budget'])))
        self.budget_entry.pack(fill='x')
        
        # Generate button
        generate_frame = tk.Frame(right_panel)
        generate_frame.pack(fill='x', pady=10)
        tk.Button(generate_frame, text="Generate Intelligent Crafting Plan", 
                 command=self.generate_intelligent_plan, bg='#2E86AB', fg='white',
                 font=("Arial", 12, "bold")).pack(fill='x')
        
        # Results display
        results_frame = tk.Frame(self.root)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        tk.Label(results_frame, text="Intelligent Crafting Plan:", font=("Arial", 12, "bold")).pack(anchor='w')
        self.results_text = scrolledtext.ScrolledText(results_frame, height=20, width=80, font=("Consolas", 9))
        self.results_text.pack(fill='both', expand=True)
        
        # Enhanced control buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Left side buttons
        left_controls = tk.Frame(control_frame)
        left_controls.pack(side='left')
        tk.Button(left_controls, text="Clear All", command=self.clear_all, 
                 bg='#f44336', fg='white').pack(side='left', padx=2)
        tk.Button(left_controls, text="Refresh Prices", command=self.refresh_prices,
                 bg='#2196F3', fg='white').pack(side='left', padx=2)
        tk.Button(left_controls, text="Detect Item", command=self.open_item_detection,
                 bg='#9C27B0', fg='white').pack(side='left', padx=2)
        
        # Right side buttons  
        right_controls = tk.Frame(control_frame)
        right_controls.pack(side='right')
        tk.Button(right_controls, text="Toggle Overlay", 
                 command=self.toggle_overlay).pack(side='right', padx=2)
        tk.Button(right_controls, text="Multi-Monitor", 
                 command=self.setup_multi_monitor).pack(side='right', padx=2)
        tk.Button(right_controls, text="Analytics", 
                 command=self.open_session_analytics).pack(side='right', padx=2)
        
        # Overlay controls frame
        overlay_frame = tk.Frame(self.root)
        overlay_frame.pack(fill='x', padx=10, pady=2)
        
        # Transparency control
        tk.Label(overlay_frame, text="Opacity:", font=("Arial", 9)).pack(side='left')
        self.opacity_var = tk.DoubleVar(value=0.95)
        opacity_scale = tk.Scale(overlay_frame, from_=0.3, to=1.0, resolution=0.05,
                               orient='horizontal', variable=self.opacity_var,
                               command=self.update_opacity, length=100)
        opacity_scale.pack(side='left', padx=5)
        
        # Position presets
        tk.Label(overlay_frame, text="Position:", font=("Arial", 9)).pack(side='left', padx=(10,0))
        position_frame = tk.Frame(overlay_frame)
        position_frame.pack(side='left', padx=5)
        tk.Button(position_frame, text="TL", command=lambda: self.set_position('top-left'), 
                 width=3).pack(side='left', padx=1)
        tk.Button(position_frame, text="TR", command=lambda: self.set_position('top-right'), 
                 width=3).pack(side='left', padx=1)
        tk.Button(position_frame, text="BL", command=lambda: self.set_position('bottom-left'), 
                 width=3).pack(side='left', padx=1)
        tk.Button(position_frame, text="BR", command=lambda: self.set_position('bottom-right'), 
                 width=3).pack(side='left', padx=1)
        
        # Performance monitor (optional, compact display)
        if hasattr(self, 'performance_optimizer'):
            perf_frame = self.performance_optimizer.create_performance_widget(overlay_frame)
            perf_frame.pack(side='right', padx=10)
        
    def suggest_modifiers(self):
        """Suggest popular modifiers based on item type"""
        suggestions = [
            "Maximum Life",
            "Maximum Energy Shield", 
            "Attack Speed",
            "Critical Strike Chance",
            "Elemental Damage",
            "Movement Speed"
        ]
        
        current_text = self.target_text.get("1.0", tk.END).strip()
        if current_text:
            current_text += "\n"
        
        for suggestion in suggestions:
            current_text += f"{suggestion}\n"
            
        self.target_text.delete("1.0", tk.END)
        self.target_text.insert("1.0", current_text.strip())
        
    def generate_intelligent_plan(self):
        """Generate an AI-enhanced intelligent crafting plan"""
        base_item = self.base_entry.get().strip()
        target_mods = self.target_text.get("1.0", tk.END).strip().split('\n')
        target_mods = [mod.strip() for mod in target_mods if mod.strip()]
        method = self.method_var.get()
        budget = float(self.budget_entry.get() or 1000)
        ilvl = int(self.ilvl_entry.get() or 85)
        
        if not base_item:
            messagebox.showerror("Error", "Please enter an item base!")
            return
            
        if not target_mods:
            messagebox.showerror("Error", "Please enter target modifiers!")
            return
        
        # Create AI crafting scenario
        scenario = CraftingScenario(
            target_modifiers=target_mods,
            item_base=base_item,
            item_level=ilvl,
            budget=budget,
            league_meta={'current_league': get_current_league_name()},
            user_preferences=self.get_user_ai_preferences()
        )
        
        # Calculate precise probabilities
        probability_analysis = self.probability_engine.calculate_exact_probabilities(
            target_mods, base_item, ilvl, method if method != "auto" else "chaos_spam"
        )
        
        # Use AI optimizer if method is auto
        if method == "auto":
            ai_plan = self.ai_optimizer.generate_adaptive_plan(scenario)
            plan = self.format_ai_plan(ai_plan)
            # Add probability analysis to AI plan
            plan += self.format_probability_analysis(probability_analysis)
        else:
            # Enhanced analysis with probability engine
            modifier_analysis = self.analyze_modifiers(target_mods, ilvl)
            plan = self.generate_detailed_plan(base_item, target_mods, method, modifier_analysis, budget, ilvl)
            # Add detailed probability analysis
            plan += self.format_probability_analysis(probability_analysis)
        
        # Add comprehensive intelligent recommendations
        plan += self.generate_comprehensive_recommendations(base_item, target_mods, budget, ilvl)
        
        # Start crafting session tracking
        session_id = self.start_crafting_session(base_item, target_mods, method, budget)
        
        # Add session info to plan
        if session_id:
            plan += f"\n📊 SESSION TRACKING:\n"
            plan += f"Session ID: {session_id}\n"
            plan += f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            plan += f"Use the Analytics button to track your progress!\n"
        
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", plan)
        
    def analyze_modifiers(self, target_mods: List[str], ilvl: int) -> Dict:
        """Analyze target modifiers for compatibility and requirements with enhanced recognition"""
        analysis = {
            'modifiers': [],
            'prefix_count': 0,
            'suffix_count': 0,
            'total_weight': 0,
            'min_ilvl': 1,
            'compatible': True,
            'warnings': [],
            'recognized_modifiers': []
        }
        
        for input_mod in target_mods:
            # Use enhanced modifier recognition
            normalized_mod = self.normalize_modifier_name(input_mod)
            analysis['recognized_modifiers'].append({
                'input': input_mod,
                'recognized_as': normalized_mod
            })
            
            if normalized_mod in self.modifier_database:
                mod_data = self.modifier_database[normalized_mod]
                mod_type = mod_data['type']
                
                # Count prefixes/suffixes
                if mod_type == 'prefix':
                    analysis['prefix_count'] += 1
                else:
                    analysis['suffix_count'] += 1
                    
                # Check item level requirements
                available_tiers = [t for t in mod_data['tiers'] if t['ilvl'] <= ilvl]
                if available_tiers:
                    best_tier = available_tiers[0]  # Highest tier available
                    analysis['modifiers'].append({
                        'name': normalized_mod,
                        'input_name': input_mod,
                        'type': mod_type,
                        'best_tier': best_tier,
                        'weight': best_tier['weight']
                    })
                    analysis['total_weight'] += best_tier['weight']
                    analysis['min_ilvl'] = max(analysis['min_ilvl'], best_tier['ilvl'])
                else:
                    analysis['warnings'].append(f"{normalized_mod} (input: '{input_mod}') requires higher item level than {ilvl}")
                    
            else:
                analysis['warnings'].append(f"Unknown modifier: '{input_mod}' (could not recognize)")
                
        # Check compatibility (max 3 prefixes, 3 suffixes)
        if analysis['prefix_count'] > 3:
            analysis['compatible'] = False
            analysis['warnings'].append("Too many prefixes (max 3)")
        if analysis['suffix_count'] > 3:
            analysis['compatible'] = False
            analysis['warnings'].append("Too many suffixes (max 3)")
            
        return analysis
        
    def select_best_method(self, analysis: Dict, budget: float) -> str:
        """Select optimal crafting method using market price analysis"""
        if not analysis['compatible']:
            return "chaos_spam"  # Fallback
            
        mod_count = len(analysis['modifiers'])
        total_weight = analysis['total_weight']
        current_prices = self.currency_costs
        
        # Calculate cost efficiency for each method
        methods = []
        
        # Chaos spam method
        chaos_cost = (200 + (total_weight * 0.5)) * current_prices.get('Chaos Orb', 1.0)
        chaos_cost += max(1, mod_count // 2) * current_prices.get('Divine Orb', 15.0)
        chaos_cost += mod_count * current_prices.get('Orb of Annulment', 8.0)
        methods.append({
            'name': 'chaos_spam',
            'cost': chaos_cost,
            'success_rate': 0.7,  # Baseline success rate
            'efficiency': 0.7 / max(chaos_cost, 1)
        })
        
        # Alt-regal method (good for 1-2 mods)
        if mod_count <= 2:
            alt_cost = (50 + (total_weight * 0.2)) * current_prices.get('Orb of Alteration', 0.1)
            alt_cost += mod_count * current_prices.get('Regal Orb', 2.0)
            alt_cost += max(0, mod_count - 1) * current_prices.get('Exalted Orb', 200.0)
            methods.append({
                'name': 'alt_regal',
                'cost': alt_cost,
                'success_rate': 0.5,
                'efficiency': 0.5 / max(alt_cost, 1)
            })
        
        # Essence method
        essence_cost = mod_count * current_prices.get('Essence', 5.0)
        essence_cost += 100 * current_prices.get('Chaos Orb', 1.0)
        essence_cost += mod_count * current_prices.get('Orb of Annulment', 8.0)
        methods.append({
            'name': 'essence',
            'cost': essence_cost,
            'success_rate': 0.8,
            'efficiency': 0.8 / max(essence_cost, 1)
        })
        
        # Fossil method  
        fossil_cost = mod_count * current_prices.get('Fossil', 3.0)
        fossil_cost += mod_count * current_prices.get('Resonator', 2.0)
        fossil_cost += 50 * current_prices.get('Chaos Orb', 1.0)
        methods.append({
            'name': 'fossil',
            'cost': fossil_cost,
            'success_rate': 0.6,
            'efficiency': 0.6 / max(fossil_cost, 1)
        })
        
        # Filter methods within budget
        affordable_methods = [m for m in methods if m['cost'] <= budget]
        
        if affordable_methods:
            # Select most efficient method within budget
            best_method = max(affordable_methods, key=lambda x: x['efficiency'])
            return best_method['name']
        else:
            # If nothing is affordable, choose cheapest
            cheapest = min(methods, key=lambda x: x['cost'])
            return cheapest['name']
    
    def optimize_budget_allocation(self, target_mods: List[str], budget: float) -> str:
        """Generate optimized budget allocation using market API"""
        try:
            optimization = self.price_optimizer.optimize_crafting_budget(target_mods, budget)
            
            plan = "\n🎯 BUDGET OPTIMIZATION:\n"
            plan += "-" * 40 + "\n"
            plan += f"Total Budget: {budget:.1f} chaos orbs\n\n"
            
            plan += "RECOMMENDED ALLOCATION:\n"
            for currency, details in optimization.get('allocation', {}).items():
                plan += f"• {currency}: {details['currency_amount']:.1f} units ({details['chaos_allocated']:.1f}c)\n"
                
            remaining = optimization.get('remaining_budget', 0)
            if remaining > 0:
                plan += f"\nRemaining Budget: {remaining:.1f}c (for contingencies)\n"
                
            plan += f"\nOptimization calculated at: {optimization.get('optimization_timestamp', 'Unknown')}\n"
            return plan
            
        except Exception as e:
            return f"\n⚠ Budget optimization failed: {e}\n"
        
    def generate_detailed_plan(self, base_item: str, target_mods: List[str], 
                             method: str, analysis: Dict, budget: float, ilvl: int) -> str:
        """Generate a detailed, intelligent crafting plan"""
        plan = f"INTELLIGENT CRAFTING PLAN FOR {base_item.upper()}\n"
        plan += "="*60 + "\n\n"
        
        # Analysis summary
        plan += "ANALYSIS SUMMARY:\n"
        plan += f"• Item Level: {ilvl}\n"
        plan += f"• Target Modifiers: {len(target_mods)}\n"
        plan += f"• Prefixes: {analysis['prefix_count']}/3\n"
        plan += f"• Suffixes: {analysis['suffix_count']}/3\n"
        plan += f"• Total Weight: {analysis['total_weight']}\n"
        plan += f"• Budget: {budget} Chaos Orbs\n"
        plan += f"• Selected Method: {method.upper()}\n\n"
        
        # Show modifier recognition results
        if 'recognized_modifiers' in analysis and analysis['recognized_modifiers']:
            plan += "MODIFIER RECOGNITION:\n"
            for rec in analysis['recognized_modifiers']:
                if rec['input'] != rec['recognized_as']:
                    plan += f"• '{rec['input']}' → '{rec['recognized_as']}' ✓\n"
                else:
                    plan += f"• '{rec['input']}' ✓\n"
            plan += "\n"
        
        if analysis['warnings']:
            plan += "WARNINGS:\n"
            for warning in analysis['warnings']:
                plan += f"⚠ {warning}\n"
            plan += "\n"
            
        if not analysis['compatible']:
            plan += "❌ INCOMPATIBLE MODIFIER COMBINATION!\n"
            plan += "Please reduce the number of prefixes/suffixes.\n\n"
            return plan
            
        # Detailed steps based on method
        if method == "chaos_spam":
            plan += self.generate_chaos_spam_plan(target_mods, analysis, budget)
        elif method == "alt_regal":
            plan += self.generate_alt_regal_plan(target_mods, analysis, budget)
        elif method == "essence":
            plan += self.generate_essence_plan(target_mods, analysis, budget)
        elif method == "fossil":
            plan += self.generate_fossil_plan(target_mods, analysis, budget)
        elif method == "flask":
            plan += self.generate_flask_plan(target_mods, analysis, budget)
        elif method == "mastercraft":
            plan += self.generate_mastercraft_plan(target_mods, analysis, budget)
            
        # Cost estimation
        plan += self.estimate_costs(method, analysis, budget)
        
        # Budget optimization
        plan += self.optimize_budget_allocation(target_mods, budget)
        
        # Success probability
        plan += self.calculate_success_probability(method, analysis)
        
        # Alternative suggestions
        plan += self.suggest_alternatives(target_mods, analysis)
        
        return plan
        
    def generate_chaos_spam_plan(self, target_mods: List[str], analysis: Dict, budget: float) -> str:
        """Generate chaos spam crafting plan"""
        plan = "CHAOS SPAM METHOD:\n"
        plan += "-" * 30 + "\n\n"
        
        plan += "EXACT STEPS TO FOLLOW:\n"
        plan += f"1. 🛒 BUY: {int(budget * 0.8)} Chaos Orbs, 5-10 Divine Orbs, 2-3 Annulment Orbs\n"
        plan += f"2. 🏪 ACQUIRE: {analysis.get('item_base', 'Base item')} with item level {analysis.get('min_ilvl', 85)}+\n"
        plan += "3. ✅ CHECK: Item must be RARE (yellow) - if not, use Orb of Alchemy\n"
        plan += "4. 🎲 CRAFT: Right-click Chaos Orb → Left-click your item\n"
        plan += "5. 👀 INSPECT: Check if you got your target modifiers\n"
        plan += "6. 🔄 REPEAT: Steps 4-5 until you get desired modifiers\n"
        plan += "7. 💎 OPTIMIZE: Use Divine Orbs to perfect the numeric values\n"
        plan += "8. 🗑️ CLEAN: Use Annulment Orbs to remove bad modifiers (RISKY!)\n\n"
        
        plan += "TARGET MODIFIERS:\n"
        for i, mod in enumerate(analysis['modifiers'], 1):
            tier = mod['best_tier']
            plan += f"  {i}. {mod['name']} ({tier['name']}: {tier['value']})\n"
        plan += "\n"
        
        plan += "⚠️ IMPORTANT ACTIONS:\n"
        plan += f"• STOP crafting when you see: {', '.join(target_mods)}\n"
        plan += f"• BUDGET LIMIT: Stop at {int(budget * 0.9)} Chaos Orbs used\n"
        plan += "• SAVE OFTEN: Create multiple copies of promising items\n"
        plan += "• USE FILTER: Highlight items with your target mods\n"
        plan += f"• EXPECTED ATTEMPTS: ~{max(50, int(budget / 10))} chaos orbs for success\n\n"
        
        return plan
        
    def generate_alt_regal_plan(self, target_mods: List[str], analysis: Dict, budget: float) -> str:
        """Generate alt+regal crafting plan"""
        plan = "ALTERATION + REGAL METHOD:\n"
        plan += "-" * 30 + "\n\n"
        plan += f"Budget: {budget:.0f}c | Target: {len(target_mods)} modifiers\n\n"
        
        plan += "EXACT STEPS TO FOLLOW:\n"
        plan += f"1. 🛒 BUY: {int(budget * 0.4)} Alteration Orbs, {int(budget * 0.1)} Augmentation Orbs, 5 Regal Orbs, 2-3 Exalted Orbs\n"
        plan += f"2. 🏪 ACQUIRE: WHITE (normal) {analysis.get('item_base', 'base item')} with ilvl {analysis.get('min_ilvl', 85)}+\n"
        plan += "3. ✅ USE: Right-click Orb of Transmutation → Left-click item (makes it BLUE/magic)\n"
        plan += "4. 🎲 SPAM: Right-click Alteration Orb → Left-click item until you see ONE target mod\n"
        plan += "5. 🔍 CHECK: If item has only 1 mod, use Augmentation Orb to add 2nd mod\n"
        plan += "6. ⬆️ UPGRADE: Right-click Regal Orb → Left-click item (makes it YELLOW/rare)\n"
        plan += "7. ✨ FINISH: Use Exalted Orbs to add remaining target modifiers\n"
        plan += "7. Use Divine Orbs to perfect values\n\n"
        
        plan += "TARGET MODIFIERS:\n"
        for i, mod in enumerate(analysis['modifiers'], 1):
            tier = mod['best_tier']
            plan += f"  {i}. {mod['name']} ({tier['name']}: {tier['value']})\n"
        plan += "\n"
        
        plan += "TIPS:\n"
        plan += "• Use Eternal Orb imprint before regaling if available\n"
        plan += "• Focus on highest weight modifiers first\n"
        plan += "• Consider using Beastcrafting for imprinting\n"
        plan += "⚠️ COMPLETION CHECKLIST:\n"
        plan += f"• ✅ Got target prefix mods: {', '.join([m for m in target_mods if 'life' in m.lower() or 'damage' in m.lower()][:2])}\n"
        plan += f"• ✅ Got target suffix mods: {', '.join([m for m in target_mods if 'resist' in m.lower() or 'speed' in m.lower()][:2])}\n"
        plan += f"• ✅ Budget remaining: Track your spending vs {budget}c limit\n\n"
        
        return plan
        
    def generate_essence_plan(self, target_mods: List[str], analysis: Dict, budget: float) -> str:
        """Generate detailed essence crafting plan with automatic essence detection"""
        plan = "ESSENCE CRAFTING METHOD:\n"
        plan += "-" * 30 + "\n\n"
        plan += f"Budget: {budget:.0f}c | Complexity: {analysis.get('total_weight', 0)}\n\n"
        
        # Auto-detect required essences
        essence_req = self.detect_required_essences(target_mods)
        
        if essence_req['guaranteed_mods']:
            plan += "🔍 AUTO-DETECTED ESSENCE REQUIREMENTS:\n"
            for priority_mod in essence_req['essence_priorities']:
                plan += f"• {priority_mod['modifier']} → {priority_mod['essence']} ({priority_mod['type']})\n"
            plan += "\n"
            
            plan += "📋 DETAILED STEP-BY-STEP PROCESS:\n"
            plan += "=" * 40 + "\n\n"
            
            # Step 1: Identify essences
            plan += "STEP 1: ESSENCE IDENTIFICATION ✅\n"
            plan += f"Required Essences: {', '.join(essence_req['required_essences'])}\n"
            plan += f"Primary Essence: {essence_req['essence_priorities'][0]['essence']}\n"
            plan += f"Guarantees: {essence_req['essence_priorities'][0]['modifier']}\n\n"
            
            # Step 2: Use essence on base
            plan += "STEP 2: APPLY PRIMARY ESSENCE 🎯\n"
            plan += f"🛒 BUY: {essence_req['essence_priorities'][0]['essence']} (quantity: {max(10, int(budget/20))})\n"
            plan += f"🏪 ACQUIRE: WHITE {analysis.get('item_base', 'base item')} with ilvl {analysis.get('min_ilvl', 85)}+\n"
            plan += f"✅ ACTION: Right-click {essence_req['essence_priorities'][0]['essence']} → Left-click item\n"
            plan += f"👀 RESULT: Item becomes RARE with guaranteed {essence_req['essence_priorities'][0]['modifier']}\n\n"
            primary_essence = essence_req['essence_priorities'][0]['essence']
            primary_mod = essence_req['essence_priorities'][0]['modifier']
            plan += f"1. Obtain base item (normal rarity)\n"
            plan += f"2. Use {primary_essence} on base item\n"
            plan += f"3. This GUARANTEES {primary_mod} modifier\n"
            plan += f"4. Check other rolled modifiers\n\n"
            
            # Step 3: Evaluation
            plan += "STEP 3: EVALUATE RESULTS 🔍\n"
            plan += "If satisfied with all modifiers:\n"
            plan += "  → Proceed to Step 5 (Divine Orbs)\n"
            plan += "If you need more modifiers:\n"
            plan += "  → Proceed to Step 4 (Exalted Orbs)\n"
            plan += "If completely unsatisfied:\n"
            plan += "  → Use Chaos Orbs or restart with essence\n\n"
            
            # Step 4: Add more modifiers
            plan += "STEP 4: ADD MORE MODIFIERS 💎\n"
            if len(essence_req['essence_priorities']) > 1:
                plan += f"Option A: Use additional essences:\n"
                for i, mod in enumerate(essence_req['essence_priorities'][1:], 2):
                    plan += f"  {i}. {mod['essence']} for {mod['modifier']}\n"
                plan += "Option B: Use Exalted Orbs (random modifiers)\n"
            else:
                plan += "Use Exalted Orbs to add random modifiers\n"
            
            if essence_req['non_essence_mods']:
                plan += f"Note: These modifiers cannot be guaranteed with essences:\n"
                for mod in essence_req['non_essence_mods']:
                    plan += f"  • {mod} (requires Exalted Orbs or luck)\n"
            plan += "\n"
            
            # Step 5: Perfect values
            plan += "STEP 5: PERFECT VALUES ✨\n"
            plan += "1. Use Divine Orbs to reroll modifier values\n"
            plan += "2. Target tier 1-2 values for best results\n"
            plan += "3. Divine Orbs are expensive - use sparingly\n\n"
            
        else:
            plan += "⚠️ NO ESSENCE-GUARANTEED MODIFIERS FOUND\n"
            plan += "None of your target modifiers can be guaranteed with essences.\n"
            plan += "Consider alternative crafting methods like:\n"
            plan += "• Chaos Spam\n"
            plan += "• Alt-Regal\n"
            plan += "• Fossil Crafting\n\n"
        
        # Cost estimation
        plan += "💰 ESSENCE CRAFTING COSTS:\n"
        plan += f"Budget: {budget} Chaos Orbs\n"
        if essence_req['required_essences']:
            plan += "Estimated essence costs:\n"
            for essence in essence_req['required_essences']:
                plan += f"• {essence}: 5-15 Chaos each\n"
        plan += "• Exalted Orbs: 150-200 Chaos each\n"
        plan += "• Divine Orbs: 200-250 Chaos each\n\n"
        
        plan += "💡 ESSENCE CRAFTING TIPS:\n"
        plan += "• Always start with white (normal) base items\n"
        plan += "• Essences can be used on magic items (removes existing mods)\n"
        plan += "• Higher tier essences give better modifier ranges\n"
        plan += "• Plan your prefix/suffix allocation carefully\n"
        plan += "• Consider essence prices vs. expected attempts\n\n"
        
        return plan
        
    def generate_fossil_plan(self, target_mods: List[str], analysis: Dict, budget: float) -> str:
        """Generate fossil crafting plan"""
        plan = "FOSSIL CRAFTING METHOD:\n"
        plan += "-" * 30 + "\n\n"
        plan += f"Budget: {budget:.0f}c | Modifiers: {len(target_mods)}\n\n"
        
        plan += "STEP-BY-STEP PROCESS:\n"
        plan += "1. Obtain relevant fossils for your modifiers\n"
        plan += "2. Use Resonators to apply fossils to base item\n"
        plan += "3. Fossils bias the outcome toward certain modifiers\n"
        plan += "4. Repeat until satisfied with results\n"
        plan += "5. Use Divine Orbs to perfect values\n\n"
        
        plan += "FOSSIL RECOMMENDATIONS:\n"
        for mod in analysis['modifiers']:
            if mod['name'] in self.modifier_database:
                fossils = self.modifier_database[mod['name']].get('fossils', ['Unknown'])
                plan += f"• {mod['name']}: {', '.join(fossils)}\n"
        plan += "\n"
        
        plan += "TIPS:\n"
        plan += "• Fossils increase/decrease chances of modifier types\n"
        plan += "• Combine multiple fossils for better targeting\n"
        plan += "• More expensive but more controlled than chaos spam\n"
        plan += "• Check fossil prices and availability\n\n"
        
        return plan
        
    def generate_flask_plan(self, target_mods: List[str], analysis: Dict, budget: float) -> str:
        """Generate flask crafting plan"""
        plan = "FLASK CRAFTING METHOD:\n"
        plan += "-" * 30 + "\n\n"
        plan += f"Budget: {budget:.0f}c | Target flask modifiers: {len(target_mods)}\n\n"
        
        # Flask-specific analysis
        flask_types = {
            'life': 'Life Flask',
            'mana': 'Mana Flask', 
            'hybrid': 'Hybrid Flask',
            'utility': 'Utility Flask (Diamond, Granite, etc.)',
            'unique': 'Unique Flask'
        }
        
        # Detect flask type from modifiers
        detected_type = 'utility'  # default
        if any('life' in mod.lower() for mod in target_mods):
            detected_type = 'life'
        elif any('mana' in mod.lower() for mod in target_mods):
            detected_type = 'mana'
        
        plan += "EXACT STEPS TO FOLLOW:\n"
        plan += f"1. 🛒 BUY: {int(budget * 0.4)} Orb of Alteration, {int(budget * 0.1)} Orb of Augmentation\n"
        plan += f"2. 🛒 BUY: 3-5 Glassblower's Baubles, 2-3 Orb of Fusing (for quality)\n"
        plan += f"3. 🎯 ACQUIRE: WHITE (normal) {flask_types.get(detected_type, 'utility flask')} with appropriate level\n"
        plan += "4. ✨ QUALITY: Use Glassblower's Baubles to get 20% quality (increases modifier values)\n"
        plan += "5. 🔵 MAGIC: Right-click Orb of Transmutation → Left-click flask (makes it BLUE/magic)\n"
        plan += "6. 🎲 ROLL: Right-click Orb of Alteration → Left-click flask until you get ONE target modifier\n"
        plan += "7. ➕ AUGMENT: If flask has only 1 modifier, use Orb of Augmentation to add 2nd\n"
        plan += "8. 🔄 REPEAT: Steps 6-7 until you get both desired flask modifiers\n\n"
        
        plan += "🧪 FLASK-SPECIFIC TIPS:\n"
        plan += f"• STOP when you see: {', '.join(target_mods)}\n"
        plan += "• Flask modifiers are PREFIX + SUFFIX (max 1 of each)\n"
        plan += "• Quality affects modifier values - always 20% quality first\n"
        plan += "• Life flasks: Look for % increased recovery rate, instant recovery\n"
        plan += "• Utility flasks: Look for % increased duration, immunity effects\n"
        plan += f"• BUDGET LIMIT: Stop at {int(budget * 0.9)} chaos worth of currency used\n\n"
        
        plan += "⚠️ FLASK MODIFIER TYPES:\n"
        plan += "• PREFIX: Recovery amount, charges used, recovery rate\n"
        plan += "• SUFFIX: Duration, immunity, resistance, utility effects\n"
        plan += "• Cannot have multiple prefixes or multiple suffixes\n\n"
        
        return plan
        
    def generate_mastercraft_plan(self, target_mods: List[str], analysis: Dict, budget: float) -> str:
        """Generate mastercraft plan"""
        plan = "MASTERCRAFT METHOD:\n"
        plan += "-" * 30 + "\n\n"
        plan += f"Budget: {budget:.0f}c | Target mods: {len(target_mods)}\n\n"
        
        plan += "STEP-BY-STEP PROCESS:\n"
        plan += "1. Craft base item using other methods first\n"
        plan += "2. Use Crafting Bench to add guaranteed modifiers\n"
        plan += "3. Mastercrafted mods can be changed at any time\n"
        plan += "4. Consider this for final modifier slots\n\n"
        
        plan += "TARGET MODIFIERS:\n"
        for i, mod in enumerate(analysis['modifiers'], 1):
            tier = mod['best_tier']
            plan += f"  {i}. {mod['name']} ({tier['name']}: {tier['value']})\n"
        plan += "\n"
        
        plan += "TIPS:\n"
        plan += "• Only use for modifiers available on crafting bench\n"
        plan += "• Leaves item with 'Crafted' modifier\n"
        plan += "• Can be removed with Orb of Scouring\n"
        plan += "• Great for finishing touches\n\n"
        
        return plan
        
    def estimate_costs(self, method: str, analysis: Dict, budget: float) -> str:
        """Estimate crafting costs using real-time market prices"""
        plan = "COST ESTIMATION (Live Market Prices):\n"
        plan += "-" * 40 + "\n"
        
        # Get current market prices
        current_prices = self.currency_costs
        total_chaos_cost = 0
        
        if method == "chaos_spam":
            base_attempts = 200 + (analysis['total_weight'] * 0.5)
            chaos_cost = base_attempts * current_prices.get('Chaos Orb', 1.0)
            divine_count = max(1, len(analysis['modifiers']) // 2)
            divine_cost = divine_count * current_prices.get('Divine Orb', 15.0)
            annul_count = len(analysis['modifiers'])
            annul_cost = annul_count * current_prices.get('Orb of Annulment', 8.0)
            
            total_chaos_cost = chaos_cost + divine_cost + annul_cost
            
            plan += f"• Chaos Orbs needed: {base_attempts:.0f} = {chaos_cost:.1f}c\n"
            plan += f"• Divine Orbs: {divine_count} × {current_prices.get('Divine Orb', 15.0):.1f}c = {divine_cost:.1f}c\n"
            plan += f"• Annulment Orbs: {annul_count} × {current_prices.get('Orb of Annulment', 8.0):.1f}c = {annul_cost:.1f}c\n"
            
        elif method == "alt_regal":
            alt_attempts = 50 + (analysis['total_weight'] * 0.2)
            alt_cost = alt_attempts * current_prices.get('Orb of Alteration', 0.1)
            regal_count = len(analysis['modifiers'])
            regal_cost = regal_count * current_prices.get('Regal Orb', 2.0)
            ex_count = max(0, len(analysis['modifiers']) - 1)
            ex_cost = ex_count * current_prices.get('Exalted Orb', 200.0)
            
            total_chaos_cost = alt_cost + regal_cost + ex_cost
            
            plan += f"• Alteration Orbs: {alt_attempts:.0f} × {current_prices.get('Orb of Alteration', 0.1):.3f}c = {alt_cost:.1f}c\n"
            plan += f"• Regal Orbs: {regal_count} × {current_prices.get('Regal Orb', 2.0):.1f}c = {regal_cost:.1f}c\n"
            plan += f"• Exalted Orbs: {ex_count} × {current_prices.get('Exalted Orb', 200.0):.1f}c = {ex_cost:.1f}c\n"
            
        elif method == "essence":
            essence_count = len(analysis['modifiers'])
            essence_cost = essence_count * current_prices.get('Essence', 5.0)
            chaos_cost = 100 * current_prices.get('Chaos Orb', 1.0)
            annul_cost = essence_count * current_prices.get('Orb of Annulment', 8.0)
            
            total_chaos_cost = essence_cost + chaos_cost + annul_cost
            
            plan += f"• Essences: {essence_count} × {current_prices.get('Essence', 5.0):.1f}c = {essence_cost:.1f}c\n"
            plan += f"• Chaos Orbs: 100 × {current_prices.get('Chaos Orb', 1.0):.1f}c = {chaos_cost:.1f}c\n"
            plan += f"• Annulment Orbs: {essence_count} × {current_prices.get('Orb of Annulment', 8.0):.1f}c = {annul_cost:.1f}c\n"
            
        elif method == "fossil":
            fossil_count = len(analysis['modifiers'])
            fossil_cost = fossil_count * current_prices.get('Fossil', 3.0)
            resonator_cost = fossil_count * current_prices.get('Resonator', 2.0)
            chaos_cost = 50 * current_prices.get('Chaos Orb', 1.0)
            
            total_chaos_cost = fossil_cost + resonator_cost + chaos_cost
            
            plan += f"• Fossils: {fossil_count} × {current_prices.get('Fossil', 3.0):.1f}c = {fossil_cost:.1f}c\n"
            plan += f"• Resonators: {fossil_count} × {current_prices.get('Resonator', 2.0):.1f}c = {resonator_cost:.1f}c\n"
            plan += f"• Chaos Orbs: 50 × {current_prices.get('Chaos Orb', 1.0):.1f}c = {chaos_cost:.1f}c\n"
            
        elif method == "flask":
            alt_attempts = 50 + (len(analysis['modifiers']) * 20)  # Flask rolling is easier
            alt_cost = alt_attempts * current_prices.get('Orb of Alteration', 0.1)
            aug_count = max(1, len(analysis['modifiers']))
            aug_cost = aug_count * current_prices.get('Orb of Augmentation', 0.5)
            glassblow_count = 5
            glassblow_cost = glassblow_count * current_prices.get("Glassblowers Bauble", 1.0)
            
            total_chaos_cost = alt_cost + aug_cost + glassblow_cost
            
            plan += f"• Alteration Orbs: {alt_attempts:.0f} × {current_prices.get('Orb of Alteration', 0.1):.3f}c = {alt_cost:.1f}c\n"
            plan += f"• Augmentation Orbs: {aug_count} × {current_prices.get('Orb of Augmentation', 0.5):.1f}c = {aug_cost:.1f}c\n"
            plan += f"• Glassblower's Baubles: {glassblow_count} × {current_prices.get('Glassblowers Bauble', 1.0):.1f}c = {glassblow_cost:.1f}c\n"
            
        else:
            total_chaos_cost = 100
            plan += f"• Base crafting costs: {total_chaos_cost:.1f}c\n"
            
        plan += f"\n💰 TOTAL ESTIMATED COST: {total_chaos_cost:.1f} chaos orbs\n"
        
        # Budget analysis with cost efficiency
        if total_chaos_cost > budget:
            over_budget = total_chaos_cost - budget
            plan += f"⚠ WARNING: Cost ({total_chaos_cost:.1f}c) exceeds budget ({budget}c) by {over_budget:.1f}c\n"
        else:
            plan += f"✅ Budget sufficient for this method\n"
            
        plan += "\n"
        return plan
        
    def calculate_success_probability(self, method: str, analysis: Dict) -> str:
        """Calculate success probability"""
        plan = "SUCCESS PROBABILITY:\n"
        plan += "-" * 20 + "\n"
        
        total_weight = analysis.get('total_weight', 0)
        mod_count = len(analysis.get('modifiers', []))
        
        if method == "chaos_spam":
            # Rough probability calculation
            base_prob = 1.0
            for mod in analysis.get('modifiers', []):
                prob = mod.get('weight', 1000) / 10000  # Rough estimate
                base_prob *= prob
            success_rate = base_prob * 100
            plan += f"• Getting all {mod_count} modifiers: {success_rate:.4f}%\n"
            plan += f"• Total modifier weight: {total_weight}\n"
            plan += f"• Expected attempts: {1/max(success_rate/100, 0.0001):.0f} chaos orbs\n"
            
        elif method == "alt_regal":
            success_rate = 50.0  # Rough estimate for alt+regal
            plan += f"• Success rate per attempt: {success_rate}%\n"
            plan += f"• Expected attempts: {2} (1 alt, 1 regal)\n"
            
        elif method == "essence":
            success_rate = 80.0  # Essence guarantees one mod
            plan += f"• Guaranteed modifier success: {success_rate}%\n"
            plan += f"• Additional mods: RNG dependent\n"
            
        else:
            success_rate = 30.0
            plan += f"• Estimated success rate: {success_rate}%\n"
            
        plan += "\n"
        return plan
        
    def suggest_alternatives(self, target_mods: List[str], analysis: Dict) -> str:
        """Suggest alternative modifiers"""
        plan = "ALTERNATIVE SUGGESTIONS:\n"
        plan += "-" * 25 + "\n"
        
        if analysis.get('warnings'):
            plan += "⚠️ DETECTED ISSUES:\n"
            for warning in analysis['warnings'][:3]:
                plan += f"• {warning}\n"
            plan += "\n"
        
        for mod_name in target_mods:
            if mod_name in self.modifier_database:
                mod_data = self.modifier_database[mod_name]
                mod_type = mod_data['type']
                
                # Find similar modifiers
                alternatives = []
                for other_mod, other_data in self.modifier_database.items():
                    if other_mod != mod_name and other_data['type'] == mod_type:
                        alternatives.append(other_mod)
                        
                if alternatives:
                    plan += f"• Instead of '{mod_name}', consider:\n"
                    for alt in alternatives[:3]:  # Top 3 alternatives
                        plan += f"  - {alt}\n"
                    plan += "\n"
                    
        plan += "GENERAL TIPS:\n"
        plan += "• Always check item level requirements\n"
        plan += "• Consider using Orb of Scouring to start over\n"
        plan += "• Divine Orbs reroll numeric values\n"
        plan += "• Annulment Orbs can remove unwanted modifiers\n"
        plan += "• Use PoE wiki/craft of exile for detailed info\n"
        plan += "• Consider influenced items for special modifiers\n"
        
        return plan
        
    def clear_all(self):
        self.base_entry.delete(0, tk.END)
        self.target_text.delete("1.0", tk.END)
        self.results_text.delete("1.0", tk.END)
        self.budget_entry.delete(0, tk.END)
        self.budget_entry.insert(0, "1000")
        self.ilvl_entry.delete(0, tk.END)
        self.ilvl_entry.insert(0, "85")
        
    def toggle_overlay(self):
        current = self.root.attributes('-topmost')
        self.root.attributes('-topmost', not current)
    
    def refresh_prices(self):
        """Manually refresh market prices"""
        try:
            self.market_api.update_all_prices()
            self.currency_costs = self.market_api.get_all_currency_prices()
            self.last_price_update = datetime.now()
            self.update_price_status()
            messagebox.showinfo("Success", "Market prices refreshed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh prices: {e}")
    
    def update_opacity(self, value):
        """Update window opacity"""
        try:
            opacity = float(value)
            self.root.attributes('-alpha', opacity)
        except Exception as e:
            print(f"Error setting opacity: {e}")
    
    def set_position(self, position):
        """Set window position based on preset"""
        try:
            # Get screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Get window dimensions
            self.root.update_idletasks()
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            # Calculate positions
            positions = {
                'top-left': (50, 50),
                'top-right': (screen_width - window_width - 50, 50),
                'bottom-left': (50, screen_height - window_height - 100),
                'bottom-right': (screen_width - window_width - 50, screen_height - window_height - 100),
            }
            
            if position in positions:
                x, y = positions[position]
                self.root.geometry(f"+{x}+{y}")
        except Exception as e:
            print(f"Error setting position: {e}")
    
    def setup_multi_monitor(self):
        """Setup multi-monitor overlay functionality"""
        try:
            # Create a new window for second monitor
            if hasattr(self, 'secondary_window') and self.secondary_window.winfo_exists():
                self.secondary_window.destroy()
            
            self.secondary_window = tk.Toplevel(self.root)
            self.secondary_window.title("PoE Helper - Monitor 2")
            self.secondary_window.geometry("400x300")
            self.secondary_window.attributes('-topmost', True)
            self.secondary_window.attributes('-alpha', 0.9)
            
            # Add essential info to secondary window
            tk.Label(self.secondary_window, text="Quick Price Reference", 
                    font=("Arial", 12, "bold")).pack(pady=10)
            
            # Currency prices display
            price_frame = tk.Frame(self.secondary_window)
            price_frame.pack(fill='both', expand=True, padx=10)
            
            key_currencies = ['Divine Orb', 'Exalted Orb', 'Orb of Annulment', 'Orb of Scouring']
            for currency in key_currencies:
                price = self.currency_costs.get(currency, 0)
                tk.Label(price_frame, text=f"{currency}: {price:.1f}c", 
                        font=("Arial", 10)).pack(anchor='w')
            
            # Position on second monitor (if available)
            try:
                screen_width = self.root.winfo_screenwidth()
                self.secondary_window.geometry(f"+{screen_width + 50}+50")
            except:
                self.secondary_window.geometry("+900+50")
                
            messagebox.showinfo("Multi-Monitor", "Secondary monitor window created!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to setup multi-monitor: {e}")
    
    def open_item_detection(self):
        """Open item detection window"""
        try:
            self.item_detection.open_detection_window()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open item detection: {e}")
    
    def load_user_preferences(self):
        """Load and apply user preferences"""
        try:
            prefs = self.session_tracker.preferences
            
            # Apply overlay preferences
            if hasattr(self, 'root'):
                self.root.attributes('-alpha', prefs.overlay_opacity)
            
            # Store for later use in UI setup
            self.user_preferences = prefs
            
        except Exception as e:
            print(f"Error loading preferences: {e}")
    
    def start_crafting_session(self, base_item: str, target_mods: List[str], method: str, budget: float):
        """Start tracking a new crafting session"""
        try:
            self.current_session_id = self.session_tracker.start_session(
                base_item, target_mods, method, budget
            )
            return self.current_session_id
        except Exception as e:
            print(f"Error starting session: {e}")
            return None
    
    def end_crafting_session(self, actual_cost: Optional[float] = None, 
                           success: Optional[bool] = None, notes: str = ""):
        """End the current crafting session"""
        if self.current_session_id:
            try:
                result = self.session_tracker.end_session(actual_cost, success, notes)
                self.current_session_id = None
                return result
            except Exception as e:
                print(f"Error ending session: {e}")
                return False
        return False
    
    def open_session_analytics(self):
        """Open session analytics window"""
        try:
            analytics_window = tk.Toplevel(self.root)
            analytics_window.title("Crafting Analytics")
            analytics_window.geometry("600x500")
            analytics_window.attributes('-topmost', True)
            
            # Get analytics data
            analytics = self.session_tracker.get_analytics(30)
            recent_sessions = self.session_tracker.get_session_history(10)
            
            # Title
            tk.Label(analytics_window, text="Crafting Analytics (Last 30 Days)", 
                    font=("Arial", 14, "bold")).pack(pady=10)
            
            # Analytics display
            analytics_text = tk.Text(analytics_window, height=25, width=70, font=("Consolas", 10))
            analytics_text.pack(fill='both', expand=True, padx=10, pady=5)
            
            # Format analytics data
            output = "CRAFTING STATISTICS\n"
            output += "=" * 50 + "\n\n"
            
            if analytics:
                output += f"Total Sessions: {analytics.get('total_sessions', 0)}\n"
                output += f"Successful Sessions: {analytics.get('successful_sessions', 0)}\n"
                output += f"Success Rate: {analytics.get('success_rate', 0):.1f}%\n"
                output += f"Total Cost: {analytics.get('total_cost', 0):.1f} chaos\n"
                output += f"Average Cost: {analytics.get('average_cost', 0):.1f} chaos\n"
                output += f"Most Used Method: {analytics.get('most_used_method', 'None')}\n"
                output += f"Most Crafted Base: {analytics.get('most_crafted_base', 'None')}\n\n"
            
            output += "RECENT SESSIONS\n"
            output += "-" * 30 + "\n"
            
            for i, session in enumerate(recent_sessions[:5], 1):
                output += f"{i}. {session['item_base']} - {session['method_used']}\n"
                output += f"   Budget: {session['budget_allocated']:.1f}c"
                if session['actual_cost']:
                    output += f" | Cost: {session['actual_cost']:.1f}c"
                if session['success'] is not None:
                    output += f" | {'✅ Success' if session['success'] else '❌ Failed'}"
                output += "\n\n"
            
            analytics_text.insert(tk.END, output)
            analytics_text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open analytics: {e}")
        
    def cleanup_on_exit(self):
        """Cleanup resources before exit"""
        try:
            # End current session if active
            if self.current_session_id:
                self.end_crafting_session(notes="Application closed")
            
            # Stop performance monitoring
            if hasattr(self, 'performance_optimizer'):
                self.performance_optimizer.stop_monitoring()
                
            # Save final preferences
            if hasattr(self, 'user_preferences'):
                self.session_tracker.save_preferences(self.user_preferences)
                
            print("Cleanup completed successfully")
            
        except Exception as e:
            print(f"Cleanup error: {e}")
    
    def get_user_ai_preferences(self) -> Dict:
        """Get user preferences for AI optimization"""
        # Get user preferences object if available
        user_prefs = getattr(self, 'user_preferences', None)
        
        return {
            'method_preferences': {
                'chaos_spam': 0.6,
                'alt_regal': 0.7,
                'essence': 0.8,
                'fossil': 0.5
            },
            'risk_tolerance': 0.5,  # Default risk tolerance
            'time_preference': 0.7,  # Prefers faster methods
            'cost_sensitivity': 0.8,   # Cost-conscious
            'preferred_method': getattr(user_prefs, 'preferred_method', 'chaos_spam') if user_prefs else 'chaos_spam',
            'default_budget': getattr(user_prefs, 'default_budget', 1000.0) if user_prefs else 1000.0
        }
    
    def format_ai_plan(self, ai_plan: Dict) -> str:
        """Format AI-generated plan for display"""
        plan = "🤖 AI-ENHANCED CRAFTING PLAN\n"
        plan += "=" * 60 + "\n\n"
        
        # Scenario analysis
        scenario = ai_plan.get('scenario_analysis', {})
        plan += f"🎯 SCENARIO ANALYSIS:\n"
        plan += f"• Complexity Score: {scenario.get('complexity_score', 0):.2f}\n"
        plan += f"• Recommended Strategy: {scenario.get('recommended_strategy', 'unknown').upper()}\n"
        plan += f"• AI Confidence: {scenario.get('confidence_level', 0)*100:.1f}%\n\n"
        
        # Strategy rankings
        rankings = ai_plan.get('strategy_rankings', [])
        if rankings:
            plan += f"📊 AI STRATEGY RANKINGS:\n"
            for i, strategy in enumerate(rankings[:3], 1):
                plan += f"{i}. {strategy['method'].upper()}\n"
                plan += f"   • AI Score: {strategy['score']:.3f}\n"
                plan += f"   • Success Rate: {strategy['success_rate']*100:.1f}%\n"
                plan += f"   • Expected Cost: {strategy['expected_cost']:.1f}c\n\n"
        
        # Budget allocation
        budget_alloc = ai_plan.get('budget_allocation', {})
        if budget_alloc:
            plan += f"💰 OPTIMIZED BUDGET ALLOCATION:\n"
            primary = budget_alloc.get('primary_method', {})
            plan += f"• Primary ({primary.get('method', 'unknown').upper()}): {primary.get('allocated_budget', 0):.1f}c\n"
            plan += f"  Expected Attempts: {primary.get('expected_attempts', 0)}\n"
            plan += f"  Success Probability: {primary.get('success_probability', 0)*100:.1f}%\n"
            
            backup = budget_alloc.get('backup_method', {})
            plan += f"• Backup ({backup.get('method', 'unknown').upper()}): {backup.get('allocated_budget', 0):.1f}c\n"
            
            emergency = budget_alloc.get('emergency_reserve', {})
            plan += f"• Emergency Reserve: {emergency.get('amount', 0):.1f}c\n\n"
        
        # Adaptive plan steps
        adaptive_steps = ai_plan.get('adaptive_plan', [])
        if adaptive_steps:
            plan += f"🔄 ADAPTIVE EXECUTION PLAN:\n"
            plan += "-" * 40 + "\n"
            
            for i, step in enumerate(adaptive_steps, 1):
                phase = step.get('phase', 'unknown').upper()
                plan += f"PHASE {i}: {phase}\n"
                plan += f"Description: {step.get('description', '')}\n"
                
                actions = step.get('actions', [])
                if actions:
                    plan += f"🎯 EXACT ACTIONS TO TAKE:\n"
                    for j, action in enumerate(actions, 1):
                        # Make actions more specific and actionable
                        if 'purchase' in action.lower() or 'acquire' in action.lower():
                            plan += f"  {j}. 🛒 {action.upper()}\n"
                        elif 'use' in action.lower() or 'apply' in action.lower():
                            plan += f"  {j}. ⚡ {action.upper()}\n"
                        elif 'monitor' in action.lower() or 'check' in action.lower():
                            plan += f"  {j}. 👁️ {action.upper()}\n"
                        else:
                            plan += f"  {j}. ✅ {action.upper()}\n"
                
                if 'success_probability' in step:
                    plan += f"Success Rate: {step['success_probability']*100:.1f}%\n"
                if 'budget_required' in step:
                    plan += f"Budget Required: {step['budget_required']:.1f}c\n"
                plan += "\n"
        
        # Risk assessment
        risk = ai_plan.get('risk_assessment', {})
        if risk:
            plan += f"⚠️ RISK ASSESSMENT:\n"
            plan += f"• Primary Risk Level: {risk.get('primary_risk', 0)*100:.1f}%\n"
            plan += f"• Market Volatility: {risk.get('market_volatility_factor', 0)*100:.1f}%\n"
            
            mitigations = risk.get('mitigation_strategies', [])
            if mitigations:
                plan += f"Risk Mitigations:\n"
                for mitigation in mitigations:
                    plan += f"  • {mitigation}\n"
            plan += "\n"
        
        # Add final action summary
        plan += "🎯 FINAL ACTION SUMMARY:\n"
        plan += "-" * 30 + "\n"
        primary_method = ai_plan.get('budget_allocation', {}).get('primary_method', {})
        if primary_method:
            method_name = primary_method.get('method', 'chaos_spam').upper()
            budget = primary_method.get('allocated_budget', 0)
            plan += f"1. 🛒 GO TO MARKET: Buy currency for {method_name} method\n"
            plan += f"2. 💰 SPEND UP TO: {budget:.0f} Chaos Orbs\n"
            plan += f"3. 🎲 USE METHOD: {method_name} until target mods appear\n"
            plan += f"4. ⚠️ STOP WHEN: You see your target modifiers OR budget depleted\n\n"
        
        plan += f"🤖 AI Analysis completed at: {ai_plan.get('generated_at', 'Unknown')}\n"
        plan += f"AI Version: {ai_plan.get('ai_version', '1.0.0')}\n"
        
        return plan
    
    def format_probability_analysis(self, probability_analysis) -> str:
        """Format detailed probability analysis for display"""
        plan = "\n\n📊 ADVANCED PROBABILITY ANALYSIS\n"
        plan += "=" * 60 + "\n\n"
        
        # Overall probability
        plan += f"🎯 SUCCESS PROBABILITY:\n"
        plan += f"• Combined Success Rate: {probability_analysis.combined_probability*100:.4f}%\n"
        plan += f"• Expected Attempts: {probability_analysis.expected_attempts:.1f}\n"
        plan += f"• Best Case Scenario: {probability_analysis.best_case_attempts} attempts\n"
        plan += f"• Worst Case Scenario: {probability_analysis.worst_case_attempts} attempts\n\n"
        
        # Individual modifier probabilities
        if probability_analysis.individual_probabilities:
            plan += f"🔍 INDIVIDUAL MODIFIER PROBABILITIES:\n"
            for mod_name, prob in probability_analysis.individual_probabilities.items():
                plan += f"• {mod_name}: {prob*100:.3f}%\n"
            plan += "\n"
        
        # Cost analysis
        cost_dist = probability_analysis.cost_distribution
        if cost_dist:
            plan += f"💰 COST PROBABILITY DISTRIBUTION:\n"
            plan += f"• Expected Cost: {cost_dist.get('expected_cost', 0):.1f} chaos orbs\n"
            plan += f"• Standard Deviation: {cost_dist.get('standard_deviation', 0):.1f}c\n"
            
            cost_range = cost_dist.get('cost_range_90_percent', (0, 0))
            plan += f"• 90% Confidence Range: {cost_range[0]:.1f}c - {cost_range[1]:.1f}c\n"
            plan += f"• Optimistic Cost: {cost_dist.get('optimistic_cost', 0):.1f}c\n"
            plan += f"• Pessimistic Cost: {cost_dist.get('pessimistic_cost', 0):.1f}c\n\n"
        
        # Confidence interval
        conf_interval = probability_analysis.confidence_interval
        if conf_interval[0] != float('inf'):
            plan += f"📈 CONFIDENCE INTERVALS (95%):\n"
            plan += f"• Attempt Range: {conf_interval[0]:.1f} - {conf_interval[1]:.1f} attempts\n\n"
        
        # Method-specific insights
        plan += f"⚙️ METHOD ANALYSIS ({probability_analysis.method.upper()}):\n"
        if probability_analysis.method == 'chaos_spam':
            plan += f"• Chaos spam provides complete randomness\n"
            plan += f"• Success depends purely on probability mathematics\n"
            plan += f"• Budget should account for high variance\n"
        elif probability_analysis.method == 'alt_regal':
            plan += f"• Alt-regal best for 1-2 specific modifiers\n"
            plan += f"• More predictable cost than chaos spam\n"
            plan += f"• Limited to simpler modifier combinations\n"
        elif probability_analysis.method == 'essence':
            plan += f"• Guarantees at least one modifier\n"
            plan += f"• Higher success rate for compatible modifiers\n"
            plan += f"• More expensive per attempt but more reliable\n"
        elif probability_analysis.method == 'fossil':
            plan += f"• Biases probabilities toward desired outcomes\n"
            plan += f"• Better success rates than pure chaos spam\n"
            plan += f"• Requires specific fossil combinations\n"
        
        plan += "\n📍 PROBABILITY ENGINE: Advanced mathematical modeling using\n"
        plan += "   hypergeometric distributions and Monte Carlo methods\n"
        
        return plan
    
    def _setup_system_dependencies(self):
        """Set up dependencies between intelligence systems"""
        try:
            # Set dependencies for recommendation system
            self.intelligent_recommendations.set_dependencies(
                learning_system=self.learning_system,
                market_intelligence=self.market_intelligence,
                modifier_database=self.enhanced_modifier_db,
                probability_engine=self.probability_engine
            )
            
            # Set dependencies for real-time optimizer
            self.realtime_optimizer.set_dependencies(
                market_intelligence=self.market_intelligence,
                probability_engine=self.probability_engine,
                recommendation_system=self.intelligent_recommendations
            )
            
            print("Intelligence system dependencies configured successfully")
            
        except Exception as e:
            print(f"Error setting up system dependencies: {e}")
    
    def generate_comprehensive_recommendations(self, base_item: str, target_mods: List[str], 
                                             budget: float, ilvl: int) -> str:
        """Generate comprehensive recommendations using all intelligence systems"""
        try:
            from intelligent_recommendations import RecommendationContext
            
            # Create recommendation context
            context = RecommendationContext(
                user_id="default_user",  # Would be actual user ID in production
                current_modifiers=target_mods,
                item_base=base_item,
                item_level=ilvl,
                budget=budget,
                league="Current",
                risk_tolerance=0.5
            )
            
            # Generate comprehensive recommendations
            recommendations = self.intelligent_recommendations.generate_comprehensive_recommendations(context)
            
            # Format recommendations for display
            plan = "\n\n🎯 INTELLIGENT RECOMMENDATIONS\n"
            plan += "=" * 60 + "\n\n"
            
            # Overall strategy
            plan += f"📋 OVERALL STRATEGY: {recommendations.overall_strategy.replace('_', ' ').title()}\n"
            plan += f"🔮 CONFIDENCE SCORE: {recommendations.confidence_score*100:.1f}%\n\n"
            
            # High priority recommendations
            high_priority = [r for r in recommendations.recommendations if r.priority == 'high']
            if high_priority:
                plan += f"🔥 HIGH PRIORITY RECOMMENDATIONS:\n"
                for i, rec in enumerate(high_priority[:3], 1):
                    plan += f"{i}. {rec.title}\n"
                    plan += f"   {rec.description}\n"
                    plan += f"   Confidence: {rec.confidence*100:.0f}%\n"
                    if rec.reasoning:
                        plan += f"   Reasoning: {rec.reasoning[0]}\n"
                    plan += "\n"
            
            # Meta insights
            if recommendations.meta_insights:
                plan += f"📊 META INSIGHTS:\n"
                alignment = recommendations.meta_insights.get('meta_alignment_score', 0)
                plan += f"• Meta Alignment: {alignment*100:.0f}%\n"
                
                trending = recommendations.meta_insights.get('trending_modifiers', [])[:3]
                if trending:
                    plan += f"• Trending Modifiers: {', '.join([mod[0] for mod in trending])}\n"
                plan += "\n"
            
            # Market timing
            if recommendations.market_timing:
                plan += f"📈 MARKET TIMING:\n"
                timing_score = recommendations.market_timing.get('market_timing_score', 0)
                plan += f"• Market Timing Score: {timing_score:.2f}\n"
                optimal_window = recommendations.market_timing.get('optimal_window', 'unknown')
                plan += f"• Optimal Window: {optimal_window.replace('_', ' ').title()}\n"
                plan += "\n"
            
            # User insights
            if recommendations.user_insights:
                plan += f"👤 PERSONALIZATION:\n"
                exp_level = recommendations.user_insights.get('experience_level', 'intermediate')
                plan += f"• Experience Level: {exp_level.title()}\n"
                success_rate = recommendations.user_insights.get('success_rate_history', 0.5)
                plan += f"• Historical Success Rate: {success_rate*100:.0f}%\n"
                confidence = recommendations.user_insights.get('personalization_confidence', 0.3)
                plan += f"• Personalization Confidence: {confidence*100:.0f}%\n"
            
            return plan
            
        except Exception as e:
            return f"\n\n⚠️ Error generating recommendations: {e}\n"
    
    def run(self):
        # Set up cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", lambda: [self.cleanup_on_exit(), self.root.destroy()])
        self.root.mainloop()

if __name__ == "__main__":
    app = IntelligentPOECraftHelper()
    app.run()