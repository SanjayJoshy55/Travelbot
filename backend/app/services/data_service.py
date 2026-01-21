from app.data.open_meteo import OpenMeteoClient
from app.data.open_trip_map import OpenTripMapClient
from typing import Dict, Any

class DataService:
    def __init__(self):
        self.weather_client = OpenMeteoClient()
        self.places_client = OpenTripMapClient() # loads key from env

    async def gather_trip_data(self, destination: str, month: str = "May") -> Dict[str, Any]:
        """
        Orchestrates fetching all necessary data for a trip.
        1. Geocodes the destination.
        2. Fetches climate/weather data.
        3. Fetches top attractions.
        """
        data_context = {
            "destination": destination,
            "geo": {},
            "weather": {},
            "attractions": []
        }

        # 1. Geocoding (Open-Meteo)
        geo = await self.weather_client.get_geocode(destination)
        if not geo:
            return data_context # Return empty context if city not found
        
        data_context["geo"] = geo
        lat, lon = geo["lat"], geo["lon"]

        # 2. Weather Data (Historical/Climate Estimate)
        weather = await self.weather_client.get_climate_data(lat, lon, "2024-05-01", "2024-05-07")
        data_context["weather"] = weather

        # 3. Attractions (OpenTripMap)
        places = await self.places_client.get_attractions(lat, lon)
        data_context["attractions"] = places

        return data_context

    async def close(self):
        await self.weather_client.close()
        await self.places_client.close()
