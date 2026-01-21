import sys
import os

# Add backend to python path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.agents.travel_agent import TravelAgent

def verify_travel_logic():
    print("--- Verifying Travel Agent Logic ---")
    agent = TravelAgent()
    
    origin = "London"
    destination = "New York"
    
    print(f"Planning trip from {origin} to {destination}...")
    try:
        result = agent.plan_trip(origin, destination)
        
        print("\n[RESULT]")
        print(f"Mode: {result.get('mode')}")
        print(f"Distance: {result.get('distance')}")
        print(f"Duration: {result.get('estimated_duration')}")
        print(f"Google Link: {result.get('booking_link')}")
        
        # Checks
        if "google.com" in result.get("booking_link", ""):
            print("\n[PASS] Google link generated.")
        else:
             print("[FAIL] Google link missing.")
             
        if result.get("distance") and "km" in result.get("distance"):
             print("[PASS] Distance calculated.")
        else:
             print("[FAIL] Distance calculation failed.")

    except Exception as e:
        print(f"\n[CRITICAL FAIL] Exception occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_travel_logic()
