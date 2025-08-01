from .flights import get_flights
from .hotels import get_hotels
from .car_rental import rent_car
from .attractions import get_attractions
from .search import general_search
from .date import get_current_year
# from .min_price import get_min_price
from .flights import search_airport_id

tool_registry = {
    "get_flights": get_flights,
    "get_hotels": get_hotels,
    "rent_car": rent_car,
    "get_attractions": get_attractions,
    "get_current_year": get_current_year,
    "search": general_search,
    # "get_min_price": get_min_price,
    "search_airport_id": search_airport_id,
}
