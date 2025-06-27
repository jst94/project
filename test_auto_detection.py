#!/usr/bin/env python3
"""
Auto-Detection Test Script
Tests the auto-detection functionality manually
"""

import sys
import time
import tkinter as tk
from tkinter import messagebox

def test_detection():
    """Test auto-detection manually"""
    try:
        from auto_detection import AutoDetector
        
        print("Starting auto-detection test...")
        print("Position your mouse over a PoE item tooltip and press Enter...")
        input("Press Enter when ready...")
        
        detector = AutoDetector()
        
        print("Detecting item at cursor position...")
        item = detector.detect_item_at_cursor()
        
        if item:
            print(f"\n✓ Item detected!")
            print(f"Base Type: {item.base_type}")
            print(f"Item Type: {item.item_type}")
            print(f"Rarity: {item.rarity}")
            print(f"Confidence: {item.confidence:.0%}")
            
            if item.item_level:
                print(f"Item Level: {item.item_level}")
            
            if item.modifiers:
                print(f"Modifiers ({len(item.modifiers)}):")
                for mod in item.modifiers[:5]:  # Show first 5
                    print(f"  - {mod}")
        else:
            print("\n✗ No item detected")
            print("Make sure:")
            print("- You're hovering over a PoE item tooltip")
            print("- The tooltip is clearly visible")
            print("- The game is in windowed or borderless mode")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")

def test_hotkey():
    """Test hotkey functionality"""
    try:
        import keyboard
        
        print("Testing hotkey functionality...")
        print("Press Ctrl+D to test hotkey detection (Ctrl+C to exit)")
        
        def on_hotkey():
            print("\n🔥 Hotkey detected! Ctrl+D pressed")
        
        keyboard.add_hotkey('ctrl+d', on_hotkey)
        
        try:
            keyboard.wait('ctrl+c')
        except KeyboardInterrupt:
            pass
        
        print("\nHotkey test complete")
        
    except ImportError:
        print("✗ Keyboard module not available for hotkey testing")
    except Exception as e:
        print(f"✗ Hotkey test failed: {e}")

if __name__ == "__main__":
    print("=== Auto-Detection Manual Test ===\n")
    
    print("1. Manual detection test")
    print("2. Hotkey test")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        test_detection()
    elif choice == '2':
        test_hotkey()
    else:
        print("Exiting...")
