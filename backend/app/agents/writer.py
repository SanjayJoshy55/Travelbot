from app.services.llm_service import LLMService
from typing import Dict

class WriterAgent:
    def __init__(self):
        self.llm = LLMService()

    def write_itinerary(self, destination: str, duration: str, context: str, daily_plan: Dict, travel_type: str) -> str:
        """
        Synthesizes the research and plan into a final markdown story.
        """
        print(f"[Writer] Drafting itinerary for {destination} ({travel_type})...")
        
        # Construct a rich prompt
        narrative = self.llm.generate_trip_narrative(
            destination=destination,
            duration=duration,
            context=context,
            daily_plan=daily_plan
        )
        return narrative

    def modify_itinerary(self, current_itinerary: str, user_request: str) -> str:
        """
        Rewrites an itinerary based on user feedback.
        """
        # We need to expose a generic method in LLMService or call client directly.
        # For now, let's assume LLMService has a generic chat method or we extend it.
        # Let's extend LLMService logic here for now.
        
        prompt = f"""
        You are editing a travel itinerary. 
        
        # ORIGINAL ITINERARY
        {current_itinerary}
        
        # USER CHANGE REQUEST
        "{user_request}"
        
        # INSTRUCTIONS
        - Apply the change REQUESTED.
        - Keep the rest of the itinerary distinct and formatted nicely.
        - Do NOT acknowledge the request ("Okay, I changed it..."), just return the NEW markdown.
        """
        
        if self.llm.client:
             response = self.llm.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.llm.model,
                temperature=0.7
            )
             return response.choices[0].message.content
        else:
            return current_itinerary + "\n\n(Simulation: Modified based on request)"
