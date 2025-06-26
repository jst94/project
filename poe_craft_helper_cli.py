#!/usr/bin/env python3

import os
import sys
from league_config import get_current_league_name

class POECraftHelperCLI:
    def __init__(self):
        self.currencies = {
            'Orb of Alchemy': 'Upgrades normal item to rare',
            'Orb of Chance': 'Upgrades normal item to magic/rare/unique',
            'Orb of Alteration': 'Rerolls magic item modifiers',
            'Orb of Augmentation': 'Adds modifier to magic item',
            'Regal Orb': 'Upgrades magic item to rare',
            'Chaos Orb': 'Rerolls rare item modifiers',
            'Exalted Orb': 'Adds modifier to rare item',
            'Orb of Annulment': 'Removes random modifier',
            'Divine Orb': 'Rerolls numeric values of modifiers',
            'Eternal Orb': 'Creates imprint of item',
            'Orb of Scouring': 'Removes all modifiers'
        }
        
        self.methods = {
            '1': ('Chaos Spam', 'chaos_spam'),
            '2': ('Alt + Regal', 'alt_regal'),
            '3': ('Essence Crafting', 'essence'),
            '4': ('Fossil Crafting', 'fossil'),
            '5': ('Mastercraft', 'mastercraft')
        }
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        print("=" * 50)
        print(f"    PATH OF EXILE CRAFT HELPER - {get_current_league_name().upper()}")
        print("=" * 50)
        print()
    
    def get_item_base(self):
        print("Enter your item base (e.g., 'Titanium Spirit Shield'):")
        base = input("> ").strip()
        return base if base else None
    
    def get_target_modifiers(self):
        print("\nEnter target modifiers (one per line, empty line to finish):")
        mods = []
        while True:
            mod = input(f"Modifier {len(mods) + 1}: ").strip()
            if not mod:
                break
            mods.append(mod)
        return mods
    
    def select_method(self):
        print("\nSelect crafting method:")
        for key, (name, _) in self.methods.items():
            print(f"{key}. {name}")
        
        while True:
            choice = input("\nEnter method number (1-5): ").strip()
            if choice in self.methods:
                return self.methods[choice][1]
            print("Invalid choice. Please enter 1-5.")
    
    def calculate_steps(self, base_item, target_mods, method):
        steps = []
        steps.append(f"CRAFTING STEPS FOR: {base_item.upper()}")
        steps.append("=" * 60)
        steps.append("")
        
        if method == "chaos_spam":
            steps.extend([
                "🔥 CHAOS SPAM METHOD:",
                "",
                "STEPS:",
                "1. Obtain a rare base item (use Orb of Alchemy if needed)",
                "2. Prepare a large stack of Chaos Orbs (50-500+)",
                "3. Use Chaos Orbs repeatedly until desired modifiers appear",
                "4. Be patient - this method is RNG dependent",
                "",
                "COST ESTIMATE: 50-500+ Chaos Orbs",
                "DIFFICULTY: Easy (but expensive)",
                "SUCCESS RATE: Variable (pure RNG)",
                ""
            ])
            
        elif method == "alt_regal":
            steps.extend([
                "⚡ ALTERATION + REGAL METHOD:",
                "",
                "STEPS:",
                "1. Start with a white (normal) base item",
                "2. Use Orb of Transmutation to make it magic (blue)",
                "3. Use Orb of Alteration to reroll until you get 1-2 desired mods",
                "4. Use Orb of Augmentation if item has only 1 modifier",
                "5. Use Regal Orb to upgrade magic item to rare",
                "6. Continue crafting with Exalted Orbs or other methods",
                "",
                "COST ESTIMATE: 50-200 Alterations + 1 Regal + extras",
                "DIFFICULTY: Medium",
                "SUCCESS RATE: Good for targeting specific modifiers",
                ""
            ])
            
        elif method == "essence":
            steps.extend([
                "💎 ESSENCE CRAFTING METHOD:",
                "",
                "STEPS:",
                "1. Identify which essence provides your desired modifier",
                "2. Obtain the relevant essence (check PoE wiki for specifics)",
                "3. Use essence on your base item (guarantees specific modifier)",
                "4. If result is unsatisfactory, use Chaos Orbs or start over",
                "5. Use Exalted Orbs to add more modifiers if needed",
                "",
                "COST ESTIMATE: Essence cost + potential chaos/exalts",
                "DIFFICULTY: Medium",
                "SUCCESS RATE: High (guarantees at least one desired mod)",
                ""
            ])
            
        elif method == "fossil":
            steps.extend([
                "🗿 FOSSIL CRAFTING METHOD:",
                "",
                "STEPS:",
                "1. Research which fossils bias toward your desired modifiers",
                "2. Obtain relevant fossils and appropriate resonators",
                "3. Socket fossils into resonator",
                "4. Use resonator on your base item",
                "5. Repeat until satisfied with results",
                "",
                "COST ESTIMATE: Variable (depends on fossil prices)",
                "DIFFICULTY: Medium-Hard",
                "SUCCESS RATE: Good (fossils bias outcomes)",
                ""
            ])
            
        elif method == "mastercraft":
            steps.extend([
                "🔨 MASTERCRAFT METHOD:",
                "",
                "STEPS:",
                "1. Craft your base item using other methods first",
                "2. Leave one modifier slot open for mastercrafting",
                "3. Visit your hideout crafting bench",
                "4. Apply desired mastercraft modifier",
                "5. Note: mastercrafted mods can be changed anytime",
                "",
                "COST ESTIMATE: Crafting bench currency costs",
                "DIFFICULTY: Easy",
                "SUCCESS RATE: 100% (guaranteed modifier)",
                ""
            ])
        
        if target_mods:
            steps.extend([
                "🎯 YOUR TARGET MODIFIERS:",
                ""
            ])
            for i, mod in enumerate(target_mods, 1):
                steps.append(f"  {i}. {mod}")
            steps.append("")
        
        steps.extend([
            "💡 GENERAL CRAFTING TIPS:",
            "",
            "• Always check item level requirements for modifiers",
            "• Use 'Orb of Scouring' to reset items and start over",
            "• 'Divine Orb' rerolls numeric values of existing modifiers",
            "• 'Orb of Annulment' removes random modifiers (risky!)",
            "• Use PoE wiki or 'Craft of Exile' website for detailed info",
            "• Consider item level, base type, and influence requirements",
            "• Have backup currency in case of bad RNG",
            "",
            "🔗 USEFUL RESOURCES:",
            "• Path of Exile Wiki: https://pathofexile.fandom.com/",
            "• Craft of Exile: https://craftofexile.com/",
            "• PoE Database: https://poedb.tw/",
            ""
        ])
        
        return steps
    
    def display_results(self, steps):
        self.clear_screen()
        self.print_header()
        
        for line in steps:
            print(line)
        
        print("\n" + "=" * 60)
        input("\nPress Enter to continue...")
    
    def main_menu(self):
        while True:
            self.clear_screen()
            self.print_header()
            
            print("1. Create Crafting Guide")
            print("2. View Currency Information")
            print("3. Exit")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == '1':
                self.create_guide()
            elif choice == '2':
                self.show_currency_info()
            elif choice == '3':
                print("\nThanks for using PoE Craft Helper!")
                sys.exit(0)
            else:
                print("Invalid choice. Press Enter to continue...")
                input()
    
    def create_guide(self):
        self.clear_screen()
        self.print_header()
        
        # Get user input
        base_item = self.get_item_base()
        if not base_item:
            print("Item base is required!")
            input("Press Enter to continue...")
            return
        
        target_mods = self.get_target_modifiers()
        method = self.select_method()
        
        # Generate and display steps
        steps = self.calculate_steps(base_item, target_mods, method)
        self.display_results(steps)
    
    def show_currency_info(self):
        self.clear_screen()
        self.print_header()
        
        print("CURRENCY ORBS AND THEIR EFFECTS:")
        print("=" * 60)
        print()
        
        for currency, effect in self.currencies.items():
            print(f"• {currency:20} - {effect}")
        
        print("\n" + "=" * 60)
        input("Press Enter to continue...")
    
    def run(self):
        try:
            self.main_menu()
        except KeyboardInterrupt:
            print("\n\nExiting... Thanks for using PoE Craft Helper!")
            sys.exit(0)

if __name__ == "__main__":
    app = POECraftHelperCLI()
    app.run()