from app.services.llm_service import LLMService
from typing import Dict

class ResourceAgent:
    def __init__(self):
        self.llm = LLMService()

    def get_resources(self, destination: str, month: str, travel_type: str) -> Dict:
        """
        Coordinates the fetching of travel resources (Packing, Lingo, Budget).
        """
        print(f"[ResourceAgent] Generating resources for {destination}...")
        return self.llm.generate_travel_resources(destination, month, travel_type)
