import pygame
import sys
import json
import os

class POECraftHelper:
    def __init__(self):
        pygame.init()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (46, 134, 171)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.GOLD = (255, 215, 0)
        
        # Screen setup
        self.width = 450
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("PoE Craft Helper - League 3.26")
        
        # Fonts
        self.font_title = pygame.font.Font(None, 24)
        self.font_normal = pygame.font.Font(None, 18)
        self.font_small = pygame.font.Font(None, 14)
        
        # State
        self.base_item = ""
        self.target_mods = []
        self.method = "chaos_spam"
        self.results = ""
        self.input_active = "base"  # "base", "mods", or "none"
        self.current_mod = ""
        
        # Currency data
        self.currencies = {
            'Orb of Alchemy': 'Upgrades normal item to rare',
            'Orb of Chance': 'Upgrades normal item to magic/rare/unique',
            'Orb of Alteration': 'Rerolls magic item modifiers',
            'Chaos Orb': 'Rerolls rare item modifiers',
            'Exalted Orb': 'Adds modifier to rare item',
            'Regal Orb': 'Upgrades magic item to rare'
        }
        
        self.methods = [
            ("Chaos Spam", "chaos_spam"),
            ("Alt + Regal", "alt_regal"), 
            ("Essence Crafting", "essence"),
            ("Fossil Crafting", "fossil"),
            ("Mastercraft", "mastercraft")
        ]
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.input_active == "base":
                    if event.key == pygame.K_BACKSPACE:
                        self.base_item = self.base_item[:-1]
                    elif event.key == pygame.K_TAB:
                        self.input_active = "mods"
                    elif event.unicode.isprintable():
                        self.base_item += event.unicode
                        
                elif self.input_active == "mods":
                    if event.key == pygame.K_BACKSPACE:
                        self.current_mod = self.current_mod[:-1]
                    elif event.key == pygame.K_RETURN:
                        if self.current_mod.strip():
                            self.target_mods.append(self.current_mod.strip())
                            self.current_mod = ""
                    elif event.key == pygame.K_TAB:
                        self.input_active = "base"
                    elif event.unicode.isprintable():
                        self.current_mod += event.unicode
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                # Check input field clicks
                if 50 <= y <= 80:  # Base item field
                    self.input_active = "base"
                elif 130 <= y <= 160:  # Mods field
                    self.input_active = "mods"
                else:
                    self.input_active = "none"
                
                # Check method radio buttons
                for i, (text, value) in enumerate(self.methods):
                    button_y = 220 + i * 25
                    if 50 <= x <= 70 and button_y <= y <= button_y + 20:
                        self.method = value
                
                # Check generate button
                if 50 <= x <= 200 and 360 <= y <= 390:
                    self.generate_steps()
                    
                # Check clear button
                if 220 <= x <= 280 and 360 <= y <= 390:
                    self.clear_all()
                    
        return True
        
    def generate_steps(self):
        if not self.base_item:
            self.results = "Please enter an item base!"
            return
            
        self.results = self.calculate_steps(self.base_item, self.target_mods, self.method)
        
    def calculate_steps(self, base_item, target_mods, method):
        steps = f"Crafting Steps for {base_item}:\n"
        steps += "="*30 + "\n\n"
        
        if method == "chaos_spam":
            steps += "CHAOS SPAM METHOD:\n"
            steps += "1. Obtain rare base item\n"
            steps += "2. Use Chaos Orbs repeatedly\n"
            steps += "3. Cost: 50-500+ Chaos\n\n"
        elif method == "alt_regal":
            steps += "ALT + REGAL METHOD:\n"
            steps += "1. Start with white base\n"
            steps += "2. Transmutation -> magic\n"
            steps += "3. Alt spam for mods\n"
            steps += "4. Regal to rare\n\n"
        elif method == "essence":
            steps += "ESSENCE METHOD:\n"
            steps += "1. Get relevant essence\n"
            steps += "2. Use on base item\n"
            steps += "3. Guarantees modifier\n\n"
        elif method == "fossil":
            steps += "FOSSIL METHOD:\n"
            steps += "1. Get relevant fossils\n"
            steps += "2. Use with resonator\n"
            steps += "3. Biases outcomes\n\n"
        elif method == "mastercraft":
            steps += "MASTERCRAFT METHOD:\n"
            steps += "1. Craft base first\n"
            steps += "2. Use crafting bench\n"
            steps += "3. Guaranteed mods\n\n"
            
        steps += "Target Modifiers:\n"
        for i, mod in enumerate(target_mods, 1):
            steps += f"{i}. {mod}\n"
            
        return steps
        
    def clear_all(self):
        self.base_item = ""
        self.target_mods = []
        self.current_mod = ""
        self.results = ""
        
    def draw(self):
        self.screen.fill(self.BLACK)
        
        # Title
        title = self.font_title.render("PoE Craft Helper - League 3.26", True, self.GOLD)
        self.screen.blit(title, (50, 10))
        
        # Base item input
        base_label = self.font_normal.render("Item Base:", True, self.WHITE)
        self.screen.blit(base_label, (50, 50))
        
        base_rect = pygame.Rect(50, 60, 350, 25)
        color = self.BLUE if self.input_active == "base" else self.GRAY
        pygame.draw.rect(self.screen, color, base_rect, 2)
        
        base_text = self.font_normal.render(self.base_item, True, self.WHITE)
        self.screen.blit(base_text, (55, 65))
        
        # Target mods input
        mods_label = self.font_normal.render("Target Modifiers:", True, self.WHITE)
        self.screen.blit(mods_label, (50, 100))
        
        mods_rect = pygame.Rect(50, 110, 350, 25)
        color = self.BLUE if self.input_active == "mods" else self.GRAY
        pygame.draw.rect(self.screen, color, mods_rect, 2)
        
        current_text = self.font_normal.render(self.current_mod, True, self.WHITE)
        self.screen.blit(current_text, (55, 115))
        
        # Display added mods
        for i, mod in enumerate(self.target_mods):
            mod_text = self.font_small.render(f"• {mod}", True, self.LIGHT_GRAY)
            self.screen.blit(mod_text, (55, 145 + i * 15))
        
        # Method selection
        method_label = self.font_normal.render("Crafting Method:", True, self.WHITE)
        self.screen.blit(method_label, (50, 200))
        
        for i, (text, value) in enumerate(self.methods):
            y_pos = 220 + i * 25
            
            # Radio button
            center = (60, y_pos + 10)
            pygame.draw.circle(self.screen, self.WHITE, center, 8, 2)
            if self.method == value:
                pygame.draw.circle(self.screen, self.GOLD, center, 5)
            
            # Text
            method_text = self.font_normal.render(text, True, self.WHITE)
            self.screen.blit(method_text, (80, y_pos))
        
        # Buttons
        generate_btn = pygame.Rect(50, 360, 150, 30)
        pygame.draw.rect(self.screen, self.BLUE, generate_btn)
        gen_text = self.font_normal.render("Generate Steps", True, self.WHITE)
        self.screen.blit(gen_text, (60, 370))
        
        clear_btn = pygame.Rect(220, 360, 60, 30)
        pygame.draw.rect(self.screen, self.GRAY, clear_btn)
        clear_text = self.font_normal.render("Clear", True, self.WHITE)
        self.screen.blit(clear_text, (235, 370))
        
        # Results
        if self.results:
            results_label = self.font_normal.render("Results:", True, self.WHITE)
            self.screen.blit(results_label, (50, 410))
            
            y_offset = 430
            for line in self.results.split('\n'):
                if y_offset > self.height - 20:
                    break
                result_text = self.font_small.render(line[:50], True, self.WHITE)
                self.screen.blit(result_text, (50, y_offset))
                y_offset += 15
        
        # Instructions
        instr = self.font_small.render("TAB: Switch fields, ENTER: Add mod", True, self.GRAY)
        self.screen.blit(instr, (50, self.height - 20))
        
        pygame.display.flip()
        
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()
            self.draw()
            clock.tick(60)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = POECraftHelper()
    app.run()