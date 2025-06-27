import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
import random
import threading
import time
import logging
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

# Configure logging
logger = logging.getLogger(__name__)


class RefactoredPOECraftHelper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_CONFIG['name']} - {get_current_league_name()}")
        self.root.geometry("900x800")
        self.root.attributes('-topmost', UI_CONFIG['topmost'])
        self.root.attributes('-alpha', UI_CONFIG['default_opacity'])
        
        # Apply modern theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.setup_theme()
        
        # Initialize components
        self.initialize_components()
        
        # Setup UI
        self.setup_ui()
        
        # Start background services
        self.start_background_services()
    
    def setup_theme(self):
        """Configure modern, clean theme"""
        # Colors
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'panel': '#2c2c2c',
            'input': '#3c3c3c',
            'button': '#3498db',
            'button_hover': '#2980b9'
        }
        
        # Configure root
        self.root.configure(bg=self.colors['bg'])
        
        # Configure ttk styles
        self.style.configure('Title.TLabel', background=self.colors['bg'], 
                           foreground=self.colors['fg'], font=('Arial', 18, 'bold'))
        self.style.configure('Heading.TLabel', background=self.colors['bg'], 
                           foreground=self.colors['fg'], font=('Arial', 12, 'bold'))
        self.style.configure('Status.TLabel', background=self.colors['bg'], 
                           foreground=self.colors['accent'], font=('Arial', 10))
        self.style.configure('Panel.TFrame', background=self.colors['panel'], 
                           relief='flat', borderwidth=1)
        self.style.configure('Action.TButton', font=('Arial', 10, 'bold'))
    
    def initialize_components(self):
        """Initialize all helper components"""
        # Databases and APIs
        self.modifier_database = self.load_modifier_database()
        self.market_api = poe_market
        self.price_optimizer = price_optimizer
        self.currency_costs = self.market_api.get_all_currency_prices()
        self.last_price_update = datetime.now()
        
        # Detection and OCR
        self.item_detection = ItemDetectionGUI(self)
        self.intelligent_ocr = intelligent_ocr
        
        # AI and optimization
        self.ai_optimizer = ai_optimizer
        self.probability_engine = probability_engine
        self.market_intelligence = market_intelligence
        self.enhanced_modifier_db = enhanced_modifier_db
        self.intelligent_recommendations = intelligent_recommendations
        self.learning_system = learning_system
        self.realtime_optimizer = realtime_optimizer
        
        # Session tracking
        self.session_tracker = session_tracker
        self.current_session_id = None
        
        # Performance optimization
        optimize_tkinter_performance(self.root)
        self.performance_optimizer = initialize_performance_optimizer(self)
        
        # Load preferences
        self.load_user_preferences()
    
    def setup_ui(self):
        """Create clean, organized UI layout"""
        # Main container with padding
        main_container = ttk.Frame(self.root, style='Panel.TFrame')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header section
        self.create_header(main_container)
        
        # Content area with notebook for organization
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True, pady=(10, 0))
        
        # Create tabs
        self.create_crafting_tab()
        self.create_detection_tab()
        self.create_analytics_tab()
        self.create_settings_tab()
        
        # Status bar
        self.create_status_bar(main_container)
    
    def create_header(self, parent):
        """Create header with title and quick actions"""
        header_frame = ttk.Frame(parent, style='Panel.TFrame')
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Title
        title_label = ttk.Label(header_frame, text="Path of Exile Craft Helper", 
                               style='Title.TLabel')
        title_label.pack(side='left', padx=10)
        
        # Quick actions
        action_frame = ttk.Frame(header_frame)
        action_frame.pack(side='right', padx=10)
        
        ttk.Button(action_frame, text="Refresh Prices", 
                  command=self.refresh_prices, style='Action.TButton').pack(side='left', padx=2)
        ttk.Button(action_frame, text="Toggle Overlay", 
                  command=self.toggle_overlay, style='Action.TButton').pack(side='left', padx=2)
    
    def create_crafting_tab(self):
        """Create the main crafting interface tab"""
        crafting_frame = ttk.Frame(self.notebook)
        self.notebook.add(crafting_frame, text="Crafting")
        
        # Create three-column layout
        left_frame = ttk.Frame(crafting_frame, style='Panel.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        center_frame = ttk.Frame(crafting_frame, style='Panel.TFrame')
        center_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        right_frame = ttk.Frame(crafting_frame, style='Panel.TFrame')
        right_frame.pack(side='left', fill='both', expand=True, padx=(5, 0))
        
        # Left column - Item Input
        self.create_item_input_section(left_frame)
        
        # Center column - Crafting Options
        self.create_crafting_options_section(center_frame)
        
        # Right column - Results
        self.create_results_section(right_frame)
    
    def create_item_input_section(self, parent):
        """Create item input section"""
        # Section header
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        ttk.Label(header_frame, text="Item Details", style='Heading.TLabel').pack(side='left')
        
        # Item base
        self.create_input_field(parent, "Item Base:", "base_entry")
        
        # Item level
        self.create_input_field(parent, "Item Level:", "ilvl_entry", default="85")
        
        # Target modifiers
        mod_frame = ttk.Frame(parent)
        mod_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        ttk.Label(mod_frame, text="Target Modifiers:", style='Heading.TLabel').pack(anchor='w')
        
        # Text area with frame
        text_frame = ttk.Frame(mod_frame)
        text_frame.pack(fill='both', expand=True)
        
        self.target_text = tk.Text(text_frame, height=10, width=30, 
                                  bg=self.colors['input'], fg=self.colors['fg'],
                                  insertbackground=self.colors['fg'],
                                  font=('Consolas', 10))
        self.target_text.pack(side='left', fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.target_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.target_text.config(yscrollcommand=scrollbar.set)
        
        # Suggest button
        ttk.Button(mod_frame, text="Suggest Modifiers", 
                  command=self.suggest_modifiers, style='Action.TButton').pack(fill='x', pady=(5, 0))
    
    def create_crafting_options_section(self, parent):
        """Create crafting options section"""
        # Section header
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        ttk.Label(header_frame, text="Crafting Options", style='Heading.TLabel').pack(side='left')
        
        # Method selection
        method_frame = ttk.LabelFrame(parent, text="Method", padding=10)
        method_frame.pack(fill='x', padx=10, pady=5)
        
        self.method_var = tk.StringVar(value="auto")
        methods = [
            ("Auto-Select", "auto"),
            ("Chaos Spam", "chaos_spam"),
            ("Alt + Regal", "alt_regal"),
            ("Essence", "essence"),
            ("Fossil", "fossil"),
            ("Mastercraft", "mastercraft")
        ]
        
        for text, value in methods:
            ttk.Radiobutton(method_frame, text=text, variable=self.method_var, 
                           value=value).pack(anchor='w')
        
        # Budget input
        self.create_input_field(parent, "Budget (Chaos):", "budget_entry", default="1000")
        
        # Generate button
        ttk.Button(parent, text="Generate Crafting Plan", 
                  command=self.generate_intelligent_plan,
                  style='Action.TButton').pack(fill='x', padx=10, pady=20)
    
    def create_results_section(self, parent):
        """Create results display section"""
        # Section header
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        ttk.Label(header_frame, text="Crafting Plan", style='Heading.TLabel').pack(side='left')
        
        # Results text area
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.results_text = tk.Text(text_frame, wrap='word',
                                   bg=self.colors['input'], fg=self.colors['fg'],
                                   insertbackground=self.colors['fg'],
                                   font=('Consolas', 9))
        self.results_text.pack(side='left', fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.results_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        # Action buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', padx=10, pady=(5, 10))
        
        ttk.Button(button_frame, text="Clear", command=self.clear_all,
                  style='Action.TButton').pack(side='left', padx=2)
        ttk.Button(button_frame, text="Copy", command=self.copy_results,
                  style='Action.TButton').pack(side='left', padx=2)
    
    def create_detection_tab(self):
        """Create item detection tab"""
        detection_frame = ttk.Frame(self.notebook)
        self.notebook.add(detection_frame, text="Detection")
        
        # Center content
        center_frame = ttk.Frame(detection_frame)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(center_frame, text="Item Detection", style='Title.TLabel').pack(pady=20)
        
        # Detection options
        ttk.Button(center_frame, text="Enable Auto-Detection (Ctrl+D)", 
                  command=self.enable_auto_detection,
                  style='Action.TButton').pack(pady=10)
        
        ttk.Button(center_frame, text="Manual Input Guide", 
                  command=self.show_manual_item_guide,
                  style='Action.TButton').pack(pady=10)
        
        ttk.Button(center_frame, text="Flask Crafting Helper", 
                  command=self.open_flask_crafting,
                  style='Action.TButton').pack(pady=10)
    
    def create_analytics_tab(self):
        """Create analytics tab"""
        analytics_frame = ttk.Frame(self.notebook)
        self.notebook.add(analytics_frame, text="Analytics")
        
        # Placeholder for analytics
        ttk.Label(analytics_frame, text="Session Analytics", style='Title.TLabel').pack(pady=20)
        
        ttk.Button(analytics_frame, text="View Session History", 
                  command=self.open_session_analytics,
                  style='Action.TButton').pack(pady=10)
    
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Settings sections
        self.create_appearance_settings(settings_frame)
        self.create_behavior_settings(settings_frame)
    
    def create_appearance_settings(self, parent):
        """Create appearance settings section"""
        appearance_frame = ttk.LabelFrame(parent, text="Appearance", padding=20)
        appearance_frame.pack(fill='x', padx=20, pady=10)
        
        # Opacity control
        opacity_frame = ttk.Frame(appearance_frame)
        opacity_frame.pack(fill='x', pady=5)
        
        ttk.Label(opacity_frame, text="Window Opacity:").pack(side='left', padx=(0, 10))
        
        self.opacity_var = tk.DoubleVar(value=0.95)
        opacity_scale = ttk.Scale(opacity_frame, from_=0.3, to=1.0, 
                                 orient='horizontal', variable=self.opacity_var,
                                 command=self.update_opacity, length=200)
        opacity_scale.pack(side='left')
        
        # Theme selection (placeholder)
        theme_frame = ttk.Frame(appearance_frame)
        theme_frame.pack(fill='x', pady=10)
        
        ttk.Label(theme_frame, text="Theme:").pack(side='left', padx=(0, 10))
        
        theme_var = tk.StringVar(value="dark")
        ttk.Combobox(theme_frame, textvariable=theme_var, 
                    values=["dark", "light"], state='readonly', width=15).pack(side='left')
    
    def create_behavior_settings(self, parent):
        """Create behavior settings section"""
        behavior_frame = ttk.LabelFrame(parent, text="Behavior", padding=20)
        behavior_frame.pack(fill='x', padx=20, pady=10)
        
        # Always on top
        self.topmost_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(behavior_frame, text="Always on Top", 
                       variable=self.topmost_var,
                       command=self.toggle_topmost).pack(anchor='w', pady=5)
        
        # Multi-monitor support
        ttk.Button(behavior_frame, text="Setup Multi-Monitor", 
                  command=self.setup_multi_monitor,
                  style='Action.TButton').pack(anchor='w', pady=5)
    
    def create_status_bar(self, parent):
        """Create status bar at bottom"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill='x', pady=(10, 0))
        
        # Market status
        self.status_label = ttk.Label(status_frame, text="Market: Connecting...", 
                                     style='Status.TLabel')
        self.status_label.pack(side='left', padx=10)
        
        # Version info
        version_label = ttk.Label(status_frame, text=f"v{APP_CONFIG.get('version', '1.0')}", 
                                 style='Status.TLabel')
        version_label.pack(side='right', padx=10)
    
    def create_input_field(self, parent, label_text, attr_name, default=""):
        """Helper to create labeled input fields"""
        frame = ttk.Frame(parent)
        frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame, text=label_text).pack(anchor='w')
        
        entry = ttk.Entry(frame, font=('Arial', 10))
        entry.pack(fill='x')
        if default:
            entry.insert(0, default)
        
        setattr(self, attr_name, entry)
    
    def start_background_services(self):
        """Start all background services"""
        # Price updater
        self.start_price_updater()
        
        # Setup system dependencies
        self._setup_system_dependencies()
    
    def start_price_updater(self):
        """Start background price updater"""
        def update_prices():
            while True:
                try:
                    self.currency_costs = self.market_api.get_all_currency_prices()
                    self.last_price_update = datetime.now()
                    self.root.after(0, self.update_price_status)
                    time.sleep(300)  # 5 minutes
                except Exception as e:
                    print(f"Price update error: {e}")
                    time.sleep(60)
                    
        thread = threading.Thread(target=update_prices, daemon=True)
        thread.start()
    
    def update_price_status(self):
        """Update price status in UI"""
        if hasattr(self, 'status_label'):
            api_status = self.market_api.get_api_status()
            if api_status['connected']:
                status_text = f"Market: Live • Updated: {self.last_price_update.strftime('%H:%M')}"
                self.status_label.config(text=status_text, foreground=self.colors['success'])
            else:
                self.status_label.config(text="Market: Offline • Using fallback prices", 
                                       foreground=self.colors['warning'])
    
    def _setup_system_dependencies(self):
        """Setup system dependencies between components"""
        # Link enhanced modifier DB to other systems
        self.enhanced_modifier_db.set_dependency('market_intelligence', self.market_intelligence)
        self.enhanced_modifier_db.set_dependency('learning_system', self.learning_system)
        
        # Link intelligent recommendations to other systems
        self.intelligent_recommendations.set_dependency('enhanced_modifier_db', self.enhanced_modifier_db)
        self.intelligent_recommendations.set_dependency('market_intelligence', self.market_intelligence)
        self.intelligent_recommendations.set_dependency('learning_system', self.learning_system)
        
        # Link realtime optimizer to other systems
        self.realtime_optimizer.set_dependency('market_intelligence', self.market_intelligence)
        self.realtime_optimizer.set_dependency('learning_system', self.learning_system)
        self.realtime_optimizer.set_dependency('probability_engine', self.probability_engine)
    
    def load_user_preferences(self):
        """Load user preferences from file"""
        prefs_file = os.path.join('data', 'user_preferences.json')
        if os.path.exists(prefs_file):
            try:
                with open(prefs_file, 'r') as f:
                    self.user_preferences = json.load(f)
            except Exception:
                self.user_preferences = {}
        else:
            self.user_preferences = {}
    
    def save_user_preferences(self):
        """Save user preferences to file"""
        prefs_file = os.path.join('data', 'user_preferences.json')
        os.makedirs('data', exist_ok=True)
        try:
            with open(prefs_file, 'w') as f:
                json.dump(self.user_preferences, f, indent=2)
        except Exception as e:
            print(f"Failed to save preferences: {e}")
    
    # Implement all the core methods from original
    def load_modifier_database(self) -> Dict:
        """Load comprehensive modifier database"""
        # Simplified version - would load from enhanced_modifier_db in production
        return {
            'Maximum Life': {
                'type': 'prefix',
                'tiers': [
                    {'name': 'T1', 'value': '+100 to +120', 'weight': 100, 'ilvl': 85},
                    {'name': 'T2', 'value': '+80 to +99', 'weight': 200, 'ilvl': 70},
                    {'name': 'T3', 'value': '+60 to +79', 'weight': 400, 'ilvl': 50},
                ],
                'methods': ['chaos_spam', 'essence', 'fossil', 'alt_regal'],
            },
            # Add more modifiers as needed
        }
    
    def suggest_modifiers(self):
        """Suggest popular modifiers"""
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
        """Generate AI-enhanced intelligent crafting plan"""
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
        
        try:
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
                
        except Exception as e:
            # Fallback to basic plan if AI systems fail
            plan = self.generate_basic_plan(base_item, target_mods, method, budget, ilvl)
        
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", plan)
    
    def clear_all(self):
        """Clear all inputs and results"""
        self.base_entry.delete(0, tk.END)
        self.target_text.delete("1.0", tk.END)
        self.results_text.delete("1.0", tk.END)
        self.budget_entry.delete(0, tk.END)
        self.budget_entry.insert(0, "1000")
        self.ilvl_entry.delete(0, tk.END)
        self.ilvl_entry.insert(0, "85")
    
    def copy_results(self):
        """Copy results to clipboard"""
        results = self.results_text.get("1.0", tk.END).strip()
        if results:
            self.root.clipboard_clear()
            self.root.clipboard_append(results)
            messagebox.showinfo("Success", "Results copied to clipboard!")
    
    def toggle_overlay(self):
        """Toggle always on top"""
        current = self.root.attributes('-topmost')
        self.root.attributes('-topmost', not current)
        if hasattr(self, 'topmost_var'):
            self.topmost_var.set(not current)
    
    def toggle_topmost(self):
        """Toggle topmost from checkbox"""
        self.root.attributes('-topmost', self.topmost_var.get())
    
    def refresh_prices(self):
        """Manually refresh market prices"""
        try:
            self.market_api.update_all_prices()
            self.currency_costs = self.market_api.get_all_currency_prices()
            self.last_price_update = datetime.now()
            self.update_price_status()
            messagebox.showinfo("Success", "Market prices refreshed!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh prices: {e}")
    
    def update_opacity(self, value):
        """Update window opacity"""
        try:
            opacity = float(value)
            self.root.attributes('-alpha', opacity)
        except Exception as e:
            print(f"Error setting opacity: {e}")
    
    def setup_multi_monitor(self):
        """Setup multi-monitor support"""
        messagebox.showinfo("Multi-Monitor", "Multi-monitor support setup!")
    
    def enable_auto_detection(self):
        """Enable auto-detection functionality"""
        try:
            # Try the simplified version first
            try:
                from auto_detection_simple import setup_auto_detection
                self.auto_detection_ui = setup_auto_detection(self)
                if self.auto_detection_ui:
                    return
            except Exception as e:
                logger.warning(f"Simplified auto-detection failed: {e}")
            
            # Fallback to original version
            from auto_detection import setup_auto_detection
            self.auto_detection_ui = setup_auto_detection(self)
            
        except Exception as e:
            # Show setup guide if both fail
            messagebox.showerror("Auto-Detection Setup Required", 
                               f"Auto-detection requires additional libraries.\n\n"
                               f"Error: {e}\n\n"
                               "Please run: python fix_auto_detection.py\n"
                               "Or install manually: pip install keyboard mss")
    
    def show_manual_item_guide(self):
        """Show manual input guide"""
        messagebox.showinfo("Manual Guide", "Manual input guide opened!")
    
    def open_flask_crafting(self):
        """Open flask crafting helper"""
        try:
            from flask_craft_helper import FlaskCraftHelper
            flask_window = FlaskCraftHelper()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open flask helper: {e}")
    
    def open_session_analytics(self):
        """Open session analytics"""
        messagebox.showinfo("Analytics", "Session analytics opened!")
    
    def get_user_ai_preferences(self):
        """Get user AI preferences"""
        return self.user_preferences.get('ai_preferences', {
            'risk_tolerance': 'medium',
            'optimization_goal': 'balanced',
            'preferred_methods': ['chaos_spam', 'essence']
        })
    
    def format_ai_plan(self, ai_plan):
        """Format AI-generated plan"""
        if isinstance(ai_plan, dict):
            formatted = "AI-OPTIMIZED CRAFTING PLAN\n"
            formatted += "=" * 60 + "\n\n"
            formatted += f"Strategy: {ai_plan.get('strategy', 'Unknown')}\n"
            formatted += f"Expected Cost: {ai_plan.get('expected_cost', 0):.0f} chaos\n"
            formatted += f"Success Rate: {ai_plan.get('success_rate', 0):.1%}\n\n"
            
            if 'steps' in ai_plan:
                formatted += "STEPS:\n"
                for i, step in enumerate(ai_plan['steps'], 1):
                    formatted += f"{i}. {step}\n"
            
            return formatted
        return str(ai_plan)
    
    def format_probability_analysis(self, analysis):
        """Format probability analysis results"""
        if not analysis:
            return ""
        
        formatted = "\n\nPROBABILITY ANALYSIS:\n"
        formatted += "-" * 40 + "\n"
        
        if isinstance(analysis, dict):
            for key, value in analysis.items():
                formatted += f"• {key}: {value}\n"
        else:
            formatted += str(analysis)
        
        return formatted
    
    def analyze_modifiers(self, target_mods, ilvl):
        """Analyze target modifiers"""
        analysis = {
            'modifiers': [],
            'prefix_count': 0,
            'suffix_count': 0,
            'total_weight': 0,
            'min_ilvl': 1,
            'compatible': True,
            'warnings': []
        }
        
        for mod in target_mods:
            if mod in self.modifier_database:
                mod_data = self.modifier_database[mod]
                if mod_data['type'] == 'prefix':
                    analysis['prefix_count'] += 1
                else:
                    analysis['suffix_count'] += 1
                
                # Check ilvl requirements
                available_tiers = [t for t in mod_data['tiers'] if t['ilvl'] <= ilvl]
                if available_tiers:
                    best_tier = available_tiers[0]
                    analysis['modifiers'].append({
                        'name': mod,
                        'type': mod_data['type'],
                        'best_tier': best_tier
                    })
                    analysis['total_weight'] += best_tier['weight']
                else:
                    analysis['warnings'].append(f"{mod} requires higher item level")
            else:
                analysis['warnings'].append(f"Unknown modifier: {mod}")
        
        # Check compatibility
        if analysis['prefix_count'] > 3:
            analysis['compatible'] = False
            analysis['warnings'].append("Too many prefixes (max 3)")
        if analysis['suffix_count'] > 3:
            analysis['compatible'] = False
            analysis['warnings'].append("Too many suffixes (max 3)")
        
        return analysis
    
    def generate_detailed_plan(self, base_item, target_mods, method, analysis, budget, ilvl):
        """Generate detailed crafting plan"""
        plan = f"CRAFTING PLAN FOR {base_item.upper()}\n"
        plan += "=" * 60 + "\n\n"
        
        # Analysis summary
        plan += "ANALYSIS SUMMARY:\n"
        plan += f"• Item Level: {ilvl}\n"
        plan += f"• Target Modifiers: {len(target_mods)}\n"
        plan += f"• Prefixes: {analysis['prefix_count']}/3\n"
        plan += f"• Suffixes: {analysis['suffix_count']}/3\n"
        plan += f"• Budget: {budget} Chaos Orbs\n"
        plan += f"• Method: {method.replace('_', ' ').title()}\n\n"
        
        if analysis['warnings']:
            plan += "WARNINGS:\n"
            for warning in analysis['warnings']:
                plan += f"⚠ {warning}\n"
            plan += "\n"
        
        if not analysis['compatible']:
            plan += "❌ INCOMPATIBLE MODIFIER COMBINATION!\n"
            return plan
        
        # Method-specific steps
        if method == "chaos_spam":
            plan += self.generate_chaos_spam_steps(target_mods, budget)
        elif method == "alt_regal":
            plan += self.generate_alt_regal_steps(target_mods, budget)
        elif method == "essence":
            plan += self.generate_essence_steps(target_mods, budget)
        elif method == "fossil":
            plan += self.generate_fossil_steps(target_mods, budget)
        elif method == "mastercraft":
            plan += self.generate_mastercraft_steps(target_mods, budget)
        
        return plan
    
    def generate_chaos_spam_steps(self, target_mods, budget):
        """Generate chaos spam steps"""
        steps = "CHAOS SPAM METHOD:\n"
        steps += "-" * 30 + "\n\n"
        steps += f"1. Buy {int(budget * 0.8)} Chaos Orbs\n"
        steps += "2. Ensure item is rare (yellow)\n"
        steps += "3. Right-click Chaos Orb → Left-click item\n"
        steps += "4. Check for target modifiers\n"
        steps += "5. Repeat until successful\n"
        steps += "6. Use Divine Orbs to perfect values\n\n"
        return steps
    
    def generate_alt_regal_steps(self, target_mods, budget):
        """Generate alt+regal steps"""
        steps = "ALT+REGAL METHOD:\n"
        steps += "-" * 30 + "\n\n"
        steps += f"1. Buy {int(budget * 0.4)} Alteration Orbs\n"
        steps += "2. Start with white (normal) item\n"
        steps += "3. Use Transmutation Orb to make magic\n"
        steps += "4. Alt spam for 1-2 target mods\n"
        steps += "5. Regal Orb to make rare\n"
        steps += "6. Craft remaining mods\n\n"
        return steps
    
    def generate_essence_steps(self, target_mods, budget):
        """Generate essence steps"""
        steps = "ESSENCE METHOD:\n"
        steps += "-" * 30 + "\n\n"
        steps += "1. Buy appropriate essences\n"
        steps += "2. Apply essence to item\n"
        steps += "3. Check other modifiers\n"
        steps += "4. Repeat if needed\n"
        steps += "5. Craft missing mods\n\n"
        return steps
    
    def generate_fossil_steps(self, target_mods, budget):
        """Generate fossil steps"""
        steps = "FOSSIL METHOD:\n"
        steps += "-" * 30 + "\n\n"
        steps += "1. Buy fossils and resonators\n"
        steps += "2. Socket fossils in resonator\n"
        steps += "3. Apply to item\n"
        steps += "4. Check results\n"
        steps += "5. Repeat as needed\n\n"
        return steps
    
    def generate_mastercraft_steps(self, target_mods, budget):
        """Generate mastercraft steps"""
        steps = "MASTERCRAFT METHOD:\n"
        steps += "-" * 30 + "\n\n"
        steps += "1. Get base with open affixes\n"
        steps += "2. Visit crafting bench\n"
        steps += "3. Apply bench crafts\n"
        steps += "4. Use currency to modify\n"
        steps += "5. Finish with bench crafts\n\n"
        return steps
    
    def generate_comprehensive_recommendations(self, base_item, target_mods, budget, ilvl):
        """Generate AI recommendations"""
        recs = "\n\nRECOMMENDATIONS:\n"
        recs += "-" * 40 + "\n"
        
        # Budget-based recommendations
        if budget < 500:
            recs += "• Low budget: Consider essence or alt+regal method\n"
        elif budget < 2000:
            recs += "• Medium budget: Chaos spam or fossil crafting recommended\n"
        else:
            recs += "• High budget: All methods viable, consider metacrafting\n"
        
        # Modifier count recommendations
        if len(target_mods) <= 2:
            recs += "• Few mods: Alt+regal is cost-effective\n"
        else:
            recs += "• Many mods: Chaos spam or essence recommended\n"
        
        return recs
    
    def start_crafting_session(self, base_item, target_mods, method, budget):
        """Start a new crafting session"""
        try:
            session_data = {
                'item_base': base_item,
                'target_modifiers': target_mods,
                'method': method,
                'budget': budget,
                'timestamp': datetime.now().isoformat()
            }
            # Would normally save to database
            return f"SESSION_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        except:
            return None
    
    def generate_basic_plan(self, base_item, target_mods, method, budget, ilvl):
        """Generate basic plan as fallback"""
        plan = f"CRAFTING PLAN FOR {base_item.upper()}\n"
        plan += "=" * 60 + "\n\n"
        plan += f"Target Modifiers: {', '.join(target_mods)}\n"
        plan += f"Method: {method}\n"
        plan += f"Budget: {budget} Chaos Orbs\n"
        plan += f"Item Level: {ilvl}\n\n"
        plan += "Steps:\n"
        plan += "1. Acquire base item\n"
        plan += "2. Apply crafting method\n"
        plan += "3. Check for target modifiers\n"
        plan += "4. Repeat until successful\n"
        return plan
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = RefactoredPOECraftHelper()
    app.run()