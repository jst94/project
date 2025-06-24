# Path of Exile Craft Helper

A Python GUI overlay application that provides step-by-step crafting guidance for Path of Exile 1 (League 3.26).

## Features

- **Overlay Window**: Stays on top of Path of Exile for easy access
- **Multiple Crafting Methods**: Supports various crafting approaches
- **Step-by-Step Guidance**: Detailed instructions for each crafting method
- **Item Base Input**: Specify your starting item
- **Target Modifiers**: List desired modifiers for your item

## Usage

1. Run the application:
   ```bash
   python poe_craft_helper.py
   ```

2. Enter your item base (e.g., "Titanium Spirit Shield")

3. List your target modifiers (one per line):
   - +1 to Level of Socketed Gems
   - 70+ Life
   - 35+ Resistances

4. Select your preferred crafting method:
   - **Chaos Spam**: Use Chaos Orbs repeatedly
   - **Alt + Regal**: Alteration/Regal method for targeted crafting
   - **Essence Crafting**: Use essences for guaranteed modifiers
   - **Fossil Crafting**: Use fossils for biased outcomes
   - **Mastercraft**: Use crafting bench for guaranteed modifiers

5. Click "Generate Crafting Steps" to get detailed instructions

## Crafting Methods Explained

### Chaos Spam
- Best for: When you have lots of currency and want multiple good modifiers
- Cost: 50-500+ Chaos Orbs (RNG dependent)
- Risk: High variance, can be expensive

### Alt + Regal  
- Best for: Targeting 1-2 specific modifiers
- Cost: Moderate (Alterations + Regal + potentially Exalts)
- Risk: Lower cost entry, good control

### Essence Crafting
- Best for: Guaranteeing at least one specific modifier
- Cost: Higher but more predictable
- Risk: Lower variance than chaos spam

### Fossil Crafting
- Best for: Biasing outcomes toward desired modifier types
- Cost: Variable based on fossil prices
- Risk: More controlled than pure RNG methods

### Mastercraft
- Best for: Adding final guaranteed modifiers
- Cost: Currency cost from crafting bench
- Risk: Very low, guaranteed outcomes

## Controls

- **Clear**: Reset all input fields
- **Toggle Overlay**: Enable/disable always-on-top behavior
- Window transparency is set to 90% for overlay functionality

## Requirements

- Python 3.6+ with tkinter (included in most Python installations)
- No additional dependencies required

## Tips

- Always check item level requirements for modifiers
- Use Path of Exile wiki or Craft of Exile for detailed modifier information
- Consider using Orb of Scouring to reset items when needed
- Divine Orbs reroll the numeric values of existing modifiers
- Annulment Orbs can remove unwanted modifiers (risky)