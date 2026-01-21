import wikipedia

class WikipediaService:
    def __init__(self):
        # Set a user agent to avoid being blocked by Wikipedia API
        wikipedia.set_user_agent("Chatbot/1.0 (https://github.com/yourusername/chatbot; contact@example.com)")

    def search_location(self, query: str):
        """
        Search for a location on Wikipedia.
        Returns a list of search results.
        """
        try:
            results = wikipedia.search(query)
            return results
        except Exception as e:
            print(f"Error searching Wikipedia: {e}")
            return []

    def get_location_details(self, title: str):
        """
        Get details including summary and coordinates for a specific page title.
        """
        try:
            page = wikipedia.page(title, auto_suggest=False)
            
            details = {
                "title": page.title,
                "summary": page.summary,
                "url": page.url,
                "coordinates": None,
                "images": []
            }

            try:
                # coordinates is usually a tuple (lat, lon)
                if page.coordinates:
                   details["coordinates"] = {
                       "lat": float(page.coordinates[0]),
                       "lon": float(page.coordinates[1])
                   }
            except KeyError:
                pass
                
            # Fetch Images (Filter for likely photos)
            try:
                raw_images = page.images
                # Filter out SVGs, small icons, etc.
                valid_images = [
                    img for img in raw_images 
                    if img.lower().endswith(('.jpg', '.jpeg', '.png')) 
                    and 'svg' not in img.lower()
                    and 'logo' not in img.lower()
                ]
                details["images"] = valid_images
            except Exception as e:
                print(f"Error fetching images: {e}")
            
            return details
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Disambiguation error for {title}: {e.options}")
            return {"error": "Ambiguous query", "options": e.options}
        except wikipedia.exceptions.PageError:
            print(f"Page not found: {title}")
            return {"error": "Page not found"}
        except Exception as e:
            print(f"Error fetching page details: {e}")
            return {"error": str(e)}

    def get_seasonal_events(self, location: str, month: str):
        """
        Attempts to find festivals or events for a specific location and month.
        Returns a summary string or None.
        """
        if not month or month == "Anytime":
            return None
            
        queries = [
            f"List of festivals in {location}",
            f"{location} festivals",
            f"Culture of {location}"
        ]
        
        print(f"Searching for seasonal events in {location} for {month}...")
        
        for q in queries:
            try:
                # Limit to 1 result to keep it fast
                results = wikipedia.search(q, results=1)
                if results:
                    page = wikipedia.page(results[0], auto_suggest=False)
                    content = page.content
                    
                    # Simple keyword search in the content
                    # We look for the month name in the page content
                    # and try to extract a relevant snippet.
                    # This is rudimentary but effective for a prototype.
                    
                    if month.lower() in content.lower():
                        # Find the index
                        idx = content.lower().find(month.lower())
                        # Grab a chunk of text around it
                        start = max(0, idx - 200)
                        end = min(len(content), idx + 500)
                        snippet = content[start:end]
                        
                        # Clean up snippet (incomplete sentences)
                        snippet = snippet.replace("\n", " ")
                        return f"Seasonal Info ({month}): ...{snippet}..."
            except:
                continue
                
        return None

if __name__ == "__main__":
    service = WikipediaService()
    print("Searching for 'Eiffel Tower'...")
    results = service.search_location("Eiffel Tower")
    print(f"Results: {results}")
    
    if results:
        print(f"Getting details for '{results[0]}'...")
        details = service.get_location_details(results[0])
        print(f"Details: {details}")
