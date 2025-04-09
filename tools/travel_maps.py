# travel_maps.py
def generate_travel_map(start_city, destinations, travel_dates):
    """
    Generate a travel map based on the starting city, destinations, and travel dates.

    Args:
        start_city (str): The starting city for the travel plan.
        destinations (list): A list of destination cities.
        travel_dates (list): A list of travel dates.

    Returns:
        str: URL of the generated travel map.
    """
    return f"Running travel map generation from {start_city} to {', '.join(destinations)} on {', '.join(travel_dates)}."
