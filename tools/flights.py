from typing import Dict

def get_flights(from_city: str, to_city: str, date: str):
    """
    Find flights from one city to another on a specific date.
    
    Args:
        from_city (str): The city to fly from.
        to_city (str): The city to fly to.
        date (str): The date of the flight in MM/DD/YYYY format.
        
    Returns:
        str: A message indicating the flight search details.
    """
    return f'Searching for flights from {from_city} to {to_city} on {date}.'