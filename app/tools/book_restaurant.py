import random
from typing import Dict, Any
from datetime import datetime
from langchain.tools import tool

@tool
# Simulated restaurant booking function for demo purposes.
# NOTE: This is a placeholder; logic such as real-time availability, menu, and validation is not implemented.
def book_restaurant(
    location: str,
    date: str,
    time: str,
    guests: int = 2,
    cuisine: str = "international",
) -> Dict[str, Any]:
    """Book a restaurant table."""
    
    # Validate and clean location parameter
    if not location:
        raise ValueError("Location is required")
    
    # Convert location to string and clean it
    location = str(location).strip()
    if not location:
        raise ValueError("Location cannot be empty")
    
    # Validate other parameters
    if not date or not time:
        raise ValueError("Date and time are required")
    
    try:
        guests = int(guests) if guests else 2
        if guests < 1:
            raise ValueError("Number of guests must be at least 1")
    except (ValueError, TypeError):
        guests = 2
    
    # Clean cuisine
    cuisine = str(cuisine).strip() if cuisine else "international"
    
    restaurants = {
        "Beijing": ["Peking Duck House", "Lotus Garden", "Dragon Palace"],
        "London": ["The Ivy", "Dishoom", "Sketch"],
        "New York": ["Le Bernardin", "Katz's Delicatessen", "Gramercy Tavern"],
    }
    
    # Get restaurant name, with fallback for unknown locations
    available_restaurants = restaurants.get(location, [f"{location} Bistro"])
    name = random.choice(available_restaurants)
    
    base = {"international": 30, "chinese": 25, "indian": 20, "french": 40}.get(cuisine, 30)
    total = base * guests
    
    return {
        "reservation_id": f"RSV-{random.randint(100000,999999)}",
        "restaurant": name,
        "location": location,
        "date": date,
        "time": time,
        "guests": guests,
        "cuisine": cuisine,
        "total_estimated_price": total,
    }