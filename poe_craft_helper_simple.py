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
from session_tracker import session_tracker
from performance_optimizer import initialize_performance_optimizer, optimize_tkinter_performance

class SimplePOECraftHelper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple PoE Craft Helper - League 3.26")
        self.root.geometry("800x700")
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.95)
        
        # Comprehensive modifier database
        self.modifier_database = self.load_modifier_database()
        
        # Dynamic currency costs (updated from market API)
        self.market_api = poe_market
        self.price_optimizer = price_optimizer
        self.currency_costs = self.market_api.get_all_currency_prices()
        self.last_price_update = datetime.now()
        
        # Start price update timer
        self.start_price_updater()
        
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
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="Simple PoE Craft Helper", 
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
        self.ilvl_entry.insert(0, "85")
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
        self.budget_entry.insert(0, "1000")
        self.budget_entry.pack(fill='x')
        
        # Generate button
        generate_frame = tk.Frame(right_panel)
        generate_frame.pack(fill='x', pady=10)
        tk.Button(generate_frame, text="Generate Crafting Plan", 
                 command=self.generate_plan, bg='#2E86AB', fg='white',
                 font=("Arial", 12, "bold")).pack(fill='x')
        
        # Results display
        results_frame = tk.Frame(self.root)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        tk.Label(results_frame, text="Crafting Plan:", font=("Arial", 12, "bold")).pack(anchor='w')
        self.results_text = scrolledtext.ScrolledText(results_frame, height=20, width=80, font=("Consolas", 9))
        self.results_text.pack(fill='both', expand=True)
        
        # Control buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(control_frame, text="Clear All", command=self.clear_all, 
                 bg='#f44336', fg='white').pack(side='left', padx=2)
        tk.Button(control_frame, text="Refresh Prices", command=self.refresh_prices,
                 bg='#2196F3', fg='white').pack(side='left', padx=2)
        tk.Button(control_frame, text="Toggle Overlay", 
                 command=self.toggle_overlay).pack(side='right', padx=2)
        
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
        
    def generate_plan(self):
        """Generate a crafting plan"""
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
        
        # Simple plan generation
        plan = f"CRAFTING PLAN FOR {base_item.upper()}\n"
        plan += "="*50 + "\n\n"
        plan += f"Item Level: {ilvl}\n"
        plan += f"Target Modifiers: {len(target_mods)}\n"
        plan += f"Budget: {budget} Chaos Orbs\n"
        plan += f"Method: {method.upper()}\n\n"
        
        plan += "TARGET MODIFIERS:\n"
        for i, mod in enumerate(target_mods, 1):
            normalized = self.normalize_modifier_name(mod)
            plan += f"  {i}. {normalized}\n"
        plan += "\n"
        
        plan += "RECOMMENDED STEPS:\n"
        if method == "chaos_spam":
            plan += "1. Use Chaos Orbs on rare base item\n"
            plan += "2. Repeat until desired modifiers appear\n"
            plan += "3. Use Divine Orbs to perfect values\n"
        elif method == "essence":
            plan += "1. Use appropriate essences on base item\n"
            plan += "2. Essences guarantee specific modifiers\n"
            plan += "3. Use Exalted Orbs for additional mods\n"
        else:
            plan += "1. Follow standard crafting methods\n"
            plan += "2. Use appropriate currency orbs\n"
            plan += "3. Perfect with Divine Orbs\n"
        
        plan += "\nEstimated Cost: " + str(budget * 0.8) + " - " + str(budget * 1.2) + " chaos orbs\n"
        
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", plan)
        
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
    
    def load_user_preferences(self):
        """Load and apply user preferences"""
        try:
            prefs = self.session_tracker.preferences
            self.user_preferences = prefs
        except Exception as e:
            print(f"Error loading preferences: {e}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SimplePOECraftHelper()
    app.run() 