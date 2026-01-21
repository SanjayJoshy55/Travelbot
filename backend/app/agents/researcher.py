from app.services.wikipedia_service import WikipediaService
from app.services.rag_service import RagService
from typing import Dict, List
import os

import json
import os

class ResearcherAgent:
    def __init__(self):
        self.wiki = WikipediaService()
        try:
            self.rag = RagService(persist_path="./chroma_db")
        except:
            self.rag = None
            
        # Load local dataset
        self.dataset = {}
        try:
            # Adjust path to point to app/data/dataset.json
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, "..", "data", "dataset.json")
            if os.path.exists(data_path):
                with open(data_path, "r") as f:
                    self.dataset = json.load(f)
        except Exception as e:
            print(f"Error loading dataset: {e}")

    def research_destination(self, destination: str) -> Dict:
        """
        Gathers raw data, images, and context about a destination.
        """
        print(f"[Researcher] Starting research on {destination}...")
        
        data = {
            "description": "",
            "coordinates": {"lat": 0, "lon": 0},
            "images": [],
            "context": "",
            "attractions": [] # List of attraction objects
        }
        
        # 1. Local Dataset Lookup
        local_data = None
        for key in self.dataset:
            if key.lower() in destination.lower():
                local_data = self.dataset[key]
                break
        
        if local_data:
            data["attractions"] = local_data.get("attractions", [])
            if "geo" in local_data:
                data["coordinates"] = {"lat": local_data["geo"]["lat"], "lon": local_data["geo"]["lon"]}
                
        # 2. Wiki Search (Enrichment + Images)
        results = self.wiki.search_location(destination)
        if results:
            details = self.wiki.get_location_details(results[0])
            
            # Fill description if missing
            data["description"] = details.get("summary", "")
            data["context"] = details.get("summary", "")
            
            # Fill images (Prioritize Wiki images)
            data["images"] = details.get("images", [])
            
            # Fill Coords if missing locally
            if data["coordinates"]["lat"] == 0 and details.get("coordinates"):
                data["coordinates"] = details["coordinates"]

        # 3. RAG Search (Optional enrichment)

        # 2. RAG Search (Optional enrichment)
        if self.rag:
            rag_results = self.rag.query(f"Interesting facts about {destination}", n_results=1)
            if rag_results:
                data["context"] += f"\n\n[RAG Insight]: {rag_results[0]['text']}"
                
        print(f"[Researcher] Found {len(data['images'])} images and context length {len(data['context'])}.")
        return data
