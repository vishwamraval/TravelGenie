def rent_car(pickup_location, dropoff_location, pickup_date, dropoff_date, car_type):
    """
    Function to simulate a car rental service.
    
    Args:
    pickup_location (str): The location where the car will be picked up.
    dropoff_location (str): The location where the car will be dropped off.
    pickup_date (str): The date when the car will be picked up.
    dropoff_date (str): The date when the car will be dropped off.
    car_type (str): The type of car to be rented.

    Returns:
    str: Confirmation message with rental details.
    """
    return f"Car of type {car_type} has been successfully rented from {pickup_location} to {dropoff_location} from {pickup_date} to {dropoff_date}."
