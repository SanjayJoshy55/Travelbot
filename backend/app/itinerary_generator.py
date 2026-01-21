import json
import os
from typing import Dict
from app.services.rag_service import RagService
from app.services.wikipedia_service import WikipediaService

class ItineraryGenerator:
    def __init__(self):
        # Load the dataset built in Phase 2
        self.dataset = {}
        try:
            data_path = os.path.join(os.path.dirname(__file__), "data/dataset.json")
            if os.path.exists(data_path):
                with open(data_path, "r") as f:
                    self.dataset = json.load(f)
            else:
                print("Warning: dataset.json not found. Using templates.")
        except Exception as e:
            print(f"Error loading dataset: {e}")

        # Initialize RAG Service (Phase 3)
        try:
            self.rag = RagService(persist_path="./chroma_db")
        except Exception as e:
            print(f"Error initializing RAG: {e}")
            self.rag = None
            
        # Initialize Wikipedia Service
        self.wiki = WikipediaService()

    def generate_itinerary(self, state: Dict) -> Dict:
        """
        Generates a structured itinerary based on state.
        Uses REAL data (Phase 2) + RAG Context (Phase 3).
        """
        dest_input = state.get("destination", "Unknown Destination")
        dur = state.get("duration", "3")
        month = state.get("month", "Anytime")
        type_ = state.get("travel_type", "Leisure")

        # Case-insensitive lookup
        city_data = None
        for key in self.dataset:
            if key.lower() in dest_input.lower():
                city_data = self.dataset[key]
                break
        
        # Fallback to Wikipedia if not in simple dataset
        wiki_context = ""
        if not city_data:
            print(f"Destination '{dest_input}' not in local DB. Searching Wikipedia...")
            results = self.wiki.search_location(dest_input)
            if results:
                print(f"Found Wikipedia matches: {results}")
                # Use the top result
                details = self.wiki.get_location_details(results[0])
                if details and "error" not in details:
                    # Construct dynamic city_data
                    city_data = {
                        "destination": details["title"],
                        "description": details.get("summary", ""),
                        "images": details.get("images", []), # Capture images here
                        "attractions": [
                            # Create a generic attraction for the city center based on coords
                            {
                                "name": f"Explore {details['title']} Center",
                                "point": {"lat": details["coordinates"]["lat"], "lon": details["coordinates"]["lon"]} if details.get("coordinates") else {"lat": 0, "lon": 0},
                                "rate": 3,
                                "kinds": "city_center"
                            }
                        ],
                        "weather": {} # No weather data for dynamic yet
                    }
                    wiki_context = details.get("summary", "")
        
        if not city_data:
            return self._generate_generic(dest_input, dur, month, type_)

        # Build Real Itinerary
        attractions = city_data.get("attractions", [])
        weather = city_data.get("weather", {})
        
        
        # Phase 3: RAG Retrieval
        rag_insight = "No insights available."
        if self.rag:
            # Query for something interesting about the city
            query = f"Interesting facts or history about {city_data['destination']}"
            results = self.rag.query(query, n_results=1)
            if results:
                rag_insight = results[0]['text']

        # Phase 3.5: Seasonal Events (Wikipedia)
        seasonal_info = self.wiki.get_seasonal_events(city_data['destination'], month)
        if seasonal_info:
            print(f"Found seasonal info: {seasonal_info[:50]}...")
            # Append to wiki_context if it exists, or create it
            if not wiki_context:
                wiki_context = seasonal_info
            else:
                wiki_context += f"\n\n{seasonal_info}"

        # Phase 4: Intelligent Planning (Clustering)
        # 1. Instantiate Planner
        from app.services.planner_service import PlannerService
        planner = PlannerService()
        
        # 2. Get Duration (Parsing "3 days" -> 3)
        try:
            day_count = int(dur.split()[0])
        except:
            day_count = 3
        
        # 3. Group Attractions by Day
        daily_plan = planner.group_attractions_by_day(attractions, day_count)
        
        # 4. Generate Narrative (LLM)
        from app.services.llm_service import LLMService
        llm = LLMService()
        
        # Prepare Context string from RAG + Wikipedia
        context_str = rag_insight if rag_insight != "No insights available." else ""
        if wiki_context:
            context_str += f"\n\nWikipedia Summary:\n{wiki_context}"
        
        if not context_str:
             context_str = f"Beautiful destination: {city_data['destination']}"
        
        # Prepare Meta Data for Frontend
        # Safe extraction of coordinates and image
        lat = 0
        lon = 0
        image_url = None
        
        # If we used Wiki details earlier (dynamic construction)
        if "coordinates" in city_data.get("attractions", [{}])[0].get("point", {}):
             pt = city_data["attractions"][0]["point"]
             lat = pt.get("lat", 0)
             lon = pt.get("lon", 0)
             
        # Also check separate 'geo' key from local dataset
        if lat == 0 and "geo" in city_data:
            lat = city_data["geo"].get("lat", 0)
            lon = city_data["geo"].get("lon", 0)
        
        # Try to snag a real wiki image if available in city_data (we added this to dynamic flow below)
        if "images" in city_data and city_data["images"]:
            image_url = city_data["images"][0] # Take first valid image
            
        # --- CRITICAL FIX: If local dataset lacked images, fetch them now ---
        if not image_url:
            print(f"No image in local data for {city_data['destination']}. Fetching from Wikipedia...")
            try:
                # Quick search
                w_results = self.wiki.search_location(city_data['destination'])
                if w_results:
                    w_details = self.wiki.get_location_details(w_results[0])
                    # Update Image
                    if w_details.get("images"):
                        image_url = w_details["images"][0]
                    # Update Coords if we still don't have them
                    if lat == 0 and w_details.get("coordinates"):
                        lat = w_details["coordinates"]["lat"]
                        lon = w_details["coordinates"]["lon"]
            except Exception as e:
                print(f"Error fetching fallback image: {e}")

        # Generate!
        narrative = llm.generate_trip_narrative(
            destination=city_data['destination'],
            duration=dur,
            context=context_str,
            daily_plan=daily_plan
        )
        
        # Return Structured Object
        return {
            "narrative": narrative,
            "meta": {
                "destination": city_data['destination'],
                "coordinates": {"lat": lat, "lon": lon},
                "image": image_url
            }
        }


    def _get_avg_temp(self, weather):
        try:
            temps = weather.get("daily", {}).get("temperature_2m_max", [])
            if temps:
                return sum(temps) / len(temps)
        except:
            pass
        return "N/A"

    def _generate_generic(self, dest, dur, month, type_):
        return f"""
# Trip to {dest}
**Duration:** {dur} Days | **Season:** {month} | **Type:** {type_}

## 🌟 Destination Overview
{dest} is a fantastic choice... (Generic Fallback)
"""
        return {"narrative": content, "meta": {"coordinates": {"lat": 0, "lon": 0}, "image": None}}
