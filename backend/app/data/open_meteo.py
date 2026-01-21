import httpx
from typing import Dict, Any, Optional

class OpenMeteoClient:
    """
    Client for Open-Meteo API to fetch climate/weather data.
    Docs: https://open-meteo.com/en/docs
    """
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    def __init__(self):
        self.client = httpx.AsyncClient()

    async def get_climate_data(self, lat: float, lon: float, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Fetches historical weather data to estimate seasonal climate.
        """
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
            "timezone": "auto"
        }
        
        try:
            response = await self.client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return {}

    async def get_geocode(self, city_name: str) -> Optional[Dict[str, float]]:
        """
        Helper to get lat/lon for a city using Open-Meteo Geocoding API.
        """
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
        
        try:
            response = await self.client.get(geo_url, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get("results"):
                result = data["results"][0]
                return {"lat": result["latitude"], "lon": result["longitude"], "name": result["name"]}
            return None
        except Exception as e:
            print(f"Error geocoding city: {e}")
            return None

    async def close(self):
        await self.client.aclose()
