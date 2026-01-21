# Agentic Travel Chatbot - Backend (Phase 1)

This is the backend service for the Agentic RAG-Powered Travel Planning Chatbot.
Phase 1 focuses on a simple conversational loop to collect trip details and generate a placeholder itinerary.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI Entry Point
│   ├── models.py               # Pydantic Data Models
│   ├── conversation_manager.py # Chat State Logic
│   └── itinerary_generator.py  # Itinerary Creation Logic
├── requirements.txt            # Dependencies
└── README.md
```

## Setup & Running

1. **Create Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # Windows
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Testing the Chat Endpoint

You can use `curl` or Postman. The server runs at `http://127.0.0.1:8000`.

**Endpoint**: `POST /chat`

**Example 1: Starting Conversation**
```json
{
  "message": "Hi",
  "state": {}
}
```
*Response*: "Welcome! I'm your travel assistant. Where would you like to go?"

**Example 2: Providing Details**
```json
{
  "message": "I want to go to Paris",
  "state": {}
}
```
*Response*: "Great choice! How many days..." (and updates state to `{"destination": "Paris"}`)

**Example 3: Simulating Full State (For Testing Itinerary)**
```json
{
  "message": "Go",
  "state": {
      "destination": "Paris",
      "duration": "3",
      "month": "May",
      "travel_type": "Solo"
  }
}
```
*Response*: Returns the full markdown itinerary.
