# agents/explorer_agent.py

from .base_agent import Agent
import json

class ExplorerAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Expert Tour Guide",
            goal="Find the best attractions and create an optimized 2-day itinerary for a given destination.",
            backstory="You are a seasoned world traveler with a knack for discovering hidden gems. You can quickly identify the must-see spots in any city and organize them into a logical and enjoyable itinerary, balancing popular sites with unique local experiences."
        )

    def find_attractions(self, destination):
        user_prompt = f"""
        Create a 2-day weekend itinerary for a trip to {destination}.
        For each day, list 2-3 key attractions or activities. The plan should be logical, minimizing travel time between places.
        
        For each attraction, provide:
        - "name": The name of the attraction.
        - "description": A brief, engaging one-sentence description.
        - "estimated_duration": How long to spend there (e.g., "2-3 hours").
        - "best_time_to_visit": The best time of day to go (e.g., "Morning", "Afternoon").

        Return the response as a JSON object with a single key "itinerary" which contains an object with "day1" and "day2" as keys. Each day should be a list of attraction objects.
        
        Example of desired JSON output:
        {{
          "itinerary": {{
            "day1": [
              {{
                "name": "Louvre Museum",
                "description": "Home to masterpieces like the Mona Lisa and the Venus de Milo.",
                "estimated_duration": "3-4 hours",
                "best_time_to_visit": "Morning"
              }}
            ],
            "day2": [
               {{
                "name": "Eiffel Tower",
                "description": "Iconic iron tower offering breathtaking panoramic views of Paris.",
                "estimated_duration": "2-3 hours",
                "best_time_to_visit": "Evening"
              }}
            ]
          }}
        }}
        """
        response = self.chat(user_prompt)
        return json.loads(response)
