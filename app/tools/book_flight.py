import random
from typing import Dict, Any
from datetime import datetime
from langchain.tools import tool

@tool
# Simulated flight booking function for demo purposes.
# NOTE: This is a placeholder; logic such as real-time availability, pricing, and validation is not implemented.
def book_flight(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str = None,
    passengers: int = 1,
    cabin_class: str = "economy",
) -> Dict[str, Any]:
    """Book a flight ticket."""
    # Validate and clean parameters
    if not origin or not destination:
        raise ValueError("Origin and destination are required")
    origin = str(origin).strip()
    destination = str(destination).strip()
    if not origin or not destination:
        raise ValueError("Origin and destination cannot be empty")
    if not departure_date:
        raise ValueError("Departure date is required")
    try:
        passengers = int(passengers) if passengers else 1
        if passengers < 1:
            raise ValueError("Number of passengers must be at least 1")
    except (ValueError, TypeError):
        passengers = 1
    cabin_class = str(cabin_class).strip() if cabin_class else "economy"

    # Simulated airlines and pricing
    airlines = {
        ("Beijing", "London"): ["Air China", "British Airways", "China Southern"],
        ("New York", "London"): ["British Airways", "American Airlines", "Virgin Atlantic"],
        ("London", "New York"): ["Delta", "United", "British Airways"],
    }
    available_airlines = airlines.get((origin, destination), [f"{origin}-{destination} Airways"])
    airline = random.choice(available_airlines)

    try:
        dep_date = datetime.strptime(departure_date, "%Y-%m-%d")
        if return_date:
            ret_date = datetime.strptime(return_date, "%Y-%m-%d")
            if ret_date <= dep_date:
                raise ValueError("Return date must be after departure date")
            trip_type = "Round-trip"
            days = (ret_date - dep_date).days
        else:
            trip_type = "One-way"
            days = 1
    except ValueError as e:
        raise ValueError(f"Invalid date format. Please use YYYY-MM-DD. Error: {str(e)}")

    base_prices = {"economy": 300, "premium": 600, "business": 1200, "first": 2000}
    base = base_prices.get(cabin_class.lower(), 350)
    total = base * passengers * (2 if trip_type == "Round-trip" else 1)

    return {
        "confirmation_id": f"FL-{random.randint(100000,999999)}",
        "airline": airline,
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "return_date": return_date,
        "passengers": passengers,
        "cabin_class": cabin_class,
        "trip_type": trip_type,
        "total_price": total,
        "days": days,
    }