from app.services.travel_service import TravelService
from app.services.wikipedia_service import WikipediaService
from typing import Dict

class TravelAgent:
    def __init__(self):
        self.service = TravelService()
        self.wiki = WikipediaService()

    def plan_trip(self, origin: str, destination: str) -> Dict:
        """
        Plans the logistics from A to B.
        """
        print(f"[TravelAgent] Planning trip from {origin} to {destination}...")
        
        # 1. Resolve Origin Coordinates
        origin_coords = {"lat": 0, "lon": 0}
        try:
            results = self.wiki.search_location(origin)
            if results:
                details = self.wiki.get_location_details(results[0])
                if details.get("coordinates"):
                    origin_coords = details["coordinates"]
        except Exception as e:
            print(f"Error fetching origin coords: {e}")
            
        # 2. Resolve Dest Coordinates (in case they weren't passed, though ideally they should be in state)
        # For simplicity, we search again to be robust.
        dest_coords = {"lat": 0, "lon": 0}
        try:
            results = self.wiki.search_location(destination)
            if results:
                details = self.wiki.get_location_details(results[0])
                if details.get("coordinates"):
                    dest_coords = details["coordinates"]
        except Exception as e:
            print(f"Error fetching dest coords: {e}")

        # 3. Estimate
        return self.service.estimate_travel(origin, origin_coords, destination, dest_coords)
