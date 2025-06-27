#!/usr/bin/env python
"""
POE Craft Helper Launcher
Allows choosing between different UI versions
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import subprocess


class LauncherWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("POE Craft Helper Launcher")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"+{x}+{y}")
        
        # Apply modern dark theme
        self.setup_theme()
        
        # Create UI
        self.create_ui()
    
    def setup_theme(self):
        """Setup dark theme"""
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#3498db',
            'success': '#2ecc71',
            'hover': '#2980b9',
            'panel': '#2c2c2c'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', 
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       font=('Arial', 20, 'bold'))
        
        style.configure('Description.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['fg'],
                       font=('Arial', 10))
        
        style.configure('Version.TFrame',
                       background=self.colors['panel'],
                       relief='flat',
                       borderwidth=2)
    
    def create_ui(self):
        """Create launcher UI"""
        # Title
        title_label = ttk.Label(self.root, text="POE Craft Helper", style='Title.TLabel')
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(self.root, text="Choose your preferred interface", 
                                  style='Description.TLabel')
        subtitle_label.pack(pady=(0, 30))
        
        # Version buttons
        self.create_version_button(
            "Refactored Version (Recommended)",
            "Clean, modern interface with improved organization",
            self.launch_refactored,
            is_recommended=True
        )
        
        self.create_version_button(
            "Original Version",
            "Classic interface with all features",
            self.launch_original
        )
        
        self.create_version_button(
            "Simple Version",
            "Lightweight interface for basic crafting",
            self.launch_simple
        )
        
        # Exit button
        exit_button = tk.Button(self.root, text="Exit", command=self.root.quit,
                               bg=self.colors['accent'], fg=self.colors['fg'],
                               font=('Arial', 10), bd=0, padx=20, pady=5)
        exit_button.pack(pady=20)
    
    def create_version_button(self, title, description, command, is_recommended=False):
        """Create a version selection button"""
        frame = tk.Frame(self.root, bg=self.colors['panel'], bd=1, relief='solid')
        frame.pack(fill='x', padx=40, pady=10)
        
        # Make the entire frame clickable
        frame.bind("<Button-1>", lambda e: command())
        
        # Title with recommendation badge
        title_frame = tk.Frame(frame, bg=self.colors['panel'])
        title_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        title_label = tk.Label(title_frame, text=title, 
                              bg=self.colors['panel'], fg=self.colors['fg'],
                              font=('Arial', 12, 'bold'))
        title_label.pack(side='left')
        title_label.bind("<Button-1>", lambda e: command())
        
        if is_recommended:
            badge = tk.Label(title_frame, text="RECOMMENDED", 
                            bg=self.colors['success'], fg='white',
                            font=('Arial', 8, 'bold'), padx=5, pady=2)
            badge.pack(side='left', padx=10)
        
        # Description
        desc_label = tk.Label(frame, text=description,
                             bg=self.colors['panel'], fg=self.colors['fg'],
                             font=('Arial', 9), wraplength=400, justify='left')
        desc_label.pack(fill='x', padx=10, pady=(0, 10))
        desc_label.bind("<Button-1>", lambda e: command())
        
        # Hover effect
        def on_enter(e):
            frame.configure(bg=self.colors['hover'])
            for widget in frame.winfo_children():
                widget.configure(bg=self.colors['hover'])
                for child in widget.winfo_children():
                    if not isinstance(child, tk.Label) or child.cget('text') != 'RECOMMENDED':
                        child.configure(bg=self.colors['hover'])
        
        def on_leave(e):
            frame.configure(bg=self.colors['panel'])
            for widget in frame.winfo_children():
                widget.configure(bg=self.colors['panel'])
                for child in widget.winfo_children():
                    if not isinstance(child, tk.Label) or child.cget('text') != 'RECOMMENDED':
                        child.configure(bg=self.colors['panel'])
        
        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)
    
    def launch_refactored(self):
        """Launch refactored version"""
        self.launch_version("poe_craft_helper_refactored.py")
    
    def launch_original(self):
        """Launch original version"""
        self.launch_version("poe_craft_helper.py")
    
    def launch_simple(self):
        """Launch simple version"""
        self.launch_version("poe_craft_helper_simple.py")
    
    def launch_version(self, filename):
        """Launch a specific version"""
        try:
            # Close launcher
            self.root.withdraw()
            
            # Launch the selected version
            if sys.platform == "win32":
                subprocess.Popen([sys.executable, filename], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([sys.executable, filename])
            
            # Exit launcher
            self.root.quit()
            
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("Launch Error", f"Failed to launch: {e}")
    
    def run(self):
        """Run the launcher"""
        self.root.mainloop()


if __name__ == "__main__":
    launcher = LauncherWindow()
    launcher.run()