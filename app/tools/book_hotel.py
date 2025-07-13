import random
from typing import Dict, Any
from datetime import datetime
from langchain.tools import tool

@tool
 # Simulated hotel booking function for demo purposes.
 # NOTE: This is a placeholder; logic such as real-time availability, pricing, and validation is not implemented.
def book_hotel(
    location: str,
    check_in: str,
    check_out: str,
    guests: int = 1,
    room_type: str = "standard",
) -> Dict[str, Any]:
    """booking a hotel room."""
    
    # Validate and clean location parameter
    if not location:
        raise ValueError("Location is required")
    
    # Convert location to string and clean it
    location = str(location).strip()
    if not location:
        raise ValueError("Location cannot be empty")
    
    # Validate other parameters
    if not check_in or not check_out:
        raise ValueError("Check-in and check-out dates are required")
    
    try:
        guests = int(guests) if guests else 1
        if guests < 1:
            raise ValueError("Number of guests must be at least 1")
    except (ValueError, TypeError):
        guests = 1
    
    # Clean room_type
    room_type = str(room_type).strip() if room_type else "standard"
    
    hotels = {
        "Beijing": ["Beijing Grand Hotel", "Great Wall Inn", "Forbidden City Hotel"],
        "London": ["The Savoy", "The Ritz", "Park Plaza"],
        "New York": ["Plaza Hotel", "The Langham", "Times Square Inn"],
    }
    
    # Get hotel name, with fallback for unknown locations
    available_hotels = hotels.get(location, [f"{location} International Hotel"])
    name = random.choice(available_hotels)
    
    try:
        nights = (datetime.strptime(check_out, "%Y-%m-%d") -
                  datetime.strptime(check_in, "%Y-%m-%d")).days
        if nights < 1:
            raise ValueError("Check-out date must be after check-in date")
    except ValueError as e:
        raise ValueError(f"Invalid date format. Please use YYYY-MM-DD format. Error: {str(e)}")
    
    base = {"standard":100, "deluxe":180, "suite":300}.get(room_type, 120)
    total = base * nights * guests
    
    return {
        "confirmation_id": f"BK-{random.randint(100000,999999)}",
        "hotel": name,
        "location": location,
        "check_in": check_in,
        "check_out": check_out,
        "guests": guests,
        "room_type": room_type,
        "nights": nights,
        "total_price": total,
    }