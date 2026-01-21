import httpx
import asyncio

async def search_wikipedia(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        # Step 1: Search for the page
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json"
        }
        print(f"Searching for {query}...")
        resp = await client.get(search_url, params=search_params)
        print(f"Request URL: {resp.url}")
        
        try:
            data = resp.json()
        except Exception:
            print(f"Failed to decode JSON. Status: {resp.status_code}")
            print(f"Response: {resp.text[:500]}")
            return
        
        if not data.get('query', {}).get('search'):
            print("No results found.")
            return

        title = data['query']['search'][0]['title']
        print(f"Found top result: {title}")

        # Step 2: Get details (extract and coordinates)
        details_params = {
            "action": "query",
            "prop": "extracts|coordinates",
            "titles": title,
            "exintro": True,
            "explaintext": True,
            "format": "json"
        }
        print(f"Fetching details for {title}...")
        resp = await client.get(search_url, params=details_params)
        try:
            data = resp.json()
        except:
             print("Failed to decode JSON details.")
             return
        
        pages = data['query']['pages']
        for page_id, page_data in pages.items():
            print(f"\n--- {page_data['title']} ---")
            print(f"Extract: {page_data.get('extract', 'No extract available.')[:200]}...")
            if 'coordinates' in page_data:
                coords = page_data['coordinates'][0]
                print(f"Coordinates: Lat {coords['lat']}, Lon {coords['lon']}")
            else:
                print("No coordinates found.")

if __name__ == "__main__":
    asyncio.run(search_wikipedia("Eiffel Tower"))
    asyncio.run(search_wikipedia("Tokyo"))
