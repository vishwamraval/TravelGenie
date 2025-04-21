# def get_attractions(city: str, date: str) -> str:
#     """
#     Find attractions in a specific city on a given date.

#     Args:
#         city (str): The city to find attractions in.
#         date (str): The date of the visit in YYYY-MM-DD format.

#     Returns:
#         str: A message indicating the available attractions.
#     """

from langchain.tools import tool
import requests

@tool
def get_attractions(query: str, languagecode: str = "en-us") -> str:
    """
    Fetches location coordinates and region info from a city or place name using the Booking.com API.

    Args:
        query: City or destination name (e.g., "Hyderabad").
        languagecode: Language for the results (default is "en-us").

    Returns:
        A string with location details (like region, city, and coordinates).
    """
    url = "https://booking-com15.p.rapidapi.com/api/v1/attraction/searchLocation"

    querystring = {"query": query, "languagecode": languagecode}

    headers = {
        "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",  # Replace with your actual key
        "x-rapidapi-host": "booking-com15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        if data and "results" in data and data["results"]:
            top_result = data["results"][0]
            name = top_result.get("name", "Unknown")
            lat = top_result.get("latitude")
            lon = top_result.get("longitude")
            region = top_result.get("region", {}).get("name", "")
            return f"{name} in {region} is located at latitude {lat}, longitude {lon}."
        else:
            return "No location found for that query."
    else:
        return f"Failed to fetch location. Status code: {response.status_code}"

    return f"Searching for attractions in {city} on {date}."
