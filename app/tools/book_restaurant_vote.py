import random
import uuid
from typing import Dict, Any
from datetime import datetime
from langchain.tools import tool

from app.utils import send_group_message
from app.store import vote_option_map, message_queue
from app.tools.book_restaurant import book_restaurant

@tool
# Collaborative restaurant booking function that creates separate votes for each category.
# Creates individual votes for location, date, time, guests, and cuisine preferences.
def book_restaurant_vote(
    group_id: str,
    location: str = None,
    date: str = None,
    time: str = None,
    guests: int = None,
    cuisine: str = None,
) -> Dict[str, Any]:
    """Create separate votes in the group for each restaurant booking category."""
    
    # Validate group_id is required
    if not group_id:
        raise ValueError("Group ID is required for restaurant booking vote")
    
    group_id = str(group_id).strip()
    if not group_id:
        raise ValueError("Group ID cannot be empty")
    
    # Track which votes were created
    created_votes = []
    
    # Create separate vote for location if missing
    if not location:
        location_vote = _create_location_vote(group_id)
        created_votes.append("location")
    
    # Create separate vote for date if missing
    if not date:
        date_vote = _create_date_vote(group_id)
        created_votes.append("date")
    
    # Create separate vote for time if missing
    if not time:
        time_vote = _create_time_vote(group_id)
        created_votes.append("time")
    
    # Create separate vote for guests if missing
    if not guests:
        guests_vote = _create_guests_vote(group_id)
        created_votes.append("guests")
    
    # Create separate vote for cuisine if missing
    if not cuisine:
        cuisine_vote = _create_cuisine_vote(group_id)
        created_votes.append("cuisine")
    
    if not created_votes:
        return {
            "status": "no_votes_needed",
            "message": f"All restaurant booking parameters are already provided for group {group_id}",
            "group_id": group_id,
            "provided_parameters": {
                "location": location,
                "date": date,
                "time": time,
                "guests": guests,
                "cuisine": cuisine
            }
        }
    
    return {
        "status": "votes_created",
        "message": f"✅ Created {len(created_votes)} restaurant booking votes in group {group_id}",
        "group_id": group_id,
        "created_votes": created_votes,
        "missing_parameters": {
            "location": location is None,
            "date": date is None,
            "time": time is None,
            "guests": guests is None,
            "cuisine": cuisine is None
        },
        "provided_parameters": {
            "location": location,
            "date": date,
            "time": time,
            "guests": guests,
            "cuisine": cuisine
        }
    }

def _create_location_vote(group_id: str) -> None:
    """Create a vote for restaurant location preference."""
    vote_message = "📍 **Restaurant Location Vote**\n\nWhere would you like to dine?\n\nPlease vote for your preferred location:"
    
    location_options = [
        "London",
        "Beijing", 
        "New York",
        "Other"
    ]
    
    button_options = []
    for option in location_options:
        selector = f"vote:{uuid.uuid4().hex}"
        button_options.append({
            "name": option,
            "selector": selector,
            "type": "default",
            "isHidden": "1"
        })
        vote_option_map[selector] = f"Location: {option}"
    
    payload = {
        "text": vote_message,
        "button": button_options
    }
    
    send_group_message(group_id, payload)

def _create_date_vote(group_id: str) -> None:
    """Create a vote for restaurant date preference."""
    vote_message = "📅 **Restaurant Date Vote**\n\nWhen would you like to dine?\n\nPlease vote for your preferred date:"
    
    date_options = [
        "Today",
        "Tomorrow",
        "This Weekend",
        "Next Week"
    ]
    
    button_options = []
    for option in date_options:
        selector = f"vote:{uuid.uuid4().hex}"
        button_options.append({
            "name": option,
            "selector": selector,
            "type": "default",
            "isHidden": "1"
        })
        vote_option_map[selector] = f"Date: {option}"
    
    payload = {
        "text": vote_message,
        "button": button_options
    }
    
    send_group_message(group_id, payload)

def _create_time_vote(group_id: str) -> None:
    """Create a vote for restaurant time preference."""
    vote_message = "🕐 **Restaurant Time Vote**\n\nWhat time would you like to dine?\n\nPlease vote for your preferred time:"
    
    time_options = [
        "18:00 (6 PM)",
        "19:00 (7 PM)",
        "20:00 (8 PM)",
        "21:00 (9 PM)"
    ]
    
    button_options = []
    for option in time_options:
        selector = f"vote:{uuid.uuid4().hex}"
        button_options.append({
            "name": option,
            "selector": selector,
            "type": "default",
            "isHidden": "1"
        })
        vote_option_map[selector] = f"Time: {option}"
    
    payload = {
        "text": vote_message,
        "button": button_options
    }
    
    send_group_message(group_id, payload)

def _create_guests_vote(group_id: str) -> None:
    """Create a vote for number of guests preference."""
    vote_message = "👥 **Number of Guests Vote**\n\nHow many people will be dining?\n\nPlease vote for the number of guests:"
    
    guests_options = [
        "2 people",
        "4 people",
        "6 people",
        "8+ people"
    ]
    
    button_options = []
    for option in guests_options:
        selector = f"vote:{uuid.uuid4().hex}"
        button_options.append({
            "name": option,
            "selector": selector,
            "type": "default",
            "isHidden": "1"
        })
        vote_option_map[selector] = f"Guests: {option}"
    
    payload = {
        "text": vote_message,
        "button": button_options
    }
    
    send_group_message(group_id, payload)

def _create_cuisine_vote(group_id: str) -> None:
    """Create a vote for cuisine preference."""
    vote_message = "🍴 **Cuisine Preference Vote**\n\nWhat type of cuisine would you prefer?\n\nPlease vote for your preferred cuisine:"
    
    cuisine_options = [
        "International",
        "Chinese",
        "French",
        "Indian"
    ]
    
    button_options = []
    for option in cuisine_options:
        selector = f"vote:{uuid.uuid4().hex}"
        button_options.append({
            "name": option,
            "selector": selector,
            "type": "default",
            "isHidden": "1"
        })
        vote_option_map[selector] = f"Cuisine: {option}"
    
    payload = {
        "text": vote_message,
        "button": button_options
    }
    
    send_group_message(group_id, payload)

@tool
def get_restaurant_vote_results(group_id: str) -> Dict[str, Any]:
    """Get the current results of the restaurant booking votes."""
    
    if not group_id:
        raise ValueError("Group ID is required")
    
    # Initialize result count dictionary for restaurant vote options
    result_count = {}
    winning_options = {}
    
    # Count votes for each restaurant vote option
    for message in message_queue:
        vote_key = message.get("message_text", "")
        if vote_key in vote_option_map:
            option = vote_option_map[vote_key]
            result_count[option] = result_count.get(option, 0) + 1
    
    # If no votes found, return empty results
    if not result_count:
        return {
            "status": "no_votes_found",
            "group_id": group_id,
            "message": f"No restaurant votes found for group {group_id}",
            "results": {},
            "winning_options": {}
        }
    
    # Determine winning options for each category
    location_votes = {k: v for k, v in result_count.items() if k.startswith("Location: ")}
    date_votes = {k: v for k, v in result_count.items() if k.startswith("Date: ")}
    time_votes = {k: v for k, v in result_count.items() if k.startswith("Time: ")}
    guests_votes = {k: v for k, v in result_count.items() if k.startswith("Guests: ")}
    cuisine_votes = {k: v for k, v in result_count.items() if k.startswith("Cuisine: ")}
    
    # Find winners for each category
    if location_votes:
        winning_location = max(location_votes.items(), key=lambda x: x[1])
        winning_options["location"] = winning_location[0].replace("Location: ", "")
    
    if date_votes:
        winning_date = max(date_votes.items(), key=lambda x: x[1])
        winning_options["date"] = winning_date[0].replace("Date: ", "")
    
    if time_votes:
        winning_time = max(time_votes.items(), key=lambda x: x[1])
        winning_options["time"] = winning_time[0].replace("Time: ", "")
    
    if guests_votes:
        winning_guests = max(guests_votes.items(), key=lambda x: x[1])
        winning_options["guests"] = winning_guests[0].replace("Guests: ", "")
    
    if cuisine_votes:
        winning_cuisine = max(cuisine_votes.items(), key=lambda x: x[1])
        winning_options["cuisine"] = winning_cuisine[0].replace("Cuisine: ", "")
    
    return {
        "status": "vote_results",
        "group_id": group_id,
        "results": result_count,
        "winning_options": winning_options
    }

@tool
def execute_restaurant_booking_with_votes(
    group_id: str,
    location: str,
    date: str,
    time: str,
    guests: int,
    cuisine: str
) -> Dict[str, Any]:
    """Execute restaurant booking with the winning vote results."""
    
    if not group_id:
        raise ValueError("Group ID is required")
    
    if not all([location, date, time, guests, cuisine]):
        raise ValueError("All booking parameters are required: location, date, time, guests, cuisine")
    
    try:
        # Convert guests to integer
        guests = int(guests)
        if guests < 1:
            raise ValueError("Number of guests must be at least 1")
    except (ValueError, TypeError):
        raise ValueError("Invalid number of guests")
    
    # Execute the actual restaurant booking
    booking_result = book_restaurant.invoke({
        "location": location,
        "date": date,
        "time": time,
        "guests": guests,
        "cuisine": cuisine
    })
    
    # Send confirmation message to the group
    confirmation_message = f"""✅ **Restaurant Booking Confirmed!**

🍽️ Restaurant: {booking_result['restaurant']}
📍 Location: {booking_result['location']}
📅 Date: {booking_result['date']}
🕐 Time: {booking_result['time']}
👥 Guests: {booking_result['guests']}
🍴 Cuisine: {booking_result['cuisine']}
💰 Estimated Total: ${booking_result['total_estimated_price']}
🆔 Reservation ID: {booking_result['reservation_id']}

🎉 Booking completed based on group votes!"""
    
    send_group_message(group_id, {"text": confirmation_message})
    
    return {
        "status": "booking_confirmed",
        "message": f"✅ Restaurant booking confirmed for group {group_id}",
        "group_id": group_id,
        "booking_details": booking_result,
        "vote_based": True
    } 