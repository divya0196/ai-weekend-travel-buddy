import json

class Orchestrator:
    """
    A complex orchestrator that processes raw attraction data and generates a
    structured, time-optimized, and detailed 2-day itinerary.
    """
    def __init__(self):
        pass

    def _get_travel_time(self, start_place, end_place, travel_times_data):
        """
        Retrieves the travel time in minutes between two places from the provided data.
        Returns a default of 30 minutes if the time is not found.
        """
        for route in travel_times_data:
            if (route["from"] == start_place and route["to"] == end_place) or \
               (route["from"] == end_place and route["to"] == start_place):
                return route["time_minutes"]
        return 30 # Default travel time if not found

    def _optimize_route(self, attractions_for_day, travel_times_data):
        """
        Optimizes the visiting order of attractions using a greedy algorithm
        to minimize total travel time.
        """
        if not attractions_for_day:
            return []

        optimized_route = []
        unvisited = list(attractions_for_day)
        
        # Start with the highest-ranked attraction
        current_place = sorted(unvisited, key=lambda x: x["ranking"])[0]
        optimized_route.append(current_place)
        unvisited.remove(current_place)

        while unvisited:
            next_place = min(unvisited, key=lambda x: self._get_travel_time(
                current_place["name"], x["name"], travel_times_data
            ))
            optimized_route.append(next_place)
            unvisited.remove(next_place)
            current_place = next_place
            
        return optimized_route

    def _filter_by_budget(self, attractions, budget_level):
        """
        Filters the list of attractions based on the specified budget level.
        'low': includes only free attractions.
        'medium': includes attractions with a moderate entry fee (<= $50).
        'high': includes all attractions regardless of cost.
        """
        budget_level = budget_level.lower()
        if budget_level == 'low':
            return [a for a in attractions if a["entry_fee_usd"] == 0]
        elif budget_level == 'medium':
            return [a for a in attractions if a["entry_fee_usd"] <= 50]
        elif budget_level == 'high':
            return attractions
        else:
            return attractions # Default to 'high' budget if input is invalid

    def orchestrate_itinerary(self, destination, itinerary_data, budget):
        """
        Takes raw itinerary data and generates a complex 2-day travel plan,
        now considering the provided budget.
        """
        attractions_list = itinerary_data.get("attractions", [])
        travel_times_data = itinerary_data.get("travel_times_minutes", [])

        # Filter attractions based on the provided budget
        filtered_attractions = self._filter_by_budget(attractions_list, budget)
        
        # Sort filtered attractions by ranking
        sorted_attractions = sorted(filtered_attractions, key=lambda x: x["ranking"])
        
        # Split attractions into two days based on the new, filtered list
        midpoint = len(sorted_attractions) // 2
        day1_attractions = sorted_attractions[:midpoint]
        day2_attractions = sorted_attractions[midpoint:]

        # Optimize the route for each day
        day1_route = self._optimize_route(day1_attractions, travel_times_data)
        day2_route = self._optimize_route(day2_attractions, travel_times_data)

        final_itinerary = {
            "destination": destination,
            "itinerary": [
                self._create_daily_plan(1, day1_route, travel_times_data),
                self._create_daily_plan(2, day2_route, travel_times_data)
            ]
        }
        
        return final_itinerary

    def _create_daily_plan(self, day_number, attractions_route, travel_times_data):
        """
        Generates a detailed plan for a single day, including timing and costs.
        """
        daily_plan = {
            "day": f"Day {day_number}",
            "total_estimated_cost_usd": 0,
            "total_estimated_travel_time_minutes": 0,
            "activities": []
        }
        
        current_time_minutes = 9 * 60  # Start day at 9:00 AM

        for i, attraction in enumerate(attractions_route):
            # Add travel time from previous location
            if i > 0:
                previous_attraction = attractions_route[i - 1]
                travel_time = self._get_travel_time(previous_attraction["name"], attraction["name"], travel_times_data)
                daily_plan["total_estimated_travel_time_minutes"] += travel_time
                current_time_minutes += travel_time

            # Calculate activity start and end times
            start_time_str = f"{current_time_minutes // 60:02}:{current_time_minutes % 60:02}"
            duration_minutes = attraction["estimated_duration_hours"] * 60
            end_time_minutes = current_time_minutes + duration_minutes
            end_time_str = f"{end_time_minutes // 60:02}:{end_time_minutes % 60:02}"

            # Add to the daily plan
            activity = {
                **attraction,
                "start_time": start_time_str,
                "end_time": end_time_str
            }
            daily_plan["activities"].append(activity)
            
            # Update total cost for the day
            fee = attraction["entry_fee_usd"]
            if isinstance(fee, (int, float)):
                daily_plan["total_estimated_cost_usd"] += fee

            # Update current time for the next activity
            current_time_minutes = end_time_minutes

        return daily_plan
