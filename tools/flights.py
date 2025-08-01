import requests
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")


def search_airport_id(query: str):
    url = f"https://{RAPIDAPI_HOST}/api/v1/flights/searchDestination"
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    params = {"query": query}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    for item in data.get("data", []):
        if item["type"] == "AIRPORT":
            return item["id"]  # e.g., HYD.AIRPORT
    return None

def get_min_price(from_id: str, to_id: str, date: str):
    url = f"https://{RAPIDAPI_HOST}/api/v1/flights/getMinPrice"
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    params = {
        "fromId": from_id,
        "toId": to_id,
        "departDate": date,
        "cabinClass": "ECONOMY",
        "currency_code": "AED"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

@tool
def get_flights(from_city: str, to_city: str, date: str):
    """
    Find flights from one city to another on a specific date, returning price and booking link.

    Args:
        from_city (str): The city to fly from.
        to_city (str): The city to fly to.
        date (str): The date of the flight in YYYY-MM-DD format.

    Returns:
        str: Flight details including price and booking link.
    """
    # Step 1: Get Airport IDs
    from_id = search_airport_id(from_city)
    to_id = search_airport_id(to_city)

    if not from_id or not to_id:
        return f"Could not find airport codes for {from_city} or {to_city}."

    # Step 2: Get Flight Prices
    flight_data = get_min_price(from_id, to_id, date)

    if not flight_data.get("status"):
        return "Failed to fetch flight prices."

    flights = flight_data.get("data", [])
    if not flights:
        return f"No flights found from {from_city} to {to_city} on {date}."

    # Taking the first cheapest flight
    cheapest_flight = flights[0]
    price = cheapest_flight.get("price")
    booking_link = cheapest_flight.get("deep_link")

    return f"The cheapest flight from {from_city} to {to_city} on {date} costs {price} AED.\nBooking Link: {booking_link}"
