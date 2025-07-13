import random
from typing import Dict, Any
from datetime import datetime, timedelta
from langchain.tools import tool

@tool
def book_flight(
    origin: str,
    destination: str,
    departure_date: str,
    passengers: int = 1,
    cabin_class: str = "economy",
) -> Dict[str, Any]:
    """Book a simple flight ticket with basic options."""
    
    # Validate and clean origin parameter
    if not origin:
        raise ValueError("Origin is required")
    origin = str(origin).strip()
    if not origin:
        raise ValueError("Origin cannot be empty")
    
    # Validate and clean destination parameter
    if not destination:
        raise ValueError("Destination is required")
    destination = str(destination).strip()
    if not destination:
        raise ValueError("Destination cannot be empty")
    
    # Validate passengers
    try:
        passengers = int(passengers) if passengers else 1
        if passengers < 1:
            raise ValueError("Number of passengers must be at least 1")
        if passengers > 9:
            raise ValueError("Maximum 9 passengers allowed per booking")
    except (ValueError, TypeError):
        passengers = 1
    
    # Clean cabin_class
    cabin_class = str(cabin_class).strip().lower() if cabin_class else "economy"
    if cabin_class not in ["economy", "premium", "business", "first"]:
        cabin_class = "economy"
    
    # Validate departure_date
    if not departure_date:
        raise ValueError("Departure date is required")
    
    try:
        dep_date = datetime.strptime(departure_date, "%Y-%m-%d")
        if dep_date < datetime.now():
            raise ValueError("Departure date cannot be in the past")
    except ValueError as e:
        raise ValueError(f"Invalid departure date format. Please use YYYY-MM-DD. Error: {str(e)}")
    
    # Get airline and flight details
    airline_info = _get_airline_info(origin, destination)
    flight_details = _get_flight_details(origin, destination, airline_info["airline"])
    
    # Calculate pricing
    pricing = _calculate_flight_pricing(origin, destination, cabin_class, passengers)
    
    return {
        "confirmation_id": f"FL-{random.randint(100000,999999)}",
        "airline": airline_info["airline"],
        "airline_code": airline_info["code"],
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "passengers": passengers,
        "cabin_class": cabin_class,
        "flight_details": flight_details,
        "pricing": pricing,
        "status": "confirmed"
    }

def _get_airline_info(origin: str, destination: str) -> Dict[str, str]:
    """Get airline information based on route."""
    
    # Major airline routes
    airline_routes = {
        ("Beijing", "London"): {"airline": "Air China", "code": "CA"},
        ("Beijing", "New York"): {"airline": "China Eastern", "code": "MU"},
        ("London", "Beijing"): {"airline": "British Airways", "code": "BA"},
        ("London", "New York"): {"airline": "British Airways", "code": "BA"},
        ("New York", "London"): {"airline": "American Airlines", "code": "AA"},
        ("New York", "Beijing"): {"airline": "United Airlines", "code": "UA"},
        ("Beijing", "Shanghai"): {"airline": "China Southern", "code": "CZ"},
        ("Shanghai", "Beijing"): {"airline": "China Eastern", "code": "MU"},
        ("London", "Paris"): {"airline": "Air France", "code": "AF"},
        ("Paris", "London"): {"airline": "British Airways", "code": "BA"},
        ("New York", "Los Angeles"): {"airline": "Delta Airlines", "code": "DL"},
        ("Los Angeles", "New York"): {"airline": "American Airlines", "code": "AA"},
    }
    
    # Check for exact route match
    route_key = (origin, destination)
    if route_key in airline_routes:
        return airline_routes[route_key]
    
    # Check for reverse route
    reverse_key = (destination, origin)
    if reverse_key in airline_routes:
        airline_info = airline_routes[reverse_key]
        return airline_info
    
    # Default airline based on origin
    default_airlines = {
        "Beijing": {"airline": "Air China", "code": "CA"},
        "London": {"airline": "British Airways", "code": "BA"},
        "New York": {"airline": "American Airlines", "code": "AA"},
        "Shanghai": {"airline": "China Eastern", "code": "MU"},
        "Paris": {"airline": "Air France", "code": "AF"},
        "Los Angeles": {"airline": "Delta Airlines", "code": "DL"},
    }
    
    for city in default_airlines:
        if city.lower() in origin.lower():
            return default_airlines[city]
    
    # Fallback
    return {"airline": f"{origin} Airways", "code": "XX"}

def _get_flight_details(origin: str, destination: str, airline: str) -> Dict[str, Any]:
    """Generate flight details including flight numbers, times, and aircraft."""
    
    # Generate flight number
    flight_number = f"{random.randint(100, 9999)}"
    
    # Generate departure and arrival times
    departure_hour = random.randint(6, 22)
    departure_minute = random.choice([0, 15, 30, 45])
    departure_time = f"{departure_hour:02d}:{departure_minute:02d}"
    
    # Calculate flight duration based on route
    duration_hours = _calculate_flight_duration(origin, destination)
    arrival_hour = (departure_hour + duration_hours) % 24
    arrival_minute = departure_minute
    arrival_time = f"{arrival_hour:02d}:{arrival_minute:02d}"
    
    # Aircraft types based on route distance
    aircraft_types = {
        "short": ["Boeing 737", "Airbus A320", "Boeing 757"],
        "medium": ["Boeing 787", "Airbus A330", "Boeing 767"],
        "long": ["Boeing 777", "Airbus A350", "Boeing 787"]
    }
    
    route_type = _get_route_type(origin, destination)
    aircraft = random.choice(aircraft_types[route_type])
    
    return {
        "flight_number": flight_number,
        "departure_time": departure_time,
        "arrival_time": arrival_time,
        "duration_hours": duration_hours,
        "aircraft": aircraft,
        "terminal": random.choice(["A", "B", "C", "D"]),
        "gate": f"{random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 50)}"
    }

def _calculate_flight_duration(origin: str, destination: str) -> int:
    """Calculate flight duration in hours based on route."""
    
    # Simplified distance calculation
    route_distances = {
        ("Beijing", "London"): 8,
        ("Beijing", "New York"): 13,
        ("London", "New York"): 7,
        ("Beijing", "Shanghai"): 2,
        ("London", "Paris"): 1,
        ("New York", "Los Angeles"): 5,
    }
    
    route_key = (origin, destination)
    if route_key in route_distances:
        return route_distances[route_key]
    
    # Estimate based on city keywords
    if "Beijing" in origin or "Beijing" in destination:
        return random.randint(2, 13)
    elif "London" in origin or "London" in destination:
        return random.randint(1, 8)
    elif "New York" in origin or "New York" in destination:
        return random.randint(1, 13)
    
    return random.randint(1, 6)

def _get_route_type(origin: str, destination: str) -> str:
    """Determine route type for aircraft selection."""
    
    short_routes = [
        ("Beijing", "Shanghai"),
        ("London", "Paris"),
        ("New York", "Boston"),
        ("Los Angeles", "San Francisco")
    ]
    
    long_routes = [
        ("Beijing", "London"),
        ("Beijing", "New York"),
        ("London", "New York"),
        ("New York", "Tokyo")
    ]
    
    route = (origin, destination)
    if route in short_routes:
        return "short"
    elif route in long_routes:
        return "long"
    else:
        return "medium"

def _calculate_flight_pricing(origin: str, destination: str, cabin_class: str, passengers: int) -> Dict[str, float]:
    """Calculate simple flight pricing."""
    
    # Base prices by cabin class
    base_prices = {
        "economy": 300,
        "premium": 600,
        "business": 1200,
        "first": 2000
    }
    
    base_price = base_prices.get(cabin_class, 300)
    
    # Route multipliers
    route_multipliers = {
        ("Beijing", "London"): 1.8,
        ("Beijing", "New York"): 2.0,
        ("London", "New York"): 1.5,
        ("Beijing", "Shanghai"): 0.8,
        ("London", "Paris"): 0.6,
        ("New York", "Los Angeles"): 1.2,
    }
    
    route_key = (origin, destination)
    multiplier = route_multipliers.get(route_key, 1.0)
    
    # Calculate total price
    total_price = base_price * multiplier * passengers
    
    # Add taxes
    taxes = total_price * 0.15
    final_total = total_price + taxes
    
    return {
        "base_fare": round(total_price, 2),
        "taxes": round(taxes, 2),
        "total": round(final_total, 2)
    }