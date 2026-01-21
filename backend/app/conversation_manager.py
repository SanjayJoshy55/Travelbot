from typing import Dict, List, Tuple

REQUIRED_FIELDS = ["destination", "duration", "month", "travel_type"]

class ConversationManager:
    def __init__(self):
        pass

    def process_message(self, message: str, current_state: Dict) -> Tuple[str, Dict, str]:
        """
        Process the user message and update state.
        Returns: (response_text, updated_state, status)
        """
        updated_state = current_state.copy()
        message_lower = message.lower()
        
        # --- STAGE 2: Post-Itinerary Review ---
        # If we are in 'reviewing_itinerary' (set by Streamlit after generation)
        if current_state.get("stage") == "reviewing_itinerary":
            # Check sentiment
            if any(x in message_lower for x in ["happy", "good", "yes", "great", "excellent", "love", "proceed", "continue", "next", "fine", "okay", "ok", "sure", "correct", "perfect", "booking", "go ahead", "awesome", "nice", "cool"]):
                updated_state["stage"] = "collecting_origin"
                return ("Glad you liked it! Let's plan your travel. Where are you starting your journey from?", updated_state, "collecting_origin")
            else:
                # Assume change request
                return ("Thinking...", updated_state, "modifying")

        # --- STAGE 3: Collecting Origin ---
        if current_state.get("stage") == "collecting_origin":
             # Extract origin (assume whole message for now)
             updated_state["origin"] = message.strip()
             updated_state["stage"] = "showing_travel"
             return ("Finding the best travel options for you...", updated_state, "showing_travel_options")

        # --- STAGE 1: Standard Collection (Legacy) ---
        # Only proceed if we are NOT in a later stage
        # ... (rest of the code)

        # Month/Season Extraction (Do this FIRST to remove it from dest)
        months = ["january", "february", "march", "april", "may", "june", 
                  "july", "august", "september", "october", "november", "december"]
        seasons = ["spring", "summer", "autumn", "fall", "winter"]
        
        found_time = None
        for m in months:
            if m in message_lower:
                found_time = m.capitalize()
                break
        if not found_time:
            for s in seasons:
                if s in message_lower:
                    found_time = s.capitalize()
                    break
        
        if found_time:
            updated_state["month"] = found_time

        # Simple heuristic extraction (Placeholder for LLM)
        if "destination" not in updated_state and not self._is_greeting(message_lower):
             # Improved extraction using regex-like replacement
             import re
             
             clean_dest = message_lower
             
             # Step 1: Remove the found month/season if any
             # e.g. "kochi in december" -> "kochi in "
             if found_time:
                 clean_dest = clean_dest.replace(found_time.lower(), "")
                 
             # Step 2: Remove "in" if it's trailing (common connector)
             clean_dest = clean_dest.strip()
             if clean_dest.endswith(" in"):
                 clean_dest = clean_dest[:-3].strip()

             # Step 3: Smart Extraction (Stopword Filtering)
             # Define Stopwords (Travel specific + Common English)
             stopwords = {
                 "i", "me", "my", "we", "us", "our", "you", "your",
                 "want", "wanna", "would", "like", "love", "wish", "dream", "hope",
                 "go", "going", "gone", "com",
                 "travel", "traveling", "travelling",
                 "visit", "visiting",
                 "plan", "planning", "planned",
                 "trip", "tour", "vacation", "holiday", "journey",
                 "to", "for", "in", "at", "on", "a", "an", "the", "from",
                 "is", "am", "are", "was", "were", "be",
                 "can", "could", "should", "please", "kindly",
                 "looking", "search", "find", "explore",
                 "about", "of", "off", "details", "info", "information"
             }
             
             # Tokenize and filter
             import string
             # Remove punctuation
             translator = str.maketrans('', '', string.punctuation)
             clean_msg_no_punct = clean_dest.translate(translator)
             
             words = clean_msg_no_punct.split()
             relevant_words = [w for w in words if w not in stopwords]
             
             # Reconstruct
             clean_dest = " ".join(relevant_words)
             
             if clean_dest and len(clean_dest) < 50: # Sanity check length
                 updated_state["destination"] = clean_dest.title()
        
        if "duration" not in updated_state and not self._is_greeting(message_lower):
            # Check for "X days"
            if "days" in message_lower:
                words = message_lower.split()
                for i, w in enumerate(words):
                    if w == "days" and i > 0 and words[i-1].isdigit():
                        updated_state["duration"] = words[i-1]
            # Fallback: Check for bare number if context suggests (e.g., just numeric) or if it's the likely answer
            # Simple heuristic: if message is just a number
            elif message.strip().isdigit():
                updated_state["duration"] = message.strip()

        if "solo" in message_lower: updated_state["travel_type"] = "Solo"
        if "family" in message_lower: updated_state["travel_type"] = "Family"
        if "adventure" in message_lower: updated_state["travel_type"] = "Adventure"
        if "honeymoon" in message_lower: updated_state["travel_type"] = "Honeymoon"

        # Determine next step
        missing = [field for field in REQUIRED_FIELDS if field not in updated_state]

        if not missing:
            return ("", updated_state, "ready_to_generate")
        
        # Ask for the first missing field
        next_field = missing[0]
        if next_field == "destination":
            return ("Welcome! I'm your travel assistant. Where would you like to go?", updated_state, "collecting_info")
        elif next_field == "duration":
            return (f"Great choice! How many days are you planning to stay in {updated_state.get('destination')}?", updated_state, "collecting_info")
        elif next_field == "month":
            return ("Which month or season do you plan to travel?", updated_state, "collecting_info")
        elif next_field == "travel_type":
            return ("What kind of trip is this? (e.g., Solo, Family, Adventure, Honeymoon)", updated_state, "collecting_info")

        return ("I didn't catch that. Could you clarify?", updated_state, "collecting_info")

    def _is_greeting(self, text: str) -> bool:
        return text.strip().lower() in ["hi", "hello", "hey", "start"]
