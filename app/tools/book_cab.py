import random
from typing import Dict, Any
from datetime import datetime
from langchain.tools import tool

@tool
# Simulated cab booking function for demo purposes.
# NOTE: This is a placeholder; logic such as real-time availability, driver assignment, and validation is not implemented.
def book_cab(
    pickup_location: str,
    destination: str,
    date: str = None,
    time: str = None,
    passengers: int = 1,
    cab_type: str = "standard",
    payment_method: str = "card",
) -> Dict[str, Any]:
    """Book a cab/ride service."""
    
    # Validate and clean pickup_location parameter
    if not pickup_location:
        raise ValueError("Pickup location is required")
    
    # Convert pickup_location to string and clean it
    pickup_location = str(pickup_location).strip()
    if not pickup_location:
        raise ValueError("Pickup location cannot be empty")
    
    # Validate destination parameter
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
        if passengers > 6:
            raise ValueError("Maximum 6 passengers allowed per cab")
    except (ValueError, TypeError):
        passengers = 1
    
    # Clean cab_type
    cab_type = str(cab_type).strip().lower() if cab_type else "standard"
    if cab_type not in ["standard", "premium", "luxury", "van", "bike"]:
        cab_type = "standard"
    
    # Clean payment_method
    payment_method = str(payment_method).strip().lower() if payment_method else "card"
    if payment_method not in ["card", "cash", "digital_wallet"]:
        payment_method = "card"
    
    # Set default date and time if not provided
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    if not time:
        time = datetime.now().strftime("%H:%M")
    
    # Calculate estimated distance and fare
    distance_km = _calculate_distance(pickup_location, destination)
    
    # Base fare calculation based on cab type
    base_fares = {
        "standard": 2.5,  # $2.5 per km
        "premium": 4.0,   # $4.0 per km
        "luxury": 6.0,    # $6.0 per km
        "van": 3.5,       # $3.5 per km (for groups)
        "bike": 1.5       # $1.5 per km (motorcycle)
    }
    
    base_fare = base_fares.get(cab_type, 2.5)
    estimated_fare = base_fare * distance_km
    
    # Add booking fee
    booking_fee = 2.0
    total_fare = estimated_fare + booking_fee
    
    # Get cab company based on location
    cab_companies = {
        "Beijing": ["Beijing Taxi Co.", "Didi Chuxing", "Beijing Express"],
        "London": ["London Black Cabs", "Uber London", "Addison Lee"],
        "New York": ["Yellow Cab NYC", "Uber NYC", "Lyft NYC"],
        "default": ["City Taxi", "Express Cab", "Metro Ride"]
    }
    
    # Determine company based on pickup location
    company_location = "default"
    for city in cab_companies.keys():
        if city.lower() in pickup_location.lower():
            company_location = city
            break
    
    available_companies = cab_companies.get(company_location, cab_companies["default"])
    company_name = random.choice(available_companies)
    
    # Generate driver info
    driver_names = [
        "John Smith", "Maria Garcia", "Ahmed Hassan", "Li Wei", 
        "Sarah Johnson", "Carlos Rodriguez", "Priya Patel", "David Kim"
    ]
    driver_name = random.choice(driver_names)
    driver_rating = round(random.uniform(4.2, 5.0), 1)
    
    # Generate vehicle info
    vehicle_info = _get_vehicle_info(cab_type)
    
    # Calculate estimated duration
    estimated_duration_minutes = int(distance_km * 2.5)  # Rough estimate: 2.5 min per km
    
    return {
        "booking_id": f"CAB-{random.randint(100000,999999)}",
        "company": company_name,
        "driver_name": driver_name,
        "driver_rating": driver_rating,
        "vehicle_info": vehicle_info,
        "pickup_location": pickup_location,
        "destination": destination,
        "date": date,
        "time": time,
        "passengers": passengers,
        "cab_type": cab_type,
        "distance_km": round(distance_km, 1),
        "estimated_duration_minutes": estimated_duration_minutes,
        "base_fare": round(estimated_fare, 2),
        "booking_fee": booking_fee,
        "total_fare": round(total_fare, 2),
        "payment_method": payment_method,
        "status": "confirmed"
    }

def _calculate_distance(pickup: str, destination: str) -> float:
    """Calculate estimated distance between pickup and destination."""
    # This is a simplified distance calculation
    # In a real system, this would use actual mapping APIs
    
    # Base distance for same city
    base_distance = random.uniform(3.0, 25.0)
    
    # Adjust based on location keywords
    if "airport" in pickup.lower() or "airport" in destination.lower():
        base_distance = random.uniform(15.0, 45.0)
    elif "downtown" in pickup.lower() or "downtown" in destination.lower():
        base_distance = random.uniform(5.0, 20.0)
    elif "suburb" in pickup.lower() or "suburb" in destination.lower():
        base_distance = random.uniform(10.0, 35.0)
    
    return base_distance

def _get_vehicle_info(cab_type: str) -> Dict[str, str]:
    """Get vehicle information based on cab type."""
    vehicle_info = {
        "standard": {
            "model": "Toyota Camry",
            "color": "White",
            "year": "2022",
            "plate_number": f"T{random.randint(1000,9999)}"
        },
        "premium": {
            "model": "Mercedes E-Class",
            "color": "Black",
            "year": "2023",
            "plate_number": f"P{random.randint(1000,9999)}"
        },
        "luxury": {
            "model": "BMW 7 Series",
            "color": "Silver",
            "year": "2023",
            "plate_number": f"L{random.randint(1000,9999)}"
        },
        "van": {
            "model": "Toyota Sienna",
            "color": "Blue",
            "year": "2022",
            "plate_number": f"V{random.randint(1000,9999)}"
        },
        "bike": {
            "model": "Honda CB150R",
            "color": "Red",
            "year": "2023",
            "plate_number": f"B{random.randint(1000,9999)}"
        }
    }
    
    return vehicle_info.get(cab_type, vehicle_info["standard"]) 