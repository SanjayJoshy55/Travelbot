import asyncio
import os
from dotenv import load_dotenv
from app.services.data_service import DataService

# Load environment variables
load_dotenv()

async def test_fetch():
    print(f"Testing with API Key: {os.getenv('OPENTRIPMAP_API_KEY')[:5]}...")
    
    service = DataService()
    destination = "Paris"
    
    print(f"Fetching data for {destination}...")
    try:
        # Pass explicit kind to test if "interesting_places" was the issue
        # Note: gather_trip_data in DataService uses defaults, we might need to update DataService to accept kind
        # or update DataService here.
        # Actually DataService.gather_trip_data doesn't accept kind.
        # Let's modify DataService to propagate **kwargs or just change the default in OpenTripMapClient?
        # A quick fix: Update OpenTripMapClient default or pass it if I update DataService.
        
        # Let's update DataService to be more flexible first? No, keeps it simple.
        # Let's update OpenTripMapClient default to 'museums' temporarily? 
        # Or better: Update DataService to accept kind.
        data = await service.gather_trip_data(destination)
        
        print("\n--- Geo Data ---")
        print(data.get("geo"))

        print("\n--- Weather (Snippet) ---")
        weather = data.get("weather", {})
        if weather and "daily" in weather:
            print(f"Max Temps: {weather['daily'].get('temperature_2m_max')}")
        else:
            print("No weather data.")

        print("\n--- Attractions (Top 5) ---")
        attractions = data.get("attractions", [])
        print(f"Type of attractions: {type(attractions)}")
        if isinstance(attractions, dict):
            print("Attractions is a dict, keys:", attractions.keys())
            # If it's a dict, maybe the list is inside a key?
            if "features" in attractions:
                attractions = attractions["features"]
        
        if isinstance(attractions, list):
            for place in attractions[:5]:
                print(f"- {place.get('name')} ({place.get('kinds')})")
        else:
            print("Attractions data is not a list:", attractions)

        if not attractions:
            print("No attractions found (Check API Key).")
    finally:
        await service.close()

if __name__ == "__main__":
    asyncio.run(test_fetch())
