# agents/explorer_agent.py
from .base_agent import Agent
import json

class ExplorerAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Senior Travel Researcher",
            goal="Identify and rank the top attractions and activities for a 2-day trip to a specific destination, including essential logistical details.",
            backstory="You are an expert travel researcher with an encyclopedic knowledge of popular destinations. You can instantly recall key details like opening hours, typical entry fees, and estimated travel times between major landmarks. Your knowledge is based on general information, not real-time data."
        )

    def plan_activities(self, destination):
        user_prompt = f"""
        Generate a list of the top 5 must-see attractions and activities for a 2-day trip to {destination}.
        For each attraction, provide the following details in a JSON object format:
        - "name": The name of the attraction.
        - "description": A brief description of the place.
        - "category": The type of attraction (e.g., "Museum", "Landmark", "Park").
        - "estimated_duration_hours": The time in hours a visit typically takes.
        - "ranking": An integer from 1 to 5, with 1 being the most essential.
        - "opening_hours": A plausible, common schedule (e.g., "9:00 AM - 6:00 PM, daily except Monday").
        - "entry_fee_usd": An estimated entry fee in USD, if applicable (use "Free" for no fee).

        Additionally, provide a section for travel times.
        - "travel_times_minutes": An array of objects estimating travel time between the top ranked attractions.
          - "from": The name of the starting attraction.
          - "to": The name of the destination attraction.
          - "time_minutes": Estimated travel time in minutes.

        Example of desired JSON output:
        {{
          "attractions": [
            {{
              "name": "Eiffel Tower",
              "description": "An iconic iron lattice tower.",
              "category": "Landmark",
              "estimated_duration_hours": 2,
              "ranking": 1,
              "opening_hours": "9:30 AM - 11:45 PM, daily",
              "entry_fee_usd": 28.30
            }},
            ...
          ],
          "travel_times_minutes": [
            {{
              "from": "Eiffel Tower",
              "to": "Louvre Museum",
              "time_minutes": 25
            }},
            ...
          ]
        }}
        """
        response = self.chat(user_prompt)
        return json.loads(response)
