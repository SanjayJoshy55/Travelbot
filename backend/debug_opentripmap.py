import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENTRIPMAP_API_KEY")

async def debug():
    base_url = "https://api.opentripmap.com/0.1/en/places/radius"
    # Try with explicit known working params for Paris
    params = {
        "radius": 1000,
        "lon": 2.3522,
        "lat": 48.8566,
        "kinds": "museums",
        "format": "json",
        "apikey": API_KEY
    }
    
    print(f"Using Key: {API_KEY[:5]}...")
    print(f"Requesting: {base_url} with params {params}")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)
        print(f"Status: {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Text Body: {response.text}")
        try:
            print(f"JSON Body: {response.json()}")
        except:
            print("JSON Decode Failed")

if __name__ == "__main__":
    asyncio.run(debug())
