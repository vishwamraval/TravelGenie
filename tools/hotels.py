from langchain.tools import tool
import requests
import json

API_KEY = "b948bbfd4cmsh14ab1def603a52ap1724e7jsn2350fde52ee3"
API_HOST = "booking-com15.p.rapidapi.com"


@tool
def get_hotels(
    query: str,
    arrival_date: str,
    departure_date: str,
    languagecode: str = "en-us",
    adults: int = 1,
    children: int = 0,
) -> str:
    """
    Fetch hotels based on a city or destination name.

    Args:
        query (str): City or destination name.
        arrival_date (str): Check-in date (YYYY-MM-DD).
        departure_date (str): Check-out date (YYYY-MM-DD).
        languagecode (str, optional): Language code (default: 'en-us').
        adults (int, optional): Number of adults (default: 1).
        children (int, optional): Number of children (default: 0).

    Returns:
        str: A JSON string with the top 5 hotel listings, including name, location, price, rating, and number of reviews.
             Returns an error message if no hotels are found or if the API request fails.
    """
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST,
    }

    # Step 1: Get destination ID
    destination_url = f"https://{API_HOST}/api/v1/hotels/searchDestination"
    destination_params = {"query": query}
    dest_response = requests.get(
        destination_url, headers=headers, params=destination_params
    )

    if dest_response.status_code != 200:
        return f"Error retrieving destination: {dest_response.status_code} - {dest_response.text}"

    dest_data = dest_response.json()
    if not dest_data.get("data"):
        return "Error: No destination found."

    dest_id = dest_data["data"][0].get("dest_id")
    if not dest_id:
        return "Error: Could not retrieve destination ID."

    # Step 2: Get hotel listings
    hotels_url = f"https://{API_HOST}/api/v1/hotels/searchHotels"
    hotels_params = {
        "dest_id": dest_id,
        "search_type": "CITY",
        "adults": str(adults),
        "children_age": "0" if children == 0 else ",".join(["5"] * children),
        "room_qty": "1",
        "page_number": "1",
        "units": "metric",
        "temperature_unit": "c",
        "languagecode": languagecode,
        "currency_code": "USD",
        "location": "US",
        "arrival_date": arrival_date,
        "departure_date": departure_date,
    }

    hotels_response = requests.get(hotels_url, headers=headers, params=hotels_params)
    if hotels_response.status_code != 200:
        return f"Error retrieving hotels: {hotels_response.status_code} - {hotels_response.text}"

    hotel_data = hotels_response.json()
    hotels = hotel_data.get("data", {}).get("hotels", [])

    if not isinstance(hotels, list) or not hotels:
        return "No hotels found."

    listings = []
    for hotel in hotels:
        if not isinstance(hotel, dict):
            continue

        prop = hotel.get("property", {})
        name = prop.get("name", "N/A")
        address = (
            hotel.get("accessibilityLabel", "").split("\n")[3].strip()
            if hotel.get("accessibilityLabel")
            else "N/A"
        )
        price = (
            "{:.2f}".format(
                float(
                    prop.get("priceBreakdown", {})
                    .get("grossPrice", {})
                    .get("value", "N/A")
                )
            )
            if prop.get("priceBreakdown", {}).get("grossPrice", {}).get("value", "N/A")
            != "N/A"
            else "N/A"
        )
        currency = (
            prop.get("priceBreakdown", {}).get("grossPrice", {}).get("currency", "USD")
        )
        rating = prop.get("reviewScore", "N/A")
        reviews = prop.get("reviewCount", "N/A")

        listings.append(
            f"🏨 {name}\n📍 Location: {address}\n💲 Price: {currency} {price}\n⭐ Rating: {rating} ({reviews} reviews)\n"
        )

    if not listings:
        return "No valid hotel listings available."

    # Convert the first 5 hotel listings to JSON
    hotel_data = []
    for listing in listings[:5]:
        # Parse each listing string to extract hotel details
        lines = listing.split("\n")
        name = lines[0].split("🏨 ")[1] if len(lines) > 0 else "N/A"
        location = lines[1].split("📍 Location: ")[1] if len(lines) > 1 else "N/A"
        price_str = lines[2].split("💲 Price: ")[1] if len(lines) > 2 else "N/A"
        currency = price_str.split(" ")[0] if price_str != "N/A" else "USD"
        price = (
            price_str.split(" ")[1]
            if price_str != "N/A" and len(price_str.split(" ")) > 1
            else "N/A"
        )
        rating_str = lines[3].split("⭐ Rating: ")[1] if len(lines) > 3 else "N/A"
        rating = rating_str.split(" ")[0] if rating_str != "N/A" else "N/A"
        reviews = (
            rating_str.split("(")[1].split(" ")[0]
            if rating_str != "N/A" and "(" in rating_str
            else "N/A"
        )

        hotel_data.append(
            {
                "name": name,
                "location": location,
                "currency": currency,
                "price": price,
                "rating": rating,
                "reviews": reviews,
            }
        )

    return json.dumps(hotel_data, indent=2)
