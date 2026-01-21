import wikipedia

def test_event_search(location, month):
    queries = [
        f"{location} festivals",
        f"{location} {month} events",
        f"Culture of {location}",
        f"List of festivals in {location}"
    ]
    
    print(f"--- Searching for events in {location} during {month} ---")
    
    for q in queries:
        print(f"Query: '{q}'")
        try:
            results = wikipedia.search(q)
            print(f"Results: {results}")
            if results:
                # Try to get a summary of the top result
                try:
                    summary = wikipedia.summary(results[0], sentences=3)
                    print(f"Summary of '{results[0]}': {summary}\n")
                except:
                    print(f"Could not get summary for {results[0]}\n")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_event_search("Kochi", "December")
    test_event_search("Kochi", "August")
