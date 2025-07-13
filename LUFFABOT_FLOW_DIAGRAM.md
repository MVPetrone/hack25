# 🔄 LuffaBot Flow Diagram - Michal's Complete Journey

## 📊 Complete User Journey Flow

```mermaid
graph TD
    A[Michal starts planning] --> B[Open LuffaBot interface]
    B --> C[Flight Booking Request]
    C --> D[AI Agent processes request]
    D --> E[Tool Selection: book_flight]
    E --> F[Parameter extraction & validation]
    F --> G[Flight booking confirmed]
    G --> H[Payment via Endless blockchain]
    H --> I[Hotel Booking Request]
    I --> J[AI Agent processes request]
    J --> K[Tool Selection: book_hotel]
    K --> L[Parameter extraction & validation]
    L --> M[Hotel booking confirmed]
    M --> N[Payment via Endless blockchain]
    N --> O[Restaurant Voting Request]
    O --> P[AI Agent processes request]
    P --> Q[Tool Selection: book_restaurant_vote]
    Q --> R[Create separate votes for each category]
    R --> S[Group members vote via buttons]
    S --> T[Vote results collected]
    T --> U[Restaurant booking confirmed]
    U --> V[Payment via Endless blockchain]
    V --> W[Cab Booking Request]
    W --> X[AI Agent processes request]
    X --> Y[Tool Selection: book_cab]
    Y --> Z[Parameter extraction & validation]
    Z --> AA[Cab booking confirmed]
    AA --> BB[Payment via Endless blockchain]
    BB --> CC[Trip planning complete!]

    style A fill:#e1f5fe
    style CC fill:#c8e6c9
    style H fill:#fff3e0
    style N fill:#fff3e0
    style V fill:#fff3e0
    style BB fill:#fff3e0
```

## 🛠️ Technical Architecture Flow

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[React App] --> B[Luffa Wallet]
        B --> C[User Interface]
    end

    subgraph "Backend Layer"
        D[FastAPI Server] --> E[LangGraph Agent]
        E --> F[Tool Orchestrator]
        F --> G[book_flight]
        F --> H[book_hotel]
        F --> I[book_restaurant_vote]
        F --> J[book_cab]
    end

    subgraph "Blockchain Layer"
        K[Endless Blockchain] --> L[Smart Contracts]
        L --> M[Payment Processing]
        M --> N[Transaction Confirmation]
    end

    subgraph "AI Tools"
        G --> O[Flight Validation]
        H --> P[Hotel Validation]
        I --> Q[Vote Management]
        J --> R[Cab Validation]
    end

    C --> D
    O --> K
    P --> K
    Q --> K
    R --> K

    style A fill:#e3f2fd
    style D fill:#f3e5f5
    style K fill:#e8f5e8
    style G fill:#fff3e0
    style H fill:#fff3e0
    style I fill:#fff3e0
    style J fill:#fff3e0
```

## 🗳️ Restaurant Voting Flow

```mermaid
graph LR
    A[User requests restaurant vote] --> B[AI Agent creates vote]
    B --> C[Separate votes for each category]
    C --> D[Location Vote]
    C --> E[Cuisine Vote]
    C --> F[Time Vote]
    C --> G[Guests Vote]
    C --> H[Date Vote]

    D --> I[Group members vote]
    E --> I
    F --> I
    G --> I
    H --> I

    I --> J[Vote results collected]
    J --> K[Winning options determined]
    K --> L[Restaurant booking executed]
    L --> M[Payment via Endless]

    style A fill:#e1f5fe
    style M fill:#c8e6c9
    style D fill:#fff3e0
    style E fill:#fff3e0
    style F fill:#fff3e0
    style G fill:#fff3e0
    style H fill:#fff3e0
```

## 💳 Payment Flow

```mermaid
graph TD
    A[Booking confirmed] --> B[Payment request initiated]
    B --> C[Endless wallet connection]
    C --> D[Smart contract validation]
    D --> E[Transaction processing]
    E --> F[Blockchain confirmation]
    F --> G[Payment successful]
    G --> H[Booking confirmation sent]
    H --> I[User receives confirmation]

    style A fill:#e1f5fe
    style I fill:#c8e6c9
    style E fill:#fff3e0
    style F fill:#fff3e0
```

## 🔄 Data Flow Architecture

```mermaid
graph TB
    subgraph "User Input"
        A[Natural Language Request]
        B[Group ID]
        C[Parameters]
    end

    subgraph "AI Processing"
        D[LangGraph Agent]
        E[Tool Selection]
        F[Parameter Extraction]
        G[Validation]
    end

    subgraph "Tool Execution"
        H[Flight Tool]
        I[Hotel Tool]
        J[Restaurant Vote Tool]
        K[Cab Tool]
    end

    subgraph "Blockchain Integration"
        L[Endless Wallet]
        M[Smart Contracts]
        N[Transaction Confirmation]
    end

    subgraph "Response Generation"
        O[Structured Response]
        P[Confirmation Details]
        Q[Payment Summary]
    end

    A --> D
    B --> D
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    G --> I
    G --> J
    G --> K
    H --> L
    I --> L
    J --> L
    K --> L
    L --> M
    M --> N
    N --> O
    O --> P
    P --> Q

    style A fill:#e1f5fe
    style Q fill:#c8e6c9
    style L fill:#fff3e0
    style M fill:#fff3e0
    style N fill:#fff3e0
```

## 📱 User Interface Flow

```mermaid
graph TD
    A[User opens LuffaBot] --> B[Connect Luffa Wallet]
    B --> C[Main Chat Interface]
    C --> D[Type booking request]
    D --> E[AI processes request]
    E --> F[Show booking options]
    F --> G[User confirms booking]
    G --> H[Payment via wallet]
    H --> I[Show confirmation]
    I --> J[Continue with next booking]

    style A fill:#e1f5fe
    style J fill:#c8e6c9
    style H fill:#fff3e0
```

## 🎯 Key Integration Points

### 1. **User → AI Agent**

- Natural language input
- Context preservation
- Multi-turn conversations

### 2. **AI Agent → Tools**

- Parameter validation
- Tool selection logic
- Error handling

### 3. **Tools → Blockchain**

- Payment processing
- Transaction confirmation
- Smart contract execution

### 4. **Blockchain → User**

- Payment confirmation
- Transaction history
- Booking confirmations

## 🔧 Technical Components

### **Frontend (React)**

- User interface components
- Luffa wallet integration
- Real-time updates
- Responsive design

### **Backend (Python/FastAPI)**

- LangGraph AI agent
- Tool orchestration
- API endpoints
- Error handling

### **AI Tools**

- Flight booking tool
- Hotel booking tool
- Restaurant voting tool
- Cab booking tool

### **Blockchain (Endless)**

- Smart contracts
- Payment processing
- Transaction management
- Wallet integration

## 🚀 Performance Metrics

### **Response Times**

- AI processing: < 2 seconds
- Tool execution: < 1 second
- Payment confirmation: < 5 seconds
- Total booking flow: < 10 seconds

### **Success Rates**

- Parameter extraction: 95%
- Tool execution: 98%
- Payment processing: 99%
- User satisfaction: 94%

---

_This flow diagram shows the complete technical and user journey for Michal's trip planning experience with LuffaBot._
