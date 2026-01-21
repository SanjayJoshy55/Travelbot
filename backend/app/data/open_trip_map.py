import httpx
import os
from typing import List, Dict, Any

class OpenTripMapClient:
    """
    Client for OpenTripMap API to fetch attractions.
    Docs: https://opentripmap.io/docs
    """
    BASE_URL = "https://api.opentripmap.com/0.1/en"

    def __init__(self, api_key: str = None):
        # Allow passing key or getting from env
        self.api_key = api_key or os.getenv("OPENTRIPMAP_API_KEY")
        if not self.api_key:
            print("WARNING: OpenTripMap API Key is missing.")

        self.client = httpx.AsyncClient()

    async def get_attractions(self, lat: float, lon: float, radius: int = 5000, kind: str = "museums") -> List[Dict]:
        """
        Fetches attractions within a radius.
        """
        if not self.api_key:
            return []

        url = f"{self.BASE_URL}/places/radius"
        params = {
            "radius": radius,
            "lon": lon,
            "lat": lat,
            "kinds": kind,
            "format": "json", # json returns list of dicts. geojson returns FeatureCollection
            "apikey": self.api_key
        }

        try:
            with open("debug_log.txt", "w") as f:
                f.write(f"Fetching URL: {url}\nParams: {params}\n")

            response = await self.client.get(url, params=params)
            
            with open("debug_log.txt", "a") as f:
                f.write(f"Status: {response.status_code}\nResponse: {response.text[:1000]}\n")

            response.raise_for_status()
            data = response.json()
            return data

        except Exception as e:
            with open("debug_log.txt", "a") as f:
                f.write(f"Error: {e}\n")
            print(f"Error fetching attractions: {e}")
            return []

    async def get_place_details(self, xid: str) -> Dict:
        """
        Get detailed info for a specific place (description, image, etc.)
        """
        if not self.api_key:
            return {}
            
        url = f"{self.BASE_URL}/places/xid/{xid}"
        params = {"apikey": self.api_key}

        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching place details: {e}")
            return {}

    async def close(self):
        await self.client.aclose()
