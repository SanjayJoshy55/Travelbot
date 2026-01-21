import os
from groq import Groq
from typing import Dict, List

class LLMService:
    def __init__(self):
        # 1. Try Environment Variable, 2. Fallback to the known demo key
        self.api_key = os.getenv("GROQ_API_KEY")
        
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
            self.model = "llama-3.1-8b-instant" # Using 8b instant for speed
        else:
            print("Warning: GROQ_API_KEY not found. LLM features will be mocked.")
            self.client = None

    def generate_trip_narrative(self, destination: str, duration: str, context: str, daily_plan: Dict) -> str:
        """
        Generates a cohesive travel narrative using the LLM.
        """
        if not self.client:
            return self._mock_response(destination, context)
            
        # Construct Prompt
        plan_text = ""
        for day, places in daily_plan.items():
            names = ", ".join([p['name'] for p in places])
            plan_text += f"- Day {day}: {names}\n"

        prompt = f"""
        You are an elite travel concierge. Design a premium {duration}-day itinerary for {destination}.
        
        # INPUT DATA
        CONTEXT: {context[:2000]}
        DRAFT SCHEDULE:
        {plan_text}

        # INSTRUCTIONS
        1. **Role**: Be sophisticated, enthusiastic, and helpful. 
        2. **Formatting**: 
           - Use strictly nice Markdown.
           - Use Headers (##) for Days.
           - Use bolding for place names.
        3. **Content**:
           - Flesh out the "Draft Schedule" into a full narrative.
           - Add "🍽️ Local Flavour" recommendations for lunch/dinner (hallucinate plausible highly-rated types of food if specific names aren't known).
           - Add "💡 Insider Tip" for each day.
        4. **Style**:
           - Don't be robotic.
           - Use emojis tastefully.
        
        Create the itinerary now.
        """
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.7
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"LLM Generation Error: {e}")
            # Fallback to mock if API fails
            return self._mock_response(destination, context, error_message=str(e))

    def _mock_response(self, destination, context="", error_message=""):
        return f"""
        # ⚠️ AI Service Unavailable
        
        **Error Details:** `{error_message}`
        
        **We successfully gathered data, but the AI Writer is offline.**
        
        ### What we found for {destination}:
        {context[:500]}...
        """

    def generate_travel_resources(self, destination: str, month: str, travel_type: str) -> Dict:
        """
        Generates structured resources: Packing List, Lingo, Budget.
        Returns a Dict.
        """
        import json
        
        default_response = {
            "packing_list": ["Comfortable shoes", "Universal adapter", "Power bank"],
            "lingo": [{"phrase": "Hello", "translation": "Hello"}],
            "budget": [{"item": "Coffee", "cost": "Unknown"}]
        }

        if not self.client:
            return default_response

        prompt = f"""
        Act as a travel expert. Generate a JSON object for a trip to {destination} in {month} ({travel_type}).
        
        The JSON must strictly follow this schema:
        {{
            "packing_list": ["item 1", "item 2", ...],
            "lingo": [{{"phrase": "English Phrase", "translation": "Local Phrase"}}],
            "budget": [{{"item": "Coffee/Meal/Transport", "cost": "Local Price"}}],
            "tip": "One cultural tip"
        }}
        
        Requirements:
        1. packing_list: 5-7 items specific to weather in {month} and activities.
        2. lingo: 5 essential phrases (Hello, Thank you, Please, etc).
        3. budget: 3 items (Coffee, Lunch, Taxi 1km).
        4. tip: A cultural "do/don't".
        
        Response must be PURE JSON only. No markdown formatting.
        """
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            content = chat_completion.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"LLM Resource Gen Error: {e}")
            return default_response
