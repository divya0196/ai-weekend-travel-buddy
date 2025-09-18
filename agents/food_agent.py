# agents/food_agent.py

from .base_agent import Agent
import json

class FoodAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Local Food Critic",
            goal="Recommend top-rated and authentic dining experiences near given attractions.",
            backstory="You are a passionate food blogger who lives to explore the culinary scene of every city. You know where to find the best meals, from fine dining restaurants to hidden street food stalls, and love sharing local must-try dishes."
        )

    def recommend_food(self, destination, attractions):
        attractions_str = ", ".join(attractions)
        user_prompt = f"""
        For a trip to {destination}, I will be visiting these attractions: {attractions_str}.
        
        Your task is to recommend one great food spot near each attraction. 
        For each recommendation, provide:
        - "attraction_name": The name of the nearby attraction.
        - "restaurant_name": The name of the recommended restaurant, cafe, or food stall.
        - "cuisine_type": The type of food they serve (e.g., "Local Thai", "Italian", "Cafe").
        - "must_try_dish": A signature or highly recommended dish.

        Return the response as a JSON object with a single key "food_recommendations", which is a list of objects.
        
        Example of desired JSON output:
        {{
          "food_recommendations": [
            {{
              "attraction_name": "Eiffel Tower",
              "restaurant_name": "Le Jules Verne",
              "cuisine_type": "Modern French",
              "must_try_dish": "Seared Scallops"
            }},
            {{
              "attraction_name": "Louvre Museum",
              "restaurant_name": "Le Fumoir",
              "cuisine_type": "Classic French Bistro",
              "must_try_dish": "Steak Frites"
            }}
          ]
        }}
        """
        response = self.chat(user_prompt)
        return json.loads(response)
