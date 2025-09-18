from agents.explorer_agent import ExplorerAgent
from agents.budget_agent import BudgetAgent
from agents.food_agent import FoodAgent
import json
import pandas as pd
import os

# Set your OpenAI API key as an environment variable
# os.environ["OPENAI_API_KEY"] = "...."

def create_itinerary(destination, budget):
    # Initialize all agents
    explorer = ExplorerAgent()
    budgeter = BudgetAgent()
    foodie = FoodAgent()

    print("🤖 AI Weekend Travel Buddy is planning your trip...")
    print("--------------------------------------------------")

    # Step 1: Explorer Agent generates a list of attractions
    print("🌍 Step 1: Explorer Agent is finding the top attractions...")
    try:
        explorer_output = explorer.plan_activities(destination)
        attractions = explorer_output["attractions"]
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error from Explorer Agent: {e}")
        return "Could not generate attractions. Please try again."

    # Step 2: Budget Agent estimates costs
    print("💰 Step 2: Budget Agent is calculating costs...")
    try:
        budget_output = budgeter.distribute_budget(budget, attractions)
        budget_breakdown = budget_output["budget_breakdown"]
        attraction_costs = {item['name']: item['estimated_cost'] for item in budget_output["attraction_costs"]}
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error from Budget Agent: {e}")
        return "Could not estimate budget. Please try again."

    # Step 3: Food Agent finds food spots
    print("🍽️ Step 3: Food Agent is finding tasty spots...")
    try:
        food_output = foodie.find_food_spots(attractions)
        food_recommendations = {item['attraction_name']: item for item in food_output["food_recommendations"]}
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error from Food Agent: {e}")
        return "Could not find food spots. Please try again."

    # Step 4: Compile the final itinerary
    print("✨ Compiling the final 2-Day Itinerary...")
    itinerary_list = []
    
    # Simple logic to assign attractions to days
    day1_attractions = sorted(attractions, key=lambda x: x['ranking'])[0:2]
    day2_attractions = sorted(attractions, key=lambda x: x['ranking'])[2:4]

    for i, attraction in enumerate(day1_attractions):
        food_rec = food_recommendations.get(attraction['name'], {})
        itinerary_list.append({
            "Day": "Day 1",
            "Activity": attraction["name"],
            "Description": attraction["description"],
            "Estimated Cost": attraction_costs.get(attraction['name'], "N/A"),
            "Food Suggestion": f"{food_rec.get('restaurant_name', 'N/A')} - Try the {food_rec.get('local_dish_to_try', 'N/A')}. Tip: {food_rec.get('food_tip', 'N/A')}"
        })
    
    for i, attraction in enumerate(day2_attractions):
        food_rec = food_recommendations.get(attraction['name'], {})
        itinerary_list.append({
            "Day": "Day 2",
            "Activity": attraction["name"],
            "Description": attraction["description"],
            "Estimated Cost": attraction_costs.get(attraction['name'], "N/A"),
            "Food Suggestion": f"{food_rec.get('restaurant_name', 'N/A')} - Try the {food_rec.get('local_dish_to_try', 'N/A')}. Tip: {food_rec.get('food_tip', 'N/A')}"
        })
    
    itinerary_df = pd.DataFrame(itinerary_list)
    
    print("\n✅ Itinerary generated successfully!")
    print("\nTotal Budget Breakdown:")
    print(pd.Series(budget_breakdown).to_markdown())
    print("\n--- Your 2-Day Itinerary ---")
    print(itinerary_df.to_markdown(index=False))

    return itinerary_df

if __name__ == "__main__":
    # Example usage
    destination = "Goa, India"
    budget = 5000
    create_itinerary(destination, budget)
