# main.py

import os
from dotenv import load_dotenv
from agents.explorer_agent import ExplorerAgent
from agents.budget_agent import BudgetAgent
from agents.food_agent import FoodAgent

# Load environment variables from .env file
load_dotenv()

def plan_trip(destination, budget):
    """
    Orchestrates the multi-agent collaboration to plan a weekend trip.
    """
    print(f"🤖 AI Weekend Travel Buddy is planning your trip to {destination}...")

    # 1. Instantiate Agents
    explorer = ExplorerAgent()
    budgeter = BudgetAgent()
    foodie = FoodAgent()

    # 2. Explorer Agent: Find attractions and create a basic itinerary
    print("\n🗺️ Explorer Agent is finding the best attractions...")
    attractions_result = explorer.find_attractions(destination)
    itinerary = attractions_result.get('itinerary', {})
    
    # Extract just the names for other agents
    attraction_names = [
        attraction['name'] 
        for day in itinerary.values() 
        for attraction in day
    ]
    
    if not attraction_names:
        print("Could not find any attractions. Please try another destination.")
        return

    print(f"Found attractions: {', '.join(attraction_names)}")

    # 3. Budget Agent: Distribute budget and estimate costs
    print("\n💰 Budget Agent is crunching the numbers...")
    budget_result = budgeter.distribute_budget(budget, attraction_names)
    budget_breakdown = budget_result.get('budget_breakdown', {})
    attraction_costs_list = budget_result.get('attraction_costs', [])
    attraction_costs = {item['name']: item['estimated_cost'] for item in attraction_costs_list}

    # 4. Food Agent: Recommend dining spots
    print("\n🍔 Food Agent is finding the tastiest local spots...")
    food_result = foodie.recommend_food(destination, attraction_names)
    food_recommendations_list = food_result.get('food_recommendations', [])
    food_recs = {item['attraction_name']: item for item in food_recommendations_list}
    
    # 5. Assemble and display the final itinerary
    print("\n✨ Here is your personalized weekend itinerary for", destination, "✨")
    print("-" * 60)
    
    if budget_breakdown:
        print(f"BUDGET OVERVIEW (Total: ${budget})")
        print(f"  🏨 Accommodation: ${budget_breakdown.get('accommodation', 'N/A')}")
        print(f"  🎟️ Activities: ${budget_breakdown.get('activities', 'N/A')}")
        print(f"  🍽️ Food: ${budget_breakdown.get('food', 'N/A')}")
        print(f"  🚖 Transportation: ${budget_breakdown.get('transportation', 'N/A')}")
        print("-" * 60)

    for day_num, attractions in itinerary.items():
        day_str = "Day 1" if day_num == "day1" else "Day 2"
        print(f"\n🗓️ {day_str.upper()}")
        for attraction in attractions:
            name = attraction['name']
            cost = attraction_costs.get(name, 'Free')
            food_rec = food_recs.get(name)

            print(f"\n  📍 {name}")
            print(f"     - Description: {attraction['description']}")
            print(f"     - Best Time: {attraction['best_time_to_visit']}")
            print(f"     - Duration: {attraction['estimated_duration']}")
            print(f"     - Estimated Cost: ${cost}")

            if food_rec:
                print("     - 🍽️ Nearby Food Suggestion:")
                print(f"       - Restaurant: {food_rec['restaurant_name']} ({food_rec['cuisine_type']})")
                print(f"       - Must-Try: {food_rec['must_try_dish']}")
    
    print("\nEnjoy your trip! 🎉")

if __name__ == "__main__":
    destination = input("Enter the city you want to visit: ")
    budget = input("Enter your total budget for the weekend (e.g., 500): ")
    
    if destination and budget:
        try:
            budget_amount = int(budget)
            plan_trip(destination, budget_amount)
        except ValueError:
            print("Invalid budget. Please enter a number.")
    else:
        print("Destination and budget are required.")
