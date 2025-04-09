def get_hotels(city: str, check_in: str, check_out: str) -> str:
    """
    Find hotels in a specific city for a given check-in and check-out date.

    Args:
        city (str): The city to find hotels in.
        check_in (str): The check-in date in YYYY-MM-DD format.
        check_out (str): The check-out date in YYYY-MM-DD format.

    Returns:
        str: A message indicating the available hotels.
    """
    return f"Searching for hotels in {city} from {check_in} to {check_out}."
