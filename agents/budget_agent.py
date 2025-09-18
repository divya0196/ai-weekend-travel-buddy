from .base_agent import Agent
import json

class BudgetAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Financial Planner",
            goal="Distribute a total budget across trip components and estimate the cost for each activity.",
            backstory="You are a meticulous financial analyst specializing in travel. You can accurately estimate costs for a trip based on a total budget, ensuring a realistic and financially sound plan. Your estimates are based on general knowledge and not real-time prices."
        )

    def distribute_budget(self, total_budget, activities):
        activities_str = json.dumps(activities)
        user_prompt = f"""
        Given a total budget of ${total_budget} and the following list of attractions: {activities_str},
        do the following tasks and respond in a JSON object format:

        1. Provide a breakdown of the total budget into categories:
           - "accommodation": Estimated cost for a 2-night stay.
           - "activities": Estimated cost for all activities.
           - "food": Estimated cost for all meals.
           - "transportation": Estimated cost for local travel.

        2. For each of the attractions provided, estimate the individual cost.
        - "attraction_costs": An array of objects, each with "name" and "estimated_cost".

        Example of desired JSON output:
        {{
          "budget_breakdown": {{
            "accommodation": 200,
            "activities": 150,
            "food": 100,
            "transportation": 50
          }},
          "attraction_costs": [
            {{ "name": "Eiffel Tower", "estimated_cost": 25 }},
            ...
          ]
        }}
        """
        response = self.chat(user_prompt)
        return json.loads(response)
