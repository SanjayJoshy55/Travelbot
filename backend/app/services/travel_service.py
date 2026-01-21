import urllib.parse

class TravelService:
    def __init__(self):
        pass

    def estimate_travel(self, origin_name: str, origin_coords: dict, dest_name: str, dest_coords: dict):
        """
        Estimates travel details using Geodetic distance (Haversine formula).
        """
        import math
        import urllib.parse
        
        # 1. Booking Links
        # Google
        google_url = f"https://www.google.com/travel/flights?q=Flights+to+{urllib.parse.quote(dest_name)}+from+{urllib.parse.quote(origin_name)}"
        
        # Skyscanner (Format: https://www.skyscanner.com/transport/flights/{origin}/{dest})
        # Use hyphens for multi-word cities (e.g. new-york)
        origin_slug = origin_name.lower().replace(" ", "-")
        dest_slug = dest_name.lower().replace(" ", "-")
        skyscanner_url = f"https://www.skyscanner.com/transport/flights/{origin_slug}/{dest_slug}"
        
        # 2. Calculate Distance (Haversine)
        R = 6371  # Earth radius in km
        
        lat1 = math.radians(origin_coords['lat'])
        lon1 = math.radians(origin_coords['lon'])
        lat2 = math.radians(dest_coords['lat'])
        lon2 = math.radians(dest_coords['lon'])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance_km = R * c
        
        # 3. Estimate Flight Time
        # Avg speed ~800 km/h + 30 mins takeoff/landing
        flight_hours = (distance_km / 800) + 0.5
        
        # Format time
        hours = int(flight_hours)
        mins = int((flight_hours - hours) * 60)
        
        if distance_km < 200:
             duration_str = f"{int(distance_km / 60)} hours (Driving)"
             mode = "Drive"
        else:
             duration_str = f"~{hours}h {mins}m (Flight)"
             mode = "Flight"

        return {
            "origin": origin_name,
            "destination": dest_name,
            "mode": mode,
            "distance": f"{int(distance_km)} km",
            "estimated_duration": duration_str, 
            "booking_link": google_url,
            "booking_link": google_url,
            "tips": "Estimate based on direct distance. Check links for live pricing."        }
