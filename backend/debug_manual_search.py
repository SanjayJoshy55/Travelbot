import sys
import os

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from app.services.wikipedia_service import WikipediaService

def test_athirappilly():
    service = WikipediaService()
    query = "athirappilly"
    print(f"Searching for '{query}'...")
    results = service.search_location(query)
    print(f"Search Results: {results}")
    
    if results:
        # Try the first result likely 'Athirappilly Falls' or similar
        top_result = results[0]
        print(f"\nFetching details for top result: '{top_result}'...")
        details = service.get_location_details(top_result)
        
        print("\n--- Details ---")
        print(f"Title: {details.get('title')}")
        print(f"URL: {details.get('url')}")
        print(f"Coordinates: {details.get('coordinates')}")
        print(f"Summary Start: {details.get('summary', '')[:200]}...")

if __name__ == "__main__":
    test_athirappilly()
