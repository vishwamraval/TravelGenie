from datetime import datetime
from langchain_core.tools import tool

@tool
def get_current_year():
    """
    Returns the current year as an integer.
    """
    return datetime.now().year