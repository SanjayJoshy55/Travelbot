from app.agents.researcher import ResearcherAgent
from app.agents.planner import PlannerAgent
from app.agents.writer import WriterAgent
from typing import Dict

class DirectorAgent:
    def __init__(self):
        print("[Director] Hiring crew...")
        self.researcher = ResearcherAgent()
        self.planner = PlannerAgent()
        self.writer = WriterAgent()

    def create_itinerary(self, state: Dict) -> Dict:
        """
        Orchestrates the creation of a full itinerary.
        Returns structured dict {narrative, meta}.
        """
        dest = state.get("destination", "Unknown")
        dur = state.get("duration", "3")
        travel_type = state.get("travel_type", "Leisure")
        
        # 1. Research
        print(f"[Director] Instructing Researcher to analyze {dest}...")
        research_data = self.researcher.research_destination(dest)
        
        # 2. Plan
        # Parse duration
        try:
            day_count = int(dur.split()[0])
        except:
            day_count = 3
            
        print(f"[Director] Instructing Planner to schedule {day_count} days...")
        daily_plan = self.planner.create_daily_plan(dest, day_count, research_data.get("attractions", []))
        
        # 3. Write
        print(f"[Director] Instructing Writer to compile narrative...")
        narrative = self.writer.write_itinerary(
            destination=dest,
            duration=dur,
            context=research_data["context"],
            daily_plan=daily_plan,
            travel_type=travel_type
        )
        
        # 4. Construct Final Deliverable
        # Prioritize local/wiki images
        img = None
        if research_data["images"]:
            img = research_data["images"][0]
            
        return {
            "narrative": narrative,
            "meta": {
                "destination": dest,
                "coordinates": research_data["coordinates"],
                "image": img,
                "context": research_data["context"], # useful for subsequent edits
                "daily_plan": daily_plan # useful for subsequent edits
            }
        }

    def modify_itinerary(self, current_result: Dict, user_request: str) -> Dict:
        """
        Handles interactive modification using the Writer.
        """
        print(f"[Director] Modification request: {user_request}")
        
        old_narrative = current_result.get("narrative", "")
        
        # In a full MAS, we might re-plan. For now, we ask Writer to rewrite.
        new_narrative = self.writer.modify_itinerary(old_narrative, user_request)
        
        updated_result = current_result.copy()
        updated_result["narrative"] = new_narrative
        
        return updated_result
