import sys
import os
import json

# Add backend to python path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.agents.resource_agent import ResourceAgent

def verify_resources():
    print("--- Verifying Resource Agent Logic ---")
    agent = ResourceAgent()
    
    dest = "Tokyo"
    month = "November"
    travel_type = "Solo"
    
    print(f"Fetching resources for {dest} in {month} ({travel_type})...")
    
    try:
        resources = agent.get_resources(dest, month, travel_type)
        print("\n[RESULT RAW JSON]")
        print(json.dumps(resources, indent=2))
        
        # Validation
        if "packing_list" in resources and isinstance(resources["packing_list"], list):
             print("[PASS] Packing List present.")
        else:
             print("[FAIL] Packing List missing/invalid.")
             
        if "lingo" in resources and isinstance(resources["lingo"], list):
             print("[PASS] Lingo present.")
        else:
             print("[FAIL] Lingo missing/invalid.")
             
        if "budget" in resources and isinstance(resources["budget"], list):
             print("[PASS] Budget present.")
        else:
             print("[FAIL] Budget missing/invalid.")
             
        if "tip" in resources:
             print(f"[PASS] Cultural Tip: {resources['tip']}")
        else:
             print("[FAIL] Tip missing.")

    except Exception as e:
        print(f"\n[CRITICAL FAIL] Exception occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_resources()
