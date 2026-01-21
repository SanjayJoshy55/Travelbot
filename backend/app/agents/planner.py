from app.services.planner_service import PlannerService
from typing import List, Dict

class PlannerAgent:
    def __init__(self):
        self.service = PlannerService()

    def create_daily_plan(self, destination: str, duration: int, attractions: List[Dict]) -> Dict:
        """
        Groups attractions into a daily schedule based on proximity.
        """
        print(f"[Planner] Clustering {len(attractions)} attractions into {duration} days...")
        
        # If no attractions provided (e.g. pure research mode), mock some based on city center
        if not attractions:
            # We rely on the Writer to hallucinate specific spots if we only have generic info,
            # BUT for the Map to work, we ideally want coordinates.
            # For this MVP, we pass an empty list and let the Writer handle the narrative,
            # or we could implement a "Place Search" here if we had Google Places.
            return {}

        daily_plan = self.service.group_attractions_by_day(attractions, duration)
        return daily_plan
