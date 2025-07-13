import random
import uuid
from typing import Dict, Any
from datetime import datetime
from langchain.tools import tool

from app.utils import send_group_message
from app.store import vote_option_map

@tool
# Collaborative restaurant booking function that creates a vote in the group to gather preferences.
# The group votes on location, date, time, cuisine, and number of guests before making the final booking.
def book_restaurant_vote(
    group_id: str,
    location: str = None,
    date: str = None,
    time: str = None,
    guests: int = None,
    cuisine: str = None,
) -> Dict[str, Any]:
    """Create a vote in the group to gather restaurant booking preferences."""
    
    # Validate group_id is required
    if not group_id:
        raise ValueError("Group ID is required for restaurant booking vote")
    
    group_id = str(group_id).strip()
    if not group_id:
        raise ValueError("Group ID cannot be empty")
    
    # Define voting options based on what's missing
    vote_title = "Restaurant Booking Preferences"
    vote_options = []
    
    if not location:
        vote_options.extend([
            "Location: London",
            "Location: Beijing", 
            "Location: New York",
            "Location: Other"
        ])
    
    if not date:
        vote_options.extend([
            "Date: Today",
            "Date: Tomorrow",
            "Date: This Weekend",
            "Date: Next Week"
        ])
    
    if not time:
        vote_options.extend([
            "Time: 18:00 (6 PM)",
            "Time: 19:00 (7 PM)",
            "Time: 20:00 (8 PM)",
            "Time: 21:00 (9 PM)"
        ])
    
    if not guests:
        vote_options.extend([
            "Guests: 2 people",
            "Guests: 4 people",
            "Guests: 6 people",
            "Guests: 8+ people"
        ])
    
    if not cuisine:
        vote_options.extend([
            "Cuisine: International",
            "Cuisine: Chinese",
            "Cuisine: French",
            "Cuisine: Indian"
        ])
    
    # Create the vote message
    vote_message = f"🍽️ **Restaurant Booking Vote**\n\n"
    vote_message += f"Let's decide on our restaurant booking preferences!\n\n"
    
    if location:
        vote_message += f"📍 Location: {location}\n"
    if date:
        vote_message += f"📅 Date: {date}\n"
    if time:
        vote_message += f"🕐 Time: {time}\n"
    if guests:
        vote_message += f"👥 Guests: {guests}\n"
    if cuisine:
        vote_message += f"🍴 Cuisine: {cuisine}\n"
    
    vote_message += f"\nPlease vote for your preferences:"
    
    # Create clickable buttons for voting
    button_options = []
    for option in vote_options:
        selector = f"vote:{uuid.uuid4().hex}"
        button_options.append({
            "name": option,
            "selector": selector,
            "type": "default",
            "isHidden": "1"
        })
        vote_option_map[selector] = option
    
    # Create payload with text and buttons
    payload = {
        "text": vote_message,
        "button": button_options
    }
    
    # Send the vote to the group with clickable buttons
    send_group_message(group_id, payload)
    
    return {
        "status": "vote_created",
        "message": f"✅ Restaurant booking vote created in group {group_id}",
        "group_id": group_id,
        "missing_parameters": {
            "location": location is None,
            "date": date is None,
            "time": time is None,
            "guests": guests is None,
            "cuisine": cuisine is None
        },
        "vote_options": vote_options,
        "provided_parameters": {
            "location": location,
            "date": date,
            "time": time,
            "guests": guests,
            "cuisine": cuisine
        }
    }

@tool
def get_restaurant_vote_results(group_id: str) -> Dict[str, Any]:
    """Get the current results of the restaurant booking vote."""
    
    if not group_id:
        raise ValueError("Group ID is required")
    
    # This would typically query the vote results from the database
    # For now, we'll return a mock result
    return {
        "status": "vote_results",
        "group_id": group_id,
        "results": {
            "Location: London": 5,
            "Location: Beijing": 2,
            "Location: New York": 3,
            "Date: Tomorrow": 4,
            "Date: This Weekend": 3,
            "Time: 19:00 (7 PM)": 6,
            "Time: 20:00 (8 PM)": 2,
            "Guests: 4 people": 5,
            "Guests: 6 people": 3,
            "Cuisine: French": 4,
            "Cuisine: Chinese": 2
        },
        "winning_options": {
            "location": "London",
            "date": "Tomorrow",
            "time": "19:00",
            "guests": "4 people",
            "cuisine": "French"
        }
    } 