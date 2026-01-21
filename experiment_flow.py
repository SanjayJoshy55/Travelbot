import sys
import os

# Add backend to python path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.conversation_manager import ConversationManager

def test_flow():
    manager = ConversationManager()
    state = {}
    
    print("--- 1. Initial State ---")
    print(f"State: {state}")
    
    # 1. Fill requirements
    state = {
        "destination": "Paris",
        "duration": "3",
        "month": "June",
        "travel_type": "Solo"
    }
    
    # Simulate what happens when 'ready_to_generate' is hit
    print("\n--- 2. Simulating Generation Complete ---")
    # In main.py, after generation, we manually set this:
    state["stage"] = "reviewing_itinerary"
    print(f"State set to: {state}")
    
    # 2. User says "I am happy"
    print("\n--- 3. User Input: 'I am happy' ---")
    response, new_state, status = manager.process_message("I am happy", state)
    
    print(f"Status: {status}")
    print(f"Response: {response}")
    print(f"New State: {new_state}")
    
    if status == "collecting_origin":
        print("[PASS] Correctly transitioned to collecting origin.")
    else:
        print(f"[FAIL] Expected 'collecting_origin', got '{status}'")
        return

    # 3. User says "London"
    print("\n--- 4. User Input: 'London' ---")
    response, final_state, status = manager.process_message("London", new_state)
    
    print(f"Status: {status}")
    print(f"Response: {response}")
    print(f"Final State: {final_state}")
    
    if status == "showing_travel_options":
         print("[PASS] Correctly transitioned to showing travel options.")
    else:
         print(f"[FAIL] Expected 'showing_travel_options', got '{status}'")

if __name__ == "__main__":
    test_flow()
