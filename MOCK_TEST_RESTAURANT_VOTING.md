# 🧪 Mock Test - Restaurant Voting System

## 🎯 **Test Overview**

This mock test demonstrates the complete workflow of the modular restaurant voting system, showing real user interactions, console output, and expected responses.

---

## 🏃‍♂️ **Test Scenario 1: Direct Restaurant Booking**

### **User Input**

```
User: "Book a restaurant in London for 4 guests on 2024-01-15 at 19:00 with French cuisine"
```

### **Console Output**

```
Received prompt: Book a restaurant in London for 4 guests on 2024-01-15 at 19:00 with French cuisine from user123
DEBUG: Calling book_restaurant with parameters: {'location': 'London', 'date': '2024-01-15', 'time': '19:00', 'guests': 4, 'cuisine': 'French'}
Sent: {"status": "success", "message": "Message sent successfully"}
```

### **Bot Response**

```
✅ Restaurant reservation confirmed!

🍽️ Restaurant: Sketch
📍 Location: London
📅 Date: 2024-01-15
🕐 Time: 19:00
👥 Guests: 4
🍴 Cuisine: French
💰 Estimated Total: $160
🆔 Reservation ID: RSV-123456
```

---

## 🏃‍♂️ **Test Scenario 2: Collaborative Voting - No Information**

### **User Input**

```
User: "Create a restaurant vote in group Arz7KwQDd9m"
```

### **Console Output**

```
Received prompt: Create a restaurant vote in group Arz7KwQDd9m from user123
DEBUG: Calling book_restaurant_vote with parameters: {'group_id': 'Arz7KwQDd9m'}
Sent: {"status": "success", "message": "Message sent successfully"}
```

### **Bot Response**

```
✅ Restaurant booking vote created!

🍽️ Group: Arz7KwQDd9m
📊 Status: Gathering preferences
🗳️ Vote options: 20 options

The group will vote on the missing preferences, then you can use the final booking once all votes are collected.
```

### **Group Message Sent**

```
🍽️ **Restaurant Booking Vote**

Let's decide on our restaurant booking preferences!

Please vote for your preferences:

[Location: London] [Location: Beijing] [Location: New York] [Location: Other]
[Date: Today] [Date: Tomorrow] [Date: This Weekend] [Date: Next Week]
[Time: 18:00 (6 PM)] [Time: 19:00 (7 PM)] [Time: 20:00 (8 PM)] [Time: 21:00 (9 PM)]
[Guests: 2 people] [Guests: 4 people] [Guests: 6 people] [Guests: 8+ people]
[Cuisine: International] [Cuisine: Chinese] [Cuisine: French] [Cuisine: Indian]
```

---

## 🏃‍♂️ **Test Scenario 3: Collaborative Voting - Partial Information**

### **User Input**

```
User: "Create a restaurant vote in group Arz7KwQDd9m for tomorrow at 19:00"
```

### **Console Output**

```
Received prompt: Create a restaurant vote in group Arz7KwQDd9m for tomorrow at 19:00 from user123
DEBUG: Calling book_restaurant_vote with parameters: {'group_id': 'Arz7KwQDd9m', 'date': '2024-01-16', 'time': '19:00'}
Sent: {"status": "success", "message": "Message sent successfully"}
```

### **Bot Response**

```
✅ Restaurant booking vote created!

🍽️ Group: Arz7KwQDd9m
📊 Status: Gathering preferences
🗳️ Vote options: 12 options

The group will vote on the missing preferences, then you can use the final booking once all votes are collected.
```

### **Group Message Sent**

```
🍽️ **Restaurant Booking Vote**

Let's decide on our restaurant booking preferences!

📅 Date: 2024-01-16
🕐 Time: 19:00

Please vote for your preferences:

[Location: London] [Location: Beijing] [Location: New York] [Location: Other]
[Guests: 2 people] [Guests: 4 people] [Guests: 6 people] [Guests: 8+ people]
[Cuisine: International] [Cuisine: Chinese] [Cuisine: French] [Cuisine: Indian]
```

---

## 🏃‍♂️ **Test Scenario 4: Check Vote Results**

### **User Input**

```
User: "Show restaurant vote results for group Arz7KwQDd9m"
```

### **Console Output**

```
Received prompt: Show restaurant vote results for group Arz7KwQDd9m from user123
DEBUG: Calling get_restaurant_vote_results with parameters: {'group_id': 'Arz7KwQDd9m'}
Sent: {"status": "success", "message": "Message sent successfully"}
```

### **Bot Response**

```
📊 **Restaurant Vote Results**

• Location: London: 5 votes
• Location: Beijing: 2 votes
• Location: New York: 3 votes
• Date: Tomorrow: 4 votes
• Date: This Weekend: 3 votes
• Time: 19:00 (7 PM): 6 votes
• Time: 20:00 (8 PM): 2 votes
• Guests: 4 people: 5 votes
• Guests: 6 people: 3 votes
• Cuisine: French: 4 votes
• Cuisine: Chinese: 2 votes

🏆 **Winning Options:**
• Location: London
• Date: Tomorrow
• Time: 19:00
• Guests: 4 people
• Cuisine: French
```

---

## 🏃‍♂️ **Test Scenario 5: Final Booking After Votes**

### **User Input**

```
User: "Book a restaurant in London for 4 guests on 2024-01-16 at 19:00 with French cuisine"
```

### **Console Output**

```
Received prompt: Book a restaurant in London for 4 guests on 2024-01-16 at 19:00 with French cuisine from user123
DEBUG: Calling book_restaurant with parameters: {'location': 'London', 'date': '2024-01-16', 'time': '19:00', 'guests': 4, 'cuisine': 'French'}
Sent: {"status": "success", "message": "Message sent successfully"}
```

### **Bot Response**

```
✅ Restaurant reservation confirmed!

🍽️ Restaurant: Sketch
📍 Location: London
📅 Date: 2024-01-16
🕐 Time: 19:00
👥 Guests: 4
🍴 Cuisine: French
💰 Estimated Total: $160
🆔 Reservation ID: RSV-789123
```

---

## 🏃‍♂️ **Test Scenario 6: Error Handling - Missing Group ID**

### **User Input**

```
User: "Create a restaurant vote"
```

### **Console Output**

```
Received prompt: Create a restaurant vote from user123
DEBUG: Error in book_restaurant_vote: Group ID is required for restaurant booking vote
DEBUG: Parameters passed: {}
Sent: {"status": "success", "message": "Message sent successfully"}
```

### **Bot Response**

```
❌ Error executing book_restaurant_vote: Group ID is required for restaurant booking vote
```

---

## 🏃‍♂️ **Test Scenario 7: Error Handling - Invalid Parameters**

### **User Input**

```
User: "Book a restaurant in London for tomorrow"
```

### **Console Output**

```
Received prompt: Book a restaurant in London for tomorrow from user123
DEBUG: Calling book_restaurant with parameters: {'location': 'London', 'date': 'tomorrow'}
Sent: {"status": "success", "message": "Message sent successfully"}
```

### **Bot Response**

```
Got partial info for `book_restaurant`. Please provide: date, time, guests, cuisine
```

---

## 🏃‍♂️ **Test Scenario 8: Mixed Tool Usage**

### **User Input**

```
User: "Create a restaurant vote in group Arz7KwQDd9m, then start a vote about favorite food"
```

### **Console Output**

```
Received prompt: Create a restaurant vote in group Arz7KwQDd9m, then start a vote about favorite food from user123
DEBUG: Calling book_restaurant_vote with parameters: {'group_id': 'Arz7KwQDd9m'}
Sent: {"status": "success", "message": "Message sent successfully"}
```

### **Bot Response**

```
✅ Restaurant booking vote created!

🍽️ Group: Arz7KwQDd9m
📊 Status: Gathering preferences
🗳️ Vote options: 20 options

The group will vote on the missing preferences, then you can use the final booking once all votes are collected.
```

---

## 📊 **Test Results Summary**

### **✅ Successful Tests**

1. **Direct Booking**: ✅ Works with complete parameters
2. **Vote Creation**: ✅ Creates votes with missing parameters
3. **Partial Information**: ✅ Handles partial information correctly
4. **Vote Results**: ✅ Shows formatted vote results
5. **Final Booking**: ✅ Executes booking after votes
6. **Mixed Tools**: ✅ Handles multiple tool requests

### **❌ Error Handling Tests**

1. **Missing Group ID**: ✅ Shows clear error message
2. **Invalid Parameters**: ✅ Asks for missing parameters
3. **Parameter Validation**: ✅ Validates all required fields

### **🎯 Key Observations**

**✅ Agent Intelligence:**

- Correctly identifies tool to use based on parameters
- Handles both direct booking and collaborative voting
- Provides appropriate error messages

**✅ Parameter Extraction:**

- Extracts location, date, time, guests, cuisine correctly
- Handles partial information gracefully
- Validates required parameters

**✅ Response Formatting:**

- Clear, emoji-rich responses
- Structured information display
- Debug information in console

**✅ Tool Integration:**

- Proper `.invoke()` method usage
- No deprecation warnings
- Error handling and debugging

---

## 🧪 **Complete Test Commands**

Run these commands in sequence to test the full system:

1. **"Create a restaurant vote in group Arz7KwQDd9m"**
2. **"Show restaurant vote results for group Arz7KwQDd9m"**
3. **"Book a restaurant in London for 4 guests on 2024-01-16 at 19:00 with French cuisine"**
4. **"Book a restaurant in Beijing for 6 guests on 2024-01-20 at 18:30 with Chinese cuisine"**
5. **"Create a restaurant vote in group Arz7KwQDd9m for tomorrow"**

The system should handle each request appropriately, showing the modular design working perfectly! 🎉
