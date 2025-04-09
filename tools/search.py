# search.py
# Reference: https://docs.tavily.com/sdk/python/reference
from tavily import TavilyClient
import dotenv

dotenv.load_dotenv()

client = TavilyClient()


def general_search(query: str) -> str:
    """
    Perform a general search using the Tavily API.
    Args:
        query (str): The search query.
    Returns:
        str: The search results.
    """
    result = client.search(query=query, search_depth="basic", max_results=5)
    return result


# Example search
search_results = general_search("Paris")
print(search_results)
