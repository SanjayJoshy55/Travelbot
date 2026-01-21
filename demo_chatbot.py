import sys
import os
import asyncio

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.itinerary_generator import ItineraryGenerator

def run_demo(destination):
    print(f"\n{'='*50}")
    print(f"User: Plan a trip to {destination}")
    print(f"{'='*50}")
    
    generator = ItineraryGenerator()
    
    # Simulate state passed from frontend/orchestrator
    state = {
        "destination": destination,
        "duration": "3",
        "month": "May",
        "travel_type": "Leisure"
    }
    
    print("Chatbot: (Thinking...) Checking local database...")
    # ItineraryGenerator handles the logic: DB -> missing -> Wikipedia
    try:
        response = generator.generate_itinerary(state)
        print("\nChatbot Response:\n")
        print(response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Demo 1: The user's requested location
    run_demo("Athirappilly")
    
    # Demo 2: Another random international location to prove robustness
    run_demo("Kyoto")

    # Demo 3: Seasonal Events
    print("\n--- Seasonal Event Demo ---")
    print("User: Plan a trip to Kochi in December")
    generator = ItineraryGenerator()
    state = {"destination": "Kochi", "duration": "3", "month": "December", "travel_type": "Leisure"}
    try:
        response = generator.generate_itinerary(state)
        print("\nChatbot Response:\n")
        print(response)
    except Exception as e:
        print(f"Error: {e}")
