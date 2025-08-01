import requests
from langchain_core.tools import tool
from dotenv import load_dotenv
import os
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

# @tool
def search_airport_id(query: str):
    """Search for the airport ID based on a city or destination name."""


    print("""   ----------------------------------------------------------------------

    airport_id tool is called


    -------------------------------------------------------------------------""")
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
            print(f"Found airport: {item['name']} with ID: {item['id']}")
            return item["id"]  # e.g., HYD.AIRPORT
        # print(f"No airport found for query: {query}")
        # print(f"Error for search_airport_id: {response.status_code} - {response.text}")
    return None

# @tool
def get_min_price(from_id: str, to_id: str, date: str):
    """Get the minimum flight price between two airports on a specific date."""
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
        "currency_code": "INR"
    }
    response = requests.get(url, headers=headers, params=params)
    print(f"Response status code for get_min_price: {response.json()}")
    return response.json()

@tool
def get_flights(from_city: str, to_city: str, date: str):
    """
    Find flights from one city to another on a specific date, using the search_airport_id. Use the results from serach_airport_id function as input to this function returning price and booking link.

    Args:
        from_city (str): The city to fly from.
        to_city (str): The city to fly to.
        date (str): The date of the flight in YYYY-MM-DD format.

    Returns:
        str: Flight details including price and booking link.
    """
    # Step 1: Get Airport IDs

    print("""
    ----------------------------------------------------------------------
          





    This tool is called 'get_flights'. 
    It helps you find the cheapest available flights between two cities 
    on a specific date. You just need to provide the departure city, 
    destination city, and the date of travel (in YYYY-MM-DD format).
    The tool will search for the relevant airports, fetch the minimum 
    available price, and provide you with a booking link for convenience.
          





    ----------------------------------------------------------------------
    """)
    from_id = search_airport_id(from_city)
    to_id = search_airport_id(to_city)

    if not from_id or not to_id:
        return f"Could not find airport codes for {from_city}:{from_id} or {to_city}:{to_id}."

    # Step 2: Get Flight Prices
    print(f"Searching for flights from {from_city} ({from_id}) to {to_city} ({to_id}) on {date}...")
    flight_data = get_min_price(from_id, to_id, date)

    if not flight_data.get("status"):
        return "Failed to fetch flight prices."

    flights = flight_data.get("data", [])
    if not flights:
        print(f"No flights found from {from_city} to {to_city} on {date}.")
        return f"No flights found from {from_city} to {to_city} on {date}."
    
    print(flights)
    # Taking the first cheapest flight
    cheapest_flight = flights[0]
    price = cheapest_flight.get("price")
    booking_link = cheapest_flight.get("deep_link")

    return f"The cheapest flight from {from_city} to {to_city} on {date} costs {price} AED.\nBooking Link: {booking_link}"


# # print(get_flights.invoke({"from_city": "Hyderabad", "to_city": "Dubai", "date": "2025-10-15"}))
# print("""
#       -----------------------------------------------------------------------
      
      
#       Logs
      
#       -----------------------------------------------------------------------""")
# # Example usage

# print(get_flights.invoke({"from_city": "Hyderabad", "to_city": "Dubai", "date": "2025-10-15"}))

