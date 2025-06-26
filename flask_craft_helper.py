"""
Flask Crafting Helper - Specialized UI for Flask Crafting
Separate from the main gear/armour crafting interface
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
from typing import List, Dict, Optional
from datetime import datetime
from flask_crafting import FlaskCraftingEngine, FlaskCraftingOptimizer, FlaskType
from market_api import poe_market
from intelligent_ocr import intelligent_ocr
from league_config import get_current_league_name
from config import UI_CONFIG, APP_CONFIG
import logging

logger = logging.getLogger(__name__)


class FlaskCraftHelper:
    """Specialized UI for flask crafting"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"Flask Craft Helper - {get_current_league_name()}")
        self.root.geometry("900x700")
        self.root.attributes('-topmost', UI_CONFIG['topmost'])
        
        # Initialize flask crafting engine
        self.flask_engine = FlaskCraftingEngine()
        self.flask_optimizer = FlaskCraftingOptimizer(self.flask_engine)
        
        # Market API for prices
        self.market_api = poe_market
        self.currency_prices = self.market_api.get_all_currency_prices()
        
        # Flask-specific data
        self.selected_flask_type = tk.StringVar()
        self.selected_modifiers = []
        
        self.setup_ui()
        self.update_prices()
        
    def setup_ui(self):
        """Set up the flask crafting UI"""
        # Title
        title_frame = tk.Frame(self.root, bg='#1a1a1a')
        title_frame.pack(fill='x', pady=5)
        
        title_label = tk.Label(title_frame, text="⚗️ Flask Crafting Specialist", 
                              font=("Arial", 18, "bold"), fg='#00ff88', bg='#1a1a1a')
        title_label.pack()
        
        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Flask selection and modifiers
        left_panel = tk.Frame(main_container, width=400)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Flask type selection
        self._create_flask_type_selector(left_panel)
        
        # Target modifiers selection
        self._create_modifier_selector(left_panel)
        
        # Right panel - Crafting options and results
        right_panel = tk.Frame(main_container, width=400)
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Crafting options
        self._create_crafting_options(right_panel)
        
        # Generate button
        generate_btn = tk.Button(right_panel, text="🔮 Generate Flask Crafting Plan", 
                               command=self.generate_flask_plan,
                               bg='#00ff88', fg='black', font=("Arial", 12, "bold"),
                               height=2)
        generate_btn.pack(fill='x', pady=10)
        
        # Results area
        self._create_results_area(right_panel)
        
        # Bottom controls
        self._create_bottom_controls()
        
    def _create_flask_type_selector(self, parent):
        """Create flask type selection UI"""
        frame = tk.LabelFrame(parent, text="Flask Type", font=("Arial", 11, "bold"))
        frame.pack(fill='x', pady=5)
        
        # Grid of flask types
        flask_grid = tk.Frame(frame)
        flask_grid.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Group flasks by category
        categories = {
            "Recovery": [FlaskType.LIFE, FlaskType.MANA, FlaskType.HYBRID],
            "Defensive": [FlaskType.GRANITE, FlaskType.JADE, FlaskType.BASALT, 
                         FlaskType.BISMUTH, FlaskType.STIBNITE],
            "Offensive": [FlaskType.DIAMOND, FlaskType.SULPHUR, FlaskType.SILVER],
            "Elemental": [FlaskType.RUBY, FlaskType.SAPPHIRE, FlaskType.TOPAZ, 
                         FlaskType.AMETHYST],
            "Utility": [FlaskType.QUICKSILVER, FlaskType.QUARTZ, FlaskType.AQUAMARINE,
                       FlaskType.GOLD]
        }
        
        row = 0
        for category, flasks in categories.items():
            # Category label
            cat_label = tk.Label(flask_grid, text=category, font=("Arial", 10, "bold"),
                               fg='#00ff88')
            cat_label.grid(row=row, column=0, sticky='w', pady=2)
            
            # Flask buttons
            col = 1
            for flask in flasks:
                btn = tk.Radiobutton(flask_grid, text=flask.value.replace(" Flask", ""),
                                   variable=self.selected_flask_type, value=flask.value,
                                   command=self.on_flask_type_changed)
                btn.grid(row=row, column=col, sticky='w', padx=2)
                col += 1
                if col > 3:  # Max 3 per row
                    row += 1
                    col = 1
            row += 1
            
        # Item level input
        ilvl_frame = tk.Frame(frame)
        ilvl_frame.pack(fill='x', padx=5, pady=5)
        tk.Label(ilvl_frame, text="Item Level:").pack(side='left')
        self.ilvl_entry = tk.Entry(ilvl_frame, width=10)
        self.ilvl_entry.insert(0, "85")
        self.ilvl_entry.pack(side='left', padx=5)
        
    def _create_modifier_selector(self, parent):
        """Create modifier selection UI"""
        frame = tk.LabelFrame(parent, text="Target Modifiers", font=("Arial", 11, "bold"))
        frame.pack(fill='both', expand=True, pady=5)
        
        # Instructions
        info_label = tk.Label(frame, text="Select desired flask modifiers:", 
                            font=("Arial", 9), fg='gray')
        info_label.pack(anchor='w', padx=5)
        
        # Modifier categories with tabs
        tab_control = ttk.Notebook(frame)
        tab_control.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Prefix tab
        prefix_frame = tk.Frame(tab_control)
        tab_control.add(prefix_frame, text="Prefixes")
        self._populate_modifiers(prefix_frame, 'prefix')
        
        # Suffix tab
        suffix_frame = tk.Frame(tab_control)
        tab_control.add(suffix_frame, text="Suffixes")
        self._populate_modifiers(suffix_frame, 'suffix')
        
        # Selected modifiers display
        selected_frame = tk.Frame(frame)
        selected_frame.pack(fill='x', padx=5, pady=5)
        tk.Label(selected_frame, text="Selected:", font=("Arial", 9, "bold")).pack(anchor='w')
        self.selected_mods_label = tk.Label(selected_frame, text="None", 
                                          font=("Arial", 9), fg='#00ff88')
        self.selected_mods_label.pack(anchor='w')
        
    def _populate_modifiers(self, parent, mod_type):
        """Populate modifier checkboxes"""
        # Create scrollable frame
        canvas = tk.Canvas(parent, height=200)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Get all modifiers
        all_mods = self.flask_engine.flask_modifiers[mod_type]
        
        # Group by effect type
        grouped = {}
        for mod in all_mods:
            effect_type = "Recovery" if any(tag in ["instant_recovery", "recovery_rate", "recovery_when_hit"] 
                                          for tag in (mod.tags or [])) else \
                         "Immunity" if any(tag in ["bleed_immune", "freeze_immune", "ignite_immune", 
                                                   "shock_immune", "poison_immune", "curse_immune"] 
                                          for tag in (mod.tags or [])) else \
                         "Utility"
            
            if effect_type not in grouped:
                grouped[effect_type] = []
            grouped[effect_type].append(mod)
        
        # Create checkboxes
        self.modifier_vars = {}
        row = 0
        for group_name, mods in grouped.items():
            # Group header
            header = tk.Label(scrollable_frame, text=f"— {group_name} —", 
                            font=("Arial", 10, "bold"), fg='#00ff88')
            header.grid(row=row, column=0, columnspan=2, sticky='w', pady=5)
            row += 1
            
            for mod in mods:
                var = tk.BooleanVar()
                cb = tk.Checkbutton(scrollable_frame, text=mod.name,
                                  variable=var,
                                  command=self.update_selected_modifiers)
                cb.grid(row=row, column=0, sticky='w', padx=20)
                
                # Required level
                level_label = tk.Label(scrollable_frame, text=f"(Lv{mod.required_level})",
                                     font=("Arial", 8), fg='gray')
                level_label.grid(row=row, column=1, sticky='w')
                
                self.modifier_vars[mod.name] = var
                row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def _create_crafting_options(self, parent):
        """Create crafting options UI"""
        frame = tk.LabelFrame(parent, text="Crafting Parameters", font=("Arial", 11, "bold"))
        frame.pack(fill='x', pady=5)
        
        # Budget
        budget_frame = tk.Frame(frame)
        budget_frame.pack(fill='x', padx=5, pady=5)
        tk.Label(budget_frame, text="Budget (chaos):").pack(side='left')
        self.budget_entry = tk.Entry(budget_frame, width=15)
        self.budget_entry.insert(0, "50")
        self.budget_entry.pack(side='left', padx=5)
        
        # Risk tolerance
        risk_frame = tk.Frame(frame)
        risk_frame.pack(fill='x', padx=5, pady=5)
        tk.Label(risk_frame, text="Risk Tolerance:").pack(side='left')
        self.risk_var = tk.StringVar(value="medium")
        for text, value in [("Low", "low"), ("Medium", "medium"), ("High", "high")]:
            tk.Radiobutton(risk_frame, text=text, variable=self.risk_var, 
                          value=value).pack(side='left', padx=5)
        
        # Time preference
        time_frame = tk.Frame(frame)
        time_frame.pack(fill='x', padx=5, pady=5)
        tk.Label(time_frame, text="Time Available:").pack(side='left')
        self.time_var = tk.StringVar(value="medium")
        for text, value in [("Quick", "fast"), ("Normal", "medium"), ("Patient", "slow")]:
            tk.Radiobutton(time_frame, text=text, variable=self.time_var, 
                          value=value).pack(side='left', padx=5)
        
    def _create_results_area(self, parent):
        """Create results display area"""
        frame = tk.LabelFrame(parent, text="Crafting Plan", font=("Arial", 11, "bold"))
        frame.pack(fill='both', expand=True, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(frame, height=15, width=50, 
                                                     font=("Consolas", 10))
        self.results_text.pack(fill='both', expand=True, padx=5, pady=5)
        
    def _create_bottom_controls(self):
        """Create bottom control buttons"""
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Left controls
        left_controls = tk.Frame(control_frame)
        left_controls.pack(side='left')
        
        tk.Button(left_controls, text="📷 Detect Flask", 
                 command=self.detect_flask,
                 bg='#9C27B0', fg='white').pack(side='left', padx=2)
        
        tk.Button(left_controls, text="💱 Update Prices", 
                 command=self.update_prices,
                 bg='#2196F3', fg='white').pack(side='left', padx=2)
        
        tk.Button(left_controls, text="📊 Simulate Craft", 
                 command=self.simulate_crafting,
                 bg='#FF9800', fg='white').pack(side='left', padx=2)
        
        # Right controls
        right_controls = tk.Frame(control_frame)
        right_controls.pack(side='right')
        
        tk.Button(right_controls, text="🗑️ Clear", 
                 command=self.clear_all,
                 bg='#f44336', fg='white').pack(side='left', padx=2)
        
        tk.Button(right_controls, text="💾 Save Plan", 
                 command=self.save_plan,
                 bg='#4CAF50', fg='white').pack(side='left', padx=2)
        
        # Status bar
        self.status_label = tk.Label(self.root, text="Ready", 
                                   font=("Arial", 9), anchor='w', relief='sunken')
        self.status_label.pack(fill='x', side='bottom')
        
    def on_flask_type_changed(self):
        """Handle flask type selection change"""
        flask_type_str = self.selected_flask_type.get()
        if flask_type_str:
            # Update available modifiers based on flask type
            self.status_label.config(text=f"Selected: {flask_type_str}")
            
    def update_selected_modifiers(self):
        """Update the selected modifiers display"""
        selected = [name for name, var in self.modifier_vars.items() if var.get()]
        
        if selected:
            self.selected_mods_label.config(text=", ".join(selected[:3]) + 
                                          ("..." if len(selected) > 3 else ""))
        else:
            self.selected_mods_label.config(text="None")
        
        self.selected_modifiers = selected
        
    def generate_flask_plan(self):
        """Generate comprehensive flask crafting plan"""
        # Validate inputs
        flask_type_str = self.selected_flask_type.get()
        if not flask_type_str:
            messagebox.showerror("Error", "Please select a flask type!")
            return
            
        if not self.selected_modifiers:
            messagebox.showerror("Error", "Please select at least one target modifier!")
            return
            
        try:
            budget = float(self.budget_entry.get())
            ilvl = int(self.ilvl_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid budget or item level!")
            return
            
        # Get flask type enum
        flask_type = self.flask_engine.detect_flask_type(flask_type_str)
        if not flask_type:
            messagebox.showerror("Error", "Invalid flask type!")
            return
            
        # Update optimizer with current prices
        self.flask_optimizer.update_market_prices(self.currency_prices)
        
        # Find optimal strategy
        constraints = {
            'budget': budget,
            'time': self.time_var.get(),
            'risk': self.risk_var.get()
        }
        
        optimal = self.flask_optimizer.find_optimal_strategy(
            flask_type, self.selected_modifiers, constraints
        )
        
        # Display results
        self.display_crafting_plan(flask_type, optimal)
        
    def display_crafting_plan(self, flask_type: FlaskType, strategy: Dict):
        """Display the crafting plan in the results area"""
        self.results_text.delete(1.0, tk.END)
        
        plan = f"{'='*60}\n"
        plan += f"FLASK CRAFTING PLAN - {flask_type.value}\n"
        plan += f"{'='*60}\n\n"
        
        # Recommended strategy
        rec = strategy['recommended']
        plan += f"📌 RECOMMENDED: {rec['name']}\n"
        plan += f"{'─'*40}\n"
        plan += f"💰 Expected Cost: {rec['expected_cost']:.1f} chaos\n"
        plan += f"⏱️ Time Estimate: {rec['time_estimate']}\n"
        plan += f"⚠️ Risk Level: {rec['risk']}\n"
        plan += f"📊 Efficiency Score: {rec['efficiency_score']:.2f}\n\n"
        
        # Detailed steps
        if 'details' in rec and 'steps' in rec['details']:
            plan += "📋 STEPS TO FOLLOW:\n"
            for step in rec['details']['steps']:
                plan += f"  {step}\n"
            plan += "\n"
            
        # Tips
        if 'details' in rec and 'tips' in rec['details']:
            plan += "💡 TIPS:\n"
            for tip in rec['details']['tips']:
                plan += f"  • {tip}\n"
            plan += "\n"
            
        # Alternative strategies
        if strategy['alternatives']:
            plan += f"{'─'*40}\n"
            plan += "🔄 ALTERNATIVE STRATEGIES:\n\n"
            for alt in strategy['alternatives']:
                plan += f"▸ {alt['name']}: {alt['expected_cost']:.1f}c, {alt['time_estimate']}\n"
                
        # Market prices
        plan += f"\n{'─'*40}\n"
        plan += "📈 CURRENT MARKET PRICES:\n"
        relevant_currency = ['Orb of Alteration', 'Orb of Augmentation', 
                           'Glassblowers Bauble', 'Divine Orb']
        for curr in relevant_currency:
            if curr in self.currency_prices:
                plan += f"  {curr}: {self.currency_prices[curr]:.2f}c\n"
                
        self.results_text.insert(1.0, plan)
        self.status_label.config(text="✅ Crafting plan generated successfully!")
        
    def simulate_crafting(self):
        """Run crafting simulation"""
        flask_type_str = self.selected_flask_type.get()
        if not flask_type_str or not self.selected_modifiers:
            messagebox.showerror("Error", "Please select flask type and modifiers first!")
            return
            
        flask_type = self.flask_engine.detect_flask_type(flask_type_str)
        budget = float(self.budget_entry.get() or 50)
        ilvl = int(self.ilvl_entry.get() or 85)
        
        # Run simulation
        result = self.flask_engine.simulate_alteration_crafting(
            flask_type, self.selected_modifiers, budget, ilvl
        )
        
        # Display simulation results
        sim_window = tk.Toplevel(self.root)
        sim_window.title("Crafting Simulation Results")
        sim_window.geometry("500x400")
        
        text = scrolledtext.ScrolledText(sim_window, font=("Consolas", 10))
        text.pack(fill='both', expand=True, padx=10, pady=10)
        
        report = f"SIMULATION RESULTS\n{'='*40}\n\n"
        report += f"Flask Type: {result.flask_type.value}\n"
        report += f"Success: {'✅ YES' if result.success else '❌ NO'}\n"
        report += f"Attempts: {result.attempts}\n"
        report += f"Quality: {result.quality}%\n\n"
        
        report += "COSTS:\n"
        for currency, amount in result.cost.items():
            report += f"  {currency}: {amount}\n"
            
        report += f"\nTOTAL: {sum(result.cost[c] * self.currency_prices.get(c, 1) for c in result.cost):.1f} chaos\n\n"
        
        report += "FINAL MODIFIERS:\n"
        for mod in result.modifiers:
            if mod:
                report += f"  {mod.mod_type}: {mod.name} ({mod.min_roll:.0f}%)\n"
                
        report += "\nFLASK STATS:\n"
        for stat, value in result.final_stats.items():
            if isinstance(value, float):
                report += f"  {stat}: {value:.1f}\n"
            else:
                report += f"  {stat}: {value}\n"
                
        text.insert(1.0, report)
        
    def detect_flask(self):
        """Detect flask from screenshot using OCR"""
        try:
            # Use intelligent OCR to detect item
            detected = intelligent_ocr.detect_item_from_screen()
            
            if detected and 'base' in detected:
                # Check if it's a flask
                flask_type = self.flask_engine.detect_flask_type(detected['base'])
                if flask_type:
                    self.selected_flask_type.set(flask_type.value)
                    self.status_label.config(text=f"✅ Detected: {flask_type.value}")
                    
                    # Parse modifiers if any
                    if 'modifiers' in detected:
                        # Match detected modifiers with our database
                        for mod_text in detected['modifiers']:
                            for name, var in self.modifier_vars.items():
                                if name.lower() in mod_text.lower() or mod_text.lower() in name.lower():
                                    var.set(True)
                        self.update_selected_modifiers()
                else:
                    messagebox.showwarning("Not a Flask", "Detected item is not a flask!")
            else:
                messagebox.showerror("Detection Failed", "Could not detect item from screen!")
                
        except Exception as e:
            logger.error(f"Flask detection error: {e}")
            messagebox.showerror("Error", f"Detection failed: {str(e)}")
            
    def update_prices(self):
        """Update currency prices from market API"""
        try:
            self.currency_prices = self.market_api.get_all_currency_prices()
            self.status_label.config(text="✅ Prices updated successfully!")
        except Exception as e:
            logger.error(f"Price update error: {e}")
            self.status_label.config(text="❌ Failed to update prices")
            
    def clear_all(self):
        """Clear all selections and results"""
        self.selected_flask_type.set("")
        for var in self.modifier_vars.values():
            var.set(False)
        self.selected_modifiers = []
        self.selected_mods_label.config(text="None")
        self.results_text.delete(1.0, tk.END)
        self.budget_entry.delete(0, tk.END)
        self.budget_entry.insert(0, "50")
        self.ilvl_entry.delete(0, tk.END)
        self.ilvl_entry.insert(0, "85")
        self.status_label.config(text="Ready")
        
    def save_plan(self):
        """Save the current crafting plan"""
        plan_text = self.results_text.get(1.0, tk.END).strip()
        if not plan_text:
            messagebox.showwarning("Nothing to Save", "Generate a crafting plan first!")
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"flask_plan_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(plan_text)
            messagebox.showinfo("Saved", f"Plan saved to {filename}")
        except Exception as e:
            messagebox.showerror("Save Failed", f"Could not save plan: {str(e)}")
            
    def run(self):
        """Run the flask crafting helper"""
        self.root.mainloop()


def main():
    """Launch the Flask Craft Helper"""
    app = FlaskCraftHelper()
    app.run()


if __name__ == "__main__":
    main()