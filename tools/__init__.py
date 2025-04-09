from .flights import get_flights
from .hotels import get_hotels
from .car_rental import rent_car
from .attractions import get_attractions
from .search import general_search

tool_registry = {
    "get_flights": get_flights,
    "get_hotels": get_hotels,
    "rent_car": rent_car,
    "get_attractions": get_attractions,
    "search": general_search
}
