import requests
from langchain_core.tools import tool
from dotenv import load_dotenv
import os
import json
import csv

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

def search_flights(from_id: str, to_id: str, date: str):
    """Search for flights between two airports on a specific date with full details."""
    url = f"https://{RAPIDAPI_HOST}/api/v1/flights/searchFlights"
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    params = {
        "fromId": from_id,
        "toId": to_id,
        "departDate": date,
        "cabinClass": "ECONOMY",
        "currency_code": "INR",
        "adults": 1
    }
    response = requests.get(url, headers=headers, params=params)
    print(f"Request URL: {response.url}")
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
    from_id = search_airport_id(from_city)
    to_id = search_airport_id(to_city)

    if not from_id or not to_id:
        return f"Could not find airport codes for {from_city}:{from_id} or {to_city}:{to_id}."

    print(f"Searching for flights from {from_city} ({from_id}) to {to_city} ({to_id}) on {date}...")
    
    url = f"https://{RAPIDAPI_HOST}/api/v1/flights/searchFlights"
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
    print(f"Response status code for search_flights: {response.status_code}")
    data = response.json()
    print(f"Response data: {data}")
    if not data.get("status"):
        return "Failed to fetch flight details."

    flight_offers = data.get("data", {}).get("flightOffers", [])
    print(f"Number of flight offers found: {len(flight_offers)}")
    if not flight_offers:
        return f"No flights found from {from_city} to {to_city} on {date}."

    flight_results = []
    for offer in flight_offers:
        token = offer.get("token")
        # Assuming price is inside offer (adjust if necessary)
        price = offer.get("priceBreakdown", {}).get("total", {}).get("units", "N/A") 
        currency = offer.get("priceBreakdown", {}).get("total", {}).get("currencyCode", "INR")
        segment = offer.get("segments", [])[0]  # Taking first segment
        departure_time = segment.get("departureTime")
        arrival_time = segment.get("arrivalTime")
        flight_info = segment.get("legs", [])[0].get("flightInfo", {})
        flight_number = flight_info.get("flightNumber")
        carrier = flight_info.get("carrierInfo", {}).get("marketingCarrier")

        flight_data = {
            "from_city": from_city,
            "to_city": to_city,
            "date": date,
            "token": token,
            "price": price,
            "flight_number": flight_number,
            "carrier": carrier,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "currency": currency
        }

        flight_results.append(flight_data)

    # Sort by price
    flight_results = sorted(flight_results, key=lambda x: float(x["price"]) if x["price"] != "N/A" else float('inf'))

    # Save to JSON
    with open('flights_data.json', 'w') as json_file:
        json.dump(flight_results, json_file, indent=4)

    # Save to CSV
    with open('flights_data.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=flight_results[0].keys())
        writer.writeheader()
        writer.writerows(flight_results)

    print("Flight data saved to flights_data.json and flights_data.csv")

    # Prepare summary text for top 5 flights
    result_text = "Top 5 Cheapest Flights:\n\n"
    for flight in flight_results[:5]:
        result_text += f"Flight {flight['carrier']}{flight['flight_number']}: {flight['departure_time']} -> {flight['arrival_time']}\n"
        result_text += f"Price: {flight['price']} INR\n"
        result_text += f"Token: {flight['token'][:10]}...\n\n"  # Truncate token for display

    return result_text


# Example usage:
if __name__ == "__main__":
    from_city = "Hyderabad"
    to_city = "Delhi"
    date = "2025-10-15"

    print(get_flights.invoke({"from_city": from_city, "to_city": to_city, "date": date}))
