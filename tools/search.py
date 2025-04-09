import tavily

def general_search(query: str, limit: int = 5) -> list:
    """
    Perform a general search using the Tavily API.

    Args:
        query (str): The search query.
        limit (int): The maximum number of results to return.

    Returns:
        list: A list of search results.
    """
    return f'{tavily.search(query, limit)}'