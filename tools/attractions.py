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
        A List of attractions in the specified city.
    """
    url = "https://booking-com15.p.rapidapi.com/api/v1/attraction/searchLocation"

    querystring = {"query": query, "languagecode": languagecode}

    headers = {
        "x-rapidapi-key": "112e989570msh9edb0829bd0a68ep1d5001jsn898c1ee525a5",  # Replace with your actual key
        "x-rapidapi-host": "booking-com15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    atx=[]
    if response.status_code == 200:
        data = response.json()
        for product in data['data']['products']:
            atx.append(product['title'])
        return atx
    else:
        return f"Error: {response.status_code} - {response.text} "