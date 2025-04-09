def get_attractions(city: str, date: str) -> str:
    """
    Find attractions in a specific city on a given date.

    Args:
        city (str): The city to find attractions in.
        date (str): The date of the visit in YYYY-MM-DD format.

    Returns:
        str: A message indicating the available attractions.
    """
    return f"Searching for attractions in {city} on {date}."
