# 🤖 LuffaBot AI Assistant - Mock Execution Demo

## 🎯 **Demo Overview**

This document shows realistic user interactions with the LuffaBot AI Assistant, demonstrating how the AI agent processes requests and calls appropriate tools.

---

## 🏨 **Hotel Booking Scenarios**

### **Scenario 1: Complete Hotel Booking**

**User**: "Book a hotel in London for 2 guests from 2024-01-15 to 2024-01-20"

**AI Agent Processing**:

1. ✅ **Intent Recognition**: Identifies hotel booking request
2. ✅ **Parameter Extraction**:
   - location: "London"
   - check_in: "2024-01-15"
   - check_out: "2024-01-20"
   - guests: 2
   - room_type: "standard" (default)
3. ✅ **Tool Selection**: Calls `book_hotel` tool
4. ✅ **Execution**: Processes booking simulation

**Bot Response**:

```
✅ Hotel booking confirmed!

🏨 Hotel: The Ritz
📍 Location: London
📅 Check-in: 2024-01-15
📅 Check-out: 2024-01-20
👥 Guests: 2
🛏️ Room Type: standard
🌙 Nights: 5
💰 Total Price: $1000
🆔 Confirmation ID: BK-123456
```

### **Scenario 2: Missing Parameters**

**User**: "Book a hotel in Paris"

**AI Agent Processing**:

1. ✅ **Intent Recognition**: Identifies hotel booking request
2. ❌ **Parameter Extraction**: Missing required parameters
3. ✅ **Validation**: Detects missing check_in, check_out, guests
4. ✅ **Clarification Request**: Asks for missing information

**Bot Response**:

```
Got partial info for `book_hotel`. Please provide: check_in, check_out, guests, room_type
```

### **Scenario 3: Invalid Location**

**User**: "Book a hotel in Mars for 1 guest from 2024-02-01 to 2024-02-05"

**AI Agent Processing**:

1. ✅ **Intent Recognition**: Identifies hotel booking request
2. ✅ **Parameter Extraction**: All parameters provided
3. ✅ **Tool Execution**: Calls `book_hotel` with "Mars" location
4. ✅ **Fallback Handling**: Uses generic hotel name for unknown location

**Bot Response**:

```
✅ Hotel booking confirmed!

🏨 Hotel: Mars International Hotel
📍 Location: Mars
📅 Check-in: 2024-02-01
📅 Check-out: 2024-02-05
👥 Guests: 1
🛏️ Room Type: standard
🌙 Nights: 4
💰 Total Price: $400
🆔 Confirmation ID: BK-789012
```

---

## 🍽️ **Restaurant Booking Scenarios**

### **Scenario 4: Complete Restaurant Booking**

**User**: "Book a restaurant in London for 4 guests on 2024-01-15 at 19:00 with French cuisine"

**AI Agent Processing**:

1. ✅ **Intent Recognition**: Identifies restaurant booking request
2. ✅ **Parameter Extraction**:
   - location: "London"
   - date: "2024-01-15"
   - time: "19:00"
   - guests: 4
   - cuisine: "French"
3. ✅ **Tool Selection**: Calls `book_restaurant` tool
4. ✅ **Execution**: Processes reservation simulation

**Bot Response**:

```
✅ Restaurant reservation confirmed!

🍽️ Restaurant: Sketch
📍 Location: London
📅 Date: 2024-01-15
🕐 Time: 19:00
👥 Guests: 4
🍴 Cuisine: French
💰 Estimated Total: $160
🆔 Reservation ID: RSV-456789
```

### **Scenario 5: Minimal Restaurant Booking**

**User**: "Book a restaurant in Beijing tomorrow at 18:30"

**AI Agent Processing**:

1. ✅ **Intent Recognition**: Identifies restaurant booking request
2. ✅ **Parameter Extraction**:
   - location: "Beijing"
   - date: "2024-01-16" (tomorrow)
   - time: "18:30"
   - guests: 2 (default)
   - cuisine: "international" (default)
3. ✅ **Tool Selection**: Calls `book_restaurant` tool

**Bot Response**:

```
✅ Restaurant reservation confirmed!

🍽️ Restaurant: Peking Duck House
📍 Location: Beijing
📅 Date: 2024-01-16
🕐 Time: 18:30
👥 Guests: 2
🍴 Cuisine: international
💰 Estimated Total: $60
🆔 Reservation ID: RSV-789123
```

---

## 🗳️ **Vote System Scenarios**

### **Scenario 6: Group Vote Creation**

**User**: "Start a vote in group Arz7KwQDd9m about 'which programming language is best' with options Python, JavaScript, Java"

**AI Agent Processing**:

1. ✅ **Intent Recognition**: Identifies vote creation request
2. ✅ **Parameter Extraction**:
   - group_id: "Arz7KwQDd9m"
   - title: "which programming language is best"
   - options: ["Python", "JavaScript", "Java"]
3. ✅ **Tool Selection**: Calls `initiate_vote` tool
4. ✅ **Execution**: Creates interactive vote with buttons

**Bot Response**:

```
✅ Vote initiated successfully!

📊 Title: which programming language is best
👥 Group: Arz7KwQDd9m
🗳️ Options: Python, JavaScript, Java
```

**Group Message Sent**:

```
which programming language is best

[Python] [JavaScript] [Java]
```

### **Scenario 7: Vote Result Check**

**User**: "Show me the vote results"

**AI Agent Processing**:

1. ✅ **Intent Recognition**: Identifies vote result request
2. ✅ **Tool Selection**: Calls `count_vote_result` tool
3. ✅ **Execution**: Counts votes from message queue

**Bot Response**:

```
Python: 3
JavaScript: 2
Java: 1
```

---

## 🎨 **Image Generation Scenarios**

### **Scenario 8: Image Generation**

**User**: "Generate an image of a beautiful sunset over mountains"

**AI Agent Processing**:

1. ✅ **Intent Recognition**: Identifies image generation request
2. ✅ **Parameter Extraction**:
   - prompt: "beautiful sunset over mountains"
3. ✅ **Tool Selection**: Calls `generate_image` tool
4. ✅ **Execution**: Calls external image generation API

**Bot Response**:

```
🖼️ Image generated successfully!

📸 Image URL: https://tmpfiles.org/dl/abc123/image.jpg
```

---

## ❓ **Error Handling Scenarios**

### **Scenario 9: Invalid Date Format**

**User**: "Book a hotel in Tokyo from today to next week"

**AI Agent Processing**:

1. ✅ **Intent Recognition**: Identifies hotel booking request
2. ❌ **Parameter Extraction**: Invalid date format
3. ✅ **Error Handling**: Date parsing fails
4. ✅ **Error Response**: Clear error message

**Bot Response**:

```
❌ Error executing book_hotel: Invalid date format. Please use YYYY-MM-DD format. Error: time data 'today' does not match format '%Y-%m-%d'
```

### **Scenario 10: Missing Required Parameters**

**User**: "Book a restaurant"

**AI Agent Processing**:

1. ✅ **Intent Recognition**: Identifies restaurant booking request
2. ❌ **Parameter Extraction**: Missing all required parameters
3. ✅ **Validation**: Detects missing location, date, time
4. ✅ **Clarification Request**: Asks for missing information

**Bot Response**:

```
Got partial info for `book_restaurant`. Please provide: location, date, time, guests, cuisine
```

---

## 🔄 **Conversation Flow Examples**

### **Scenario 11: Multi-turn Hotel Booking**

**User**: "I want to book a hotel"
**Bot**: "Got partial info for `book_hotel`. Please provide: location, check_in, check_out, guests, room_type"

**User**: "In London"
**Bot**: "Got partial info for `book_hotel`. Please provide: check_in, check_out, guests, room_type"

**User**: "From 2024-01-15 to 2024-01-20 for 2 guests"
**Bot**: "Got partial info for `book_hotel`. Please provide: room_type"

**User**: "Standard room"
**Bot**:

```
✅ Hotel booking confirmed!

🏨 Hotel: The Savoy
📍 Location: London
📅 Check-in: 2024-01-15
📅 Check-out: 2024-01-20
👥 Guests: 2
🛏️ Room Type: standard
🌙 Nights: 5
💰 Total Price: $1000
🆔 Confirmation ID: BK-123456
```

### **Scenario 12: Mixed Tool Usage**

**User**: "Book a hotel in New York for 3 guests from 2024-02-01 to 2024-02-05, then book a restaurant for dinner"

**AI Agent Processing**:

1. ✅ **First Request**: Processes hotel booking
2. ✅ **Hotel Response**: Returns booking confirmation
3. ✅ **Second Request**: Processes restaurant booking (needs clarification)

**Bot Response** (First):

```
✅ Hotel booking confirmed!

🏨 Hotel: Plaza Hotel
📍 Location: New York
📅 Check-in: 2024-02-01
📅 Check-out: 2024-02-05
👥 Guests: 3
🛏️ Room Type: standard
🌙 Nights: 4
💰 Total Price: $1200
🆔 Confirmation ID: BK-456789
```

**Bot Response** (Second):

```
Got partial info for `book_restaurant`. Please provide: location, date, time, guests, cuisine
```

---

## 📊 **Debug Information Examples**

### **Console Debug Output**

When a user sends: "Book a hotel in London for 2 guests from 2024-01-15 to 2024-01-20"

**Console shows**:

```
Received prompt: Book a hotel in London for 2 guests from 2024-01-15 to 2024-01-20 from user123
DEBUG: Calling book_hotel with parameters: {'location': 'London', 'check_in': '2024-01-15', 'check_out': '2024-01-20', 'guests': 2, 'room_type': 'standard'}
Sent: {"status": "success", "message": "Message sent successfully"}
```

---

## 🎯 **Key Features Demonstrated**

### **✅ Parameter Validation**

- Required parameters checking
- Type conversion and cleaning
- Default value handling
- Error message generation

### **✅ Tool Integration**

- LangChain tool decorators
- Proper `.invoke()` method usage
- Error handling and debugging
- Formatted response generation

### **✅ Multi-turn Conversations**

- Parameter collection over multiple messages
- Context preservation
- Progressive clarification

### **✅ Error Recovery**

- Graceful error handling
- Clear error messages
- Parameter validation feedback
- Fallback mechanisms

### **✅ Real-time Processing**

- 1-second polling interval
- Immediate response generation
- Background message processing
- Debug information logging

---

## 🚀 **Testing Commands**

Try these commands in your LuffaBot:

1. **Hotel Booking**: "Book a hotel in London for 2 guests from 2024-01-15 to 2024-01-20"
2. **Restaurant Booking**: "Book a restaurant in Beijing for 4 guests on 2024-01-20 at 19:00 with Chinese cuisine"
3. **Vote Creation**: "Start a vote in group Arz7KwQDd9m about 'favorite color' with options red, blue, green"
4. **Image Generation**: "Generate an image of a cute cat playing with yarn"
5. **Error Testing**: "Book a hotel" (should ask for missing parameters)

The system will process each request, validate parameters, call the appropriate tools, and return formatted responses with emojis and clear structure!
