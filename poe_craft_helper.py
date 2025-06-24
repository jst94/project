import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
import random
from typing import List, Dict, Tuple, Optional

class IntelligentPOECraftHelper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Intelligent PoE Craft Helper - League 3.26")
        self.root.geometry("800x700")
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.95)
        
        # Comprehensive modifier database
        self.modifier_database = self.load_modifier_database()
        
        # Currency costs (in chaos orbs)
        self.currency_costs = {
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
            'Essence': 5.0,  # Average essence cost
            'Fossil': 3.0,   # Average fossil cost
            'Resonator': 2.0 # Average resonator cost
        }
        
        self.setup_ui()
        
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
        tk.Button(generate_frame, text="Generate Intelligent Crafting Plan", 
                 command=self.generate_intelligent_plan, bg='#2E86AB', fg='white',
                 font=("Arial", 12, "bold")).pack(fill='x')
        
        # Results display
        results_frame = tk.Frame(self.root)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        tk.Label(results_frame, text="Intelligent Crafting Plan:", font=("Arial", 12, "bold")).pack(anchor='w')
        self.results_text = scrolledtext.ScrolledText(results_frame, height=20, width=80, font=("Consolas", 9))
        self.results_text.pack(fill='both', expand=True)
        
        # Control buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill='x', padx=10, pady=5)
        tk.Button(control_frame, text="Clear All", command=self.clear_all, 
                 bg='#f44336', fg='white').pack(side='left')
        tk.Button(control_frame, text="Toggle Overlay", 
                 command=self.toggle_overlay).pack(side='right')
        
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
        """Generate an intelligent crafting plan"""
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
            
        # Analyze modifiers
        modifier_analysis = self.analyze_modifiers(target_mods, ilvl)
        
        # Select best method if auto
        if method == "auto":
            method = self.select_best_method(modifier_analysis, budget)
            
        # Generate detailed plan
        plan = self.generate_detailed_plan(base_item, target_mods, method, modifier_analysis, budget, ilvl)
        
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
        """Select the best crafting method based on analysis"""
        if not analysis['compatible']:
            return "chaos_spam"  # Fallback
            
        mod_count = len(analysis['modifiers'])
        total_weight = analysis['total_weight']
        
        # For 1-2 specific modifiers, alt+regal is often best
        if mod_count <= 2 and total_weight < 1000:
            return "alt_regal"
            
        # For 3+ modifiers, essence or fossil might be better
        if mod_count >= 3:
            if budget > 500:  # High budget
                return "essence"
            else:
                return "fossil"
                
        # Default to chaos spam for complex cases
        return "chaos_spam"
        
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
        elif method == "mastercraft":
            plan += self.generate_mastercraft_plan(target_mods, analysis, budget)
            
        # Cost estimation
        plan += self.estimate_costs(method, analysis, budget)
        
        # Success probability
        plan += self.calculate_success_probability(method, analysis)
        
        # Alternative suggestions
        plan += self.suggest_alternatives(target_mods, analysis)
        
        return plan
        
    def generate_chaos_spam_plan(self, target_mods: List[str], analysis: Dict, budget: float) -> str:
        """Generate chaos spam crafting plan"""
        plan = "CHAOS SPAM METHOD:\n"
        plan += "-" * 30 + "\n\n"
        
        plan += "STEP-BY-STEP PROCESS:\n"
        plan += "1. Obtain a rare base item with item level ≥ {analysis['min_ilvl']}\n"
        plan += "2. Ensure item has 6 affixes (3 prefix, 3 suffix)\n"
        plan += "3. Use Chaos Orbs repeatedly until desired modifiers appear\n"
        plan += "4. Use Divine Orbs to perfect numeric values\n"
        plan += "5. Use Annulment Orbs to remove unwanted modifiers if needed\n\n"
        
        plan += "TARGET MODIFIERS:\n"
        for i, mod in enumerate(analysis['modifiers'], 1):
            tier = mod['best_tier']
            plan += f"  {i}. {mod['name']} ({tier['name']}: {tier['value']})\n"
        plan += "\n"
        
        plan += "TIPS:\n"
        plan += "• Have at least 200-500 Chaos Orbs ready\n"
        plan += "• Use item filters to highlight good bases\n"
        plan += "• Consider using Awakener's Orb for influenced items\n"
        plan += "• Be patient - this method is heavily RNG dependent\n\n"
        
        return plan
        
    def generate_alt_regal_plan(self, target_mods: List[str], analysis: Dict, budget: float) -> str:
        """Generate alt+regal crafting plan"""
        plan = "ALTERATION + REGAL METHOD:\n"
        plan += "-" * 30 + "\n\n"
        
        plan += "STEP-BY-STEP PROCESS:\n"
        plan += "1. Start with a white (normal) base item\n"
        plan += "2. Use Orb of Transmutation to make it magic\n"
        plan += "3. Use Alteration Orbs to roll desired prefix/suffix\n"
        plan += "4. Use Augmentation Orb if item has only 1 modifier\n"
        plan += "5. Use Regal Orb to upgrade to rare\n"
        plan += "6. Continue with Exalted Orbs for additional modifiers\n"
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
        plan += "• More cost-effective for specific modifiers\n\n"
        
        return plan
        
    def generate_essence_plan(self, target_mods: List[str], analysis: Dict, budget: float) -> str:
        """Generate detailed essence crafting plan with automatic essence detection"""
        plan = "ESSENCE CRAFTING METHOD:\n"
        plan += "-" * 30 + "\n\n"
        
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
        
    def generate_mastercraft_plan(self, target_mods: List[str], analysis: Dict, budget: float) -> str:
        """Generate mastercraft plan"""
        plan = "MASTERCRAFT METHOD:\n"
        plan += "-" * 30 + "\n\n"
        
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
        """Estimate crafting costs"""
        plan = "COST ESTIMATION:\n"
        plan += "-" * 20 + "\n"
        
        if method == "chaos_spam":
            estimated_cost = 200 + (analysis['total_weight'] * 0.5)
            plan += f"• Estimated Chaos Orbs needed: {estimated_cost:.0f}\n"
            plan += f"• Additional Divine Orbs: {max(1, len(analysis['modifiers']) // 2)}\n"
            plan += f"• Additional Annulment Orbs: {len(analysis['modifiers'])}\n"
            
        elif method == "alt_regal":
            estimated_cost = 50 + (analysis['total_weight'] * 0.2)
            plan += f"• Estimated Alteration Orbs: {estimated_cost:.0f}\n"
            plan += f"• Regal Orbs: {len(analysis['modifiers'])}\n"
            plan += f"• Exalted Orbs: {len(analysis['modifiers']) - 1}\n"
            
        elif method == "essence":
            estimated_cost = len(analysis['modifiers']) * 50
            plan += f"• Essence costs: {estimated_cost} chaos\n"
            plan += f"• Additional Chaos Orbs: 100\n"
            
        elif method == "fossil":
            estimated_cost = len(analysis['modifiers']) * 30
            plan += f"• Fossil costs: {estimated_cost} chaos\n"
            plan += f"• Resonator costs: {len(analysis['modifiers']) * 10} chaos\n"
            
        else:
            estimated_cost = 100
            plan += f"• Base crafting costs: {estimated_cost} chaos\n"
            
        plan += f"• Total estimated cost: {estimated_cost:.0f} chaos\n"
        
        if estimated_cost > budget:
            plan += f"⚠ WARNING: Estimated cost ({estimated_cost:.0f}) exceeds budget ({budget})\n"
        else:
            plan += f"✅ Budget sufficient for this method\n"
            
        plan += "\n"
        return plan
        
    def calculate_success_probability(self, method: str, analysis: Dict) -> str:
        """Calculate success probability"""
        plan = "SUCCESS PROBABILITY:\n"
        plan += "-" * 20 + "\n"
        
        total_weight = analysis['total_weight']
        mod_count = len(analysis['modifiers'])
        
        if method == "chaos_spam":
            # Rough probability calculation
            base_prob = 1.0
            for mod in analysis['modifiers']:
                prob = mod['weight'] / 10000  # Rough estimate
                base_prob *= prob
            success_rate = base_prob * 100
            plan += f"• Getting all {mod_count} modifiers: {success_rate:.4f}%\n"
            plan += f"• Expected attempts: {1/success_rate*100:.0f} chaos orbs\n"
            
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
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = IntelligentPOECraftHelper()
    app.run()