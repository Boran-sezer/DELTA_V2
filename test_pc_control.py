"""
Test du système PC Control
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from pc_control import PCControl

def test_smart_open():
    pc = PCControl()
    
    print(f"\n=== TEST PC CONTROL ===")
    print(f"Applications détectées: {len(pc.installed_apps)}")
    print(f"\nQuelques apps: {list(pc.installed_apps.keys())[:10]}")
    
    # Test 1: Site web connu
    print(f"\n--- Test 1: YouTube ---")
    result = pc.smart_open("YouTube")
    print(f"Résultat: {result}")
    
    # Test 2: Application
    print(f"\n--- Test 2: Chrome ---")
    result = pc.smart_open("Chrome")
    print(f"Résultat: {result}")
    
    # Test 3: Recherche Google
    print(f"\n--- Test 3: Recherche ---")
    result = pc.smart_open("météo Paris")
    print(f"Résultat: {result}")

if __name__ == "__main__":
    test_smart_open()
