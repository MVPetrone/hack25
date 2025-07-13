# 🍽️ Modular Restaurant Voting System - Demo

## 🎯 **New Architecture Overview**

The restaurant booking system is now modular with separate files:

- **`book_restaurant.py`** - Direct restaurant bookings
- **`book_restaurant_vote.py`** - Collaborative voting system
- **`agent.py`** - Orchestrates both approaches

---

## 🔄 **How It Works**

### **Option 1: Direct Booking** (Original)

**User**: "Book a restaurant in London for 4 guests on 2024-01-15 at 19:00 with French cuisine"

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
🆔 Reservation ID: RSV-123456
```

### **Option 2: Collaborative Voting** (New)

**User**: "Create a restaurant vote in group Arz7KwQDd9m"

**Bot Response**:

```
✅ Restaurant booking vote created!

🍽️ Group: Arz7KwQDd9m
📊 Status: Gathering preferences
🗳️ Vote options: 20 options

The group will vote on the missing preferences, then you can use the final booking once all votes are collected.
```

**Group Message Sent**:

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

## 🎯 **Different Scenarios**

### **Scenario 1: Partial Information Vote**

**User**: "Create a restaurant vote in group Arz7KwQDd9m for tomorrow at 19:00"

**Bot Response**:

```
✅ Restaurant booking vote created!

🍽️ Group: Arz7KwQDd9m
📊 Status: Gathering preferences
🗳️ Vote options: 12 options

The group will vote on the missing preferences, then you can use the final booking once all votes are collected.
```

**Group Message**:

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

### **Scenario 2: Check Vote Results**

**User**: "Show restaurant vote results for group Arz7KwQDd9m"

**Bot Response**:

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

### **Scenario 3: Final Booking After Votes**

**User**: "Book a restaurant in London for 4 guests on 2024-01-16 at 19:00 with French cuisine"

**Bot Response**:

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

## 🛠️ **Technical Architecture**

### **File Structure**

```
app/tools/
├── book_restaurant.py          # Direct booking tool
├── book_restaurant_vote.py     # Collaborative voting tools
├── start_vote.py              # General voting tool
└── ...
```

### **Tools Available**

1. **`book_restaurant`** - Direct restaurant booking
2. **`book_restaurant_vote`** - Create restaurant preference vote
3. **`get_restaurant_vote_results`** - Get vote results
4. **`initiate_vote`** - General voting tool
5. **`count_vote_result`** - Count general vote results

### **Agent Logic**

- **Direct booking**: When all parameters provided → Use `book_restaurant`
- **Collaborative voting**: When group_id provided but missing parameters → Use `book_restaurant_vote`
- **Vote results**: When checking results → Use `get_restaurant_vote_results`

---

## 🎯 **Key Benefits**

### **✅ Modular Design**

- **Separate concerns**: Direct booking vs collaborative voting
- **Easy maintenance**: Each file has a single responsibility
- **Extensible**: Easy to add new voting features
- **Testable**: Each component can be tested independently

### **✅ Flexible Usage**

- **Direct booking**: Quick reservations with all details
- **Collaborative voting**: Group decision-making
- **Hybrid approach**: Start with vote, finish with direct booking

### **✅ Clear Separation**

- **`book_restaurant.py`**: Simple, direct bookings
- **`book_restaurant_vote.py`**: Complex, collaborative voting
- **Agent**: Orchestrates both approaches intelligently

---

## 🧪 **Testing Commands**

### **Direct Booking**

1. **"Book a restaurant in London for 4 guests on 2024-01-15 at 19:00 with French cuisine"**

### **Collaborative Voting**

2. **"Create a restaurant vote in group Arz7KwQDd9m"**
3. **"Create a restaurant vote in group Arz7KwQDd9m for tomorrow"**
4. **"Show restaurant vote results for group Arz7KwQDd9m"**

### **General Voting**

5. **"Start a vote in group Arz7KwQDd9m about 'favorite food' with options pizza, sushi, burger"**
6. **"Show me the vote results"**

---

## 🔄 **Workflow Examples**

### **Workflow 1: Direct Booking**

```
User: "Book a restaurant in Beijing for 6 guests on 2024-01-20 at 18:30 with Chinese cuisine"
Bot: ✅ Restaurant reservation confirmed! [Full booking details]
```

### **Workflow 2: Collaborative Voting**

```
User: "Create a restaurant vote in group Arz7KwQDd9m"
Bot: ✅ Restaurant booking vote created! [Creates vote in group]
Group: [Votes on preferences]
User: "Show restaurant vote results for group Arz7KwQDd9m"
Bot: 📊 Restaurant Vote Results [Shows vote results]
User: "Book a restaurant in London for 4 guests on 2024-01-16 at 19:00 with French cuisine"
Bot: ✅ Restaurant reservation confirmed! [Final booking]
```

### **Workflow 3: Hybrid Approach**

```
User: "Create a restaurant vote in group Arz7KwQDd9m for tomorrow"
Bot: ✅ Restaurant booking vote created! [Creates vote with partial info]
Group: [Votes on remaining preferences]
User: "Book a restaurant in London for 4 guests on 2024-01-16 at 19:00 with French cuisine"
Bot: ✅ Restaurant reservation confirmed! [Final booking]
```

---

## 🎉 **Benefits of Modular Design**

1. **🎯 Clear Separation**: Each file has a specific purpose
2. **🔧 Easy Maintenance**: Changes to voting don't affect direct booking
3. **📈 Scalability**: Easy to add new voting features
4. **🧪 Testability**: Each component can be tested independently
5. **🔄 Flexibility**: Users can choose direct or collaborative approach
6. **📊 Transparency**: Clear vote results and decision-making process

This modular approach makes the system much more maintainable and provides users with both quick direct booking and collaborative group decision-making options! 🚀
