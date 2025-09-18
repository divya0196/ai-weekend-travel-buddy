from .base_agent import Agent
import json

class FoodAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Culinary Expert",
            goal="Recommend top-rated restaurants, cafes, and street food near specific attractions, and add fun food tips.",
            backstory="You are a seasoned food blogger with an encyclopedic knowledge of local cuisines. You know the best places to eat near every major landmark and can provide engaging, useful food tips."
        )

    def find_food_spots(self, attractions_list):
        attractions_str = json.dumps(attractions_list)
        user_prompt = f"""
        For each attraction in the following list: {attractions_str}, recommend a nearby food spot.
        Respond with a JSON object containing an array of recommendations.
        
        Each recommendation should be an object with:
        - "attraction_name": The name of the attraction.
        - "restaurant_name": A recommended restaurant, cafe, or food spot.
        - "local_dish_to_try": A famous local dish to try at or near this spot.
        - "food_tip": A fun, short tip about the local food culture.

        Example of desired JSON output:
        {{
          "food_recommendations": [
            {{
              "attraction_name": "Eiffel Tower",
              "restaurant_name": "Creperie de l'Eiffel",
              "local_dish_to_try": "Nutella Crepe",
              "food_tip": "Look for a street vendor for the most authentic experience."
            }},
            ...
          ]
        }}
        """
        response = self.chat(user_prompt)
        return json.loads(response)
