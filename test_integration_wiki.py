import sys
import os

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.itinerary_generator import ItineraryGenerator

def test_integration():
    generator = ItineraryGenerator()
    
    # Test with a destination definitely NOT in the local dataset
    state = {
        "destination": "Athirappilly",
        "duration": "3",
        "month": "October",
        "travel_type": "Nature"
    }
    
    print("Generating itinerary for " + state['destination'] + "...")
    result = generator.generate_itinerary(state)
    
    print("\n--- Generated Itinerary Preview ---")
    if isinstance(result, dict):
        narrative = result.get("narrative", "")
        print(narrative[:500] + "...")
        
        # Check meta
        meta = result.get("meta", {})
        print(f"\nMeta Data: {meta}")
        
        if "Generic Fallback" in narrative:
            print("\n[FAIL] Fallback generic template was used. Wikipedia integration might have failed.")
        else:
            print("\n[SUCCESS] Itinerary generated dynamically.")
            if meta.get("image"):
                print(f"[SUCCESS] Image found: {meta['image']}")
            else:
                print("[WARNING] No image found in meta.")
    else:
        # Fallback for string return (legacy)
        print(result[:500] + "...")
        if "Generic Fallback" in result:
             print("\n[FAIL] Fallback generic template was used.")
        else:
             print("\n[SUCCESS] Itinerary generated dynamically.")

if __name__ == "__main__":
    test_integration()
