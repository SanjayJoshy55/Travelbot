import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from app.services.wikipedia_service import WikipediaService
import json

def test_images():
    service = WikipediaService()
    
    cities = ["Kochi", "Tokyo", "Paris"]
    
    for city in cities:
        print(f"\n--- Testing {city} ---")
        try:
            results = service.search_location(city)
            if not results:
                print("No search results.")
                continue
                
            top_result = results[0]
            print(f"Top Result: {top_result}")
            
            details = service.get_location_details(top_result)
            
            images = details.get("images", [])
            print(f"Found {len(images)} images.")
            
            if images:
                print(f"Sample Image: {images[0]}")
            else:
                print("DEBUG: Fetching raw page to see why...")
                import wikipedia
                page = wikipedia.page(top_result, auto_suggest=False)
                print(f"Raw page.images count: {len(page.images)}")
                print(f"First 5 raw images: {page.images[:5]}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_images()
