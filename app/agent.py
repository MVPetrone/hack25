from langgraph.prebuilt import create_react_agent
# from langchain.agents import load_tools, create_react_agent



from app.tools.transcript import transcribe
from app.tools.video_downloader import download_video
from app.tools.book_hotel import book_hotel
from app.tools.book_restaurant import book_restaurant
from app.tools.book_restaurant_vote import book_restaurant_vote, get_restaurant_vote_results, execute_restaurant_booking_with_votes
from app.tools.book_cab import book_cab
from app.tools.start_vote import initiate_vote, count_vote_result
from app.tools.image_generator import generate_image

from app.config import config
from app.utils import send_user_message

openai_api_key = config.OPENAI_API_KEY

tools = [download_video, transcribe, book_hotel, book_restaurant, book_restaurant_vote, get_restaurant_vote_results, execute_restaurant_booking_with_votes, book_cab, initiate_vote, count_vote_result, generate_image]

prompt = """
You are a helpful assistant. STRICTLY follow these rules:

1. TOOL CALLING RULES:
   - For group_id: ALWAYS extract and use group_id if the user provides it; if missing, ask for it.
   - For vote titles: USE THE USER'S EXACT WORDS without modification
   - NEVER shorten, rephrase or generate new titles
   - If title is missing, ASK USER - don't create one
   - For vote options: ONLY use options explicitly provided by user

2. GENERAL RULES:
   - Preserve ALL user-provided text verbatim
   - Respond in the user's language
   - Don't assume missing arguments
   - Ask for clarification when needed

Example:
User: "Start a vote in group Arz7KwQDd9m about 'which fruit is your favourite' with options apple, banana"
Correct: group_id="Arz7KwQDd9m" title="which fruit is your favourite", options=["apple", "banana"]
"""

agent = create_react_agent(
    model=config.LLM_MODEL,
    tools=tools,
    debug=False,
    prompt=prompt
)

history = [{"role": "system", "content": prompt}]

# Receives a user prompt and forwards it to the AI agent for processing.
# Handles collecting tool call arguments and constructing responses based on tool usage.
def invoke(prompt, from_uid):
    print(f"Received prompt: {prompt} from {from_uid}")

    # Format the user message and append it to the interaction history
    message = {
        "role": "user",
        "content": f"{prompt}",
    }
    history.append(message)

    query = {
        "messages": history
    }

    # Invoke the AI agent with the accumulated history
    result = agent.invoke(query)

    # Initialize variables for tracking tool usage and arguments
    tool_name = None
    collected_args = {}
    required_params = []
    tool_result = None

    # Inspect agent's returned steps for tool calls and extract arguments
    for step in result.get("messages", []):
        if hasattr(step, "tool_calls"):
            for call in step.tool_calls:
                tool_name = call.get("name")
                collected_args.update(call.get("args", {}))
                # You can define required_params based on the tool manually if needed
                if tool_name == "book_hotel":
                    required_params = ["location", "check_in", "check_out", "guests", "room_type"]
                if tool_name == "book_restaurant":
                    required_params = ["location", "date", "time", "guests", "cuisine"]
                if tool_name == "book_restaurant_vote":
                    required_params = ["group_id"]
                if tool_name == "get_restaurant_vote_results":
                    required_params = ["group_id"]
                if tool_name == "execute_restaurant_booking_with_votes":
                    required_params = ["group_id", "location", "date", "time", "guests", "cuisine"]
                if tool_name == "book_cab":
                    required_params = ["pickup_location", "destination"]
                if tool_name == "book_flight":
                    required_params = ["origin", "destination", "departure_date"]
                if tool_name == "initiate_vote":
                    required_params = ["group_id", "title", "options"]

        elif hasattr(step, "name") and step.name == "book_hotel":
            try:
                parsed = eval(step.content)
                if isinstance(parsed, dict):
                    collected_args.update(parsed)
            except Exception:
                pass

    # Construct structured response
    # Skip structured response if tool is in excluded list (e.g., image generation, counting)
    excluded_tools = {"count_vote_result", "generate_image"}
    if tool_name and tool_name not in excluded_tools:
        missing_params = [p for p in required_params if
                          p not in collected_args or not collected_args[p] or collected_args[p] == "undefined"]
        if missing_params:
            result["response"] = f"Got partial info for `{tool_name}`. Please provide: {', '.join(missing_params)}"
        else:
            # Actually call the tool and get the result
            try:
                if tool_name == "book_hotel":
                    print(f"DEBUG: Calling book_hotel with parameters: {collected_args}")
                    tool_result = book_hotel.invoke(collected_args)
                    result["response"] = f"✅ Hotel booking confirmed!\n\n🏨 Hotel: {tool_result['hotel']}\n📍 Location: {tool_result['location']}\n📅 Check-in: {tool_result['check_in']}\n📅 Check-out: {tool_result['check_out']}\n👥 Guests: {tool_result['guests']}\n🛏️ Room Type: {tool_result['room_type']}\n🌙 Nights: {tool_result['nights']}\n💰 Total Price: ${tool_result['total_price']}\n🆔 Confirmation ID: {tool_result['confirmation_id']}"
                elif tool_name == "book_restaurant":
                    print(f"DEBUG: Calling book_restaurant with parameters: {collected_args}")
                    tool_result = book_restaurant.invoke(collected_args)
                    result["response"] = f"✅ Restaurant reservation confirmed!\n\n🍽️ Restaurant: {tool_result['restaurant']}\n📍 Location: {tool_result['location']}\n📅 Date: {tool_result['date']}\n🕐 Time: {tool_result['time']}\n👥 Guests: {tool_result['guests']}\n🍴 Cuisine: {tool_result['cuisine']}\n💰 Estimated Total: ${tool_result['total_estimated_price']}\n🆔 Reservation ID: {tool_result['reservation_id']}"
                elif tool_name == "book_restaurant_vote":
                    print(f"DEBUG: Calling book_restaurant_vote with parameters: {collected_args}")
                    tool_result = book_restaurant_vote.invoke(collected_args)
                    
                    if tool_result.get("status") == "votes_created":
                        created_votes = tool_result.get("created_votes", [])
                        vote_count = len(created_votes)
                        result["response"] = f"✅ Created {vote_count} restaurant booking votes in group {tool_result['group_id']}!\n\n📊 Votes created for: {', '.join(created_votes)}\n🗳️ Group members can now vote on each category separately.\n\nOnce all votes are complete, you can check the results and make the final booking."
                    elif tool_result.get("status") == "no_votes_needed":
                        result["response"] = f"✅ All restaurant booking parameters are already provided for group {tool_result['group_id']}!\n\nYou can proceed directly to booking with the provided parameters."
                    else:
                        result["response"] = f"✅ Restaurant booking vote created!\n\n🍽️ Group: {tool_result['group_id']}\n📊 Status: Gathering preferences\n\nThe group will vote on the missing preferences, then you can use the final booking once all votes are collected."
                elif tool_name == "get_restaurant_vote_results":
                    print(f"DEBUG: Calling get_restaurant_vote_results with parameters: {collected_args}")
                    tool_result = get_restaurant_vote_results.invoke(collected_args)
                    
                    if tool_result.get("status") == "no_votes_found":
                        result["response"] = f"📊 **Restaurant Vote Results**\n\n{tool_result.get('message', 'No votes found')}"
                    else:
                        # Format the vote results
                        results_text = "📊 **Restaurant Vote Results**\n\n"
                        for option, votes in tool_result.get('results', {}).items():
                            results_text += f"• {option}: {votes} votes\n"
                        
                        results_text += f"\n🏆 **Winning Options:**\n"
                        winning_options = tool_result.get('winning_options', {})
                        for param, value in winning_options.items():
                            results_text += f"• {param.title()}: {value}\n"
                        
                        result["response"] = results_text
                elif tool_name == "execute_restaurant_booking_with_votes":
                    print(f"DEBUG: Calling execute_restaurant_booking_with_votes with parameters: {collected_args}")
                    tool_result = execute_restaurant_booking_with_votes.invoke(collected_args)
                    
                    if tool_result.get("status") == "booking_confirmed":
                        booking_details = tool_result.get("booking_details", {})
                        result["response"] = f"✅ Restaurant booking confirmed based on group votes!\n\n🍽️ Restaurant: {booking_details['restaurant']}\n📍 Location: {booking_details['location']}\n📅 Date: {booking_details['date']}\n🕐 Time: {booking_details['time']}\n👥 Guests: {booking_details['guests']}\n🍴 Cuisine: {booking_details['cuisine']}\n💰 Estimated Total: ${booking_details['total_estimated_price']}\n🆔 Reservation ID: {booking_details['reservation_id']}\n\n🎉 Booking completed based on group votes!"
                    else:
                        result["response"] = f"✅ Restaurant booking executed for group {tool_result.get('group_id', 'unknown')}"
                elif tool_name == "book_flight":
                    print(f"DEBUG: Calling book_flight with parameters: {collected_args}")
                    tool_result = book_flight.invoke(collected_args)
                    
                    flight_details = tool_result.get('flight_details', {})
                    pricing = tool_result.get('pricing', {})
                    meal_details = tool_result.get('meal_details', {})
                    baggage_allowance = tool_result.get('baggage_allowance', {})
                    
                    result["response"] = f"✅ Flight booking confirmed!\n\n✈️ Airline: {tool_result['airline']} ({tool_result['airline_code']})\n🛫 Origin: {tool_result['origin']}\n🛬 Destination: {tool_result['destination']}\n📅 Departure: {tool_result['departure_date']} at {flight_details.get('departure_time', 'N/A')}\n📅 Return: {tool_result.get('return_date', 'N/A')}\n👥 Passengers: {tool_result['passengers']}\n💺 Cabin Class: {tool_result['cabin_class'].title()}\n🎫 Trip Type: {tool_result['trip_type']}\n\n🛩️ Flight Details:\n• Flight Number: {flight_details.get('flight_number', 'N/A')}\n• Aircraft: {flight_details.get('aircraft', 'N/A')}\n• Duration: {flight_details.get('duration_hours', 'N/A')} hours\n• Terminal: {flight_details.get('terminal', 'N/A')}\n• Gate: {flight_details.get('gate', 'N/A')}\n\n💺 Seat Assignments: {', '.join(tool_result.get('seat_assignments', []))}\n\n🍽️ Meal: {meal_details.get('type', 'N/A')} - {meal_details.get('description', 'N/A')}\n\n🧳 Baggage: {baggage_allowance.get('type', 'N/A')} - {baggage_allowance.get('allowance', {}).get(baggage_allowance.get('type', '').lower(), 'N/A')}\n\n💰 Pricing:\n• Base Fare: ${pricing.get('base_fare', 0):.2f}\n• Meal Cost: ${pricing.get('meal_cost', 0):.2f}\n• Baggage Cost: ${pricing.get('baggage_cost', 0):.2f}\n• Taxes: ${pricing.get('taxes', 0):.2f}\n• Total: ${pricing.get('total', 0):.2f}\n\n🆔 Confirmation ID: {tool_result['confirmation_id']}"
                elif tool_name == "book_cab":
                    print(f"DEBUG: Calling book_cab with parameters: {collected_args}")
                    tool_result = book_cab.invoke(collected_args)
                    result["response"] = f"✅ Cab booking confirmed!\n\n🚕 Company: {tool_result['company']}\n👨‍💼 Driver: {tool_result['driver_name']} (⭐ {tool_result['driver_rating']})\n🚗 Vehicle: {tool_result['vehicle_info']['model']} ({tool_result['vehicle_info']['color']}, {tool_result['vehicle_info']['year']})\n📍 Pickup: {tool_result['pickup_location']}\n🎯 Destination: {tool_result['destination']}\n📅 Date: {tool_result['date']}\n🕐 Time: {tool_result['time']}\n👥 Passengers: {tool_result['passengers']}\n🚙 Cab Type: {tool_result['cab_type'].title()}\n📏 Distance: {tool_result['distance_km']} km\n⏱️ Duration: ~{tool_result['estimated_duration_minutes']} minutes\n💰 Base Fare: ${tool_result['base_fare']}\n💳 Booking Fee: ${tool_result['booking_fee']}\n💵 Total Fare: ${tool_result['total_fare']}\n💳 Payment: {tool_result['payment_method'].title()}\n🆔 Booking ID: {tool_result['booking_id']}"
                elif tool_name == "initiate_vote":
                    tool_result = initiate_vote.invoke(collected_args)
                    result["response"] = f"✅ Vote initiated successfully!\n\n📊 Title: {collected_args['title']}\n👥 Group: {collected_args['group_id']}\n🗳️ Options: {', '.join(collected_args['options'])}"
                elif tool_name == "download_video":
                    tool_result = download_video.invoke(collected_args)
                    result["response"] = f"📹 Video download initiated for: {collected_args.get('video_url', 'unknown URL')}"
                elif tool_name == "transcribe":
                    tool_result = transcribe.invoke(collected_args)
                    result["response"] = f"📝 Transcription completed for: {collected_args.get('video_url', 'unknown URL')}"
                else:
                    result["response"] = f"All parameters collected for `{tool_name}`: {collected_args}"
            except Exception as e:
                print(f"DEBUG: Error in {tool_name}: {str(e)}")
                print(f"DEBUG: Parameters passed: {collected_args}")
                result["response"] = f"❌ Error executing {tool_name}: {str(e)}"
    else:
        result["response"] = result.get("messages", [])[-1].content if result.get("messages") else ""

    history.append({"role": "assistant", "content": result["response"]})

    # Send the final response back to the user via bot message
    send_user_message(from_uid, result["response"])

    return result
