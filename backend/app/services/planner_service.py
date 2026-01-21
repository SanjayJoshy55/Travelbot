import numpy as np
from sklearn.cluster import KMeans
from typing import List, Dict, Any

class PlannerService:
    """
    Intelligent Planner that groups attractions by location (clustering)
    and optimizes the order of visits.
    """
    
    def group_attractions_by_day(self, attractions: List[Dict], days: int) -> Dict[int, List[Dict]]:
        """
        Uses K-Means clustering to group attractions into 'days' based on their
        lat/lon coordinates. This ensures Day 1 visits are close to each other, etc.
        """
        if not attractions:
            return {}
            
        # If fewer attractions than days, just put one per day or group all in Day 1 used logic
        if len(attractions) < days:
             # Just map them sequentially
             return {i+1: [attr] for i, attr in enumerate(attractions)}
        
        # Prepare coordinates for clustering
        # OpenTripMap returns lat/lon.
        coords = np.array([[a['point']['lat'], a['point']['lon']] if 'point' in a else [0,0] for a in attractions])
        
        # If 'point' is missing (Mock data might handle differently), check structure
        # Phase 2 mock data: {"name": ..., "dist": ...} -> missing lat/lon?
        # Real data has 'point': {'lat': ..., 'lon': ...}
        # Let's verify structure in helper.
        
        # Fixing coord extraction for robustness
        clean_coords = []
        valid_indices = []
        for i, attr in enumerate(attractions):
            if 'point' in attr:
                clean_coords.append([attr['point']['lat'], attr['point']['lon']])
                valid_indices.append(i)
            elif 'lat' in attr and 'lon' in attr: # Fallback
                clean_coords.append([attr['lat'], attr['lon']])
                valid_indices.append(i)
                
        if len(clean_coords) < days:
             return {1: attractions} # Fallback to everything on Day 1
             
        X = np.array(clean_coords)
        
        # K-Means Clustering
        kmeans = KMeans(n_clusters=days, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)
        
        # Organize by Day
        day_plan = {day: [] for day in range(1, days + 1)}
        for coord_idx, label in zip(valid_indices, labels):
            day_num = label + 1 # 1-based day
            day_plan[day_num].append(attractions[coord_idx])
            
        return day_plan

    def optimize_route(self, day_attractions: List[Dict]) -> List[Dict]:
        """
        Simple heuristic: Sort by distance from the first item (assumed starting point)
        or just keep clustering order? 
        For MVP Phase 4, let's just keep them as-is or sort by popularity/rating if available.
        OpenTripMap has 'rate' (1, 2, 3, etc).
        """
        # Sort by rating descending (most popular first)
        return sorted(day_attractions, key=lambda x: x.get('rate', 0), reverse=True)
