# Project Workflow: Agentic Travel Planner Chatbot

This document outlines the workflow of the Agentic Travel Planner Chatbot. The application is a **Streamlit-based Monolith** that directly orchestrates AI agents to generate travel itineraries.

## 1. Architecture Overview

The system is a unified Python application where the frontend (Streamlit) directly imports and executes the backend logic.

-   **Frontend**: Streamlit (Python UI).
    -   Renders the Chat Interface.
    -   Manages Session State (`st.session_state`).
    -   Handles User Input and Display.
-   **Backend Logic**: Python Modules (in `backend/app/`).
    -   **Agents**: Director (Planner), Writer (Content), Resource (Wiki/Data), Travel (Logistics).
    -   **State Management**: `ConversationManager`.
-   **AI/Data**:
    -   **LLM**: Google Gemini / Groq (via API).
    -   **Context**: Wikipedia (via ChromaDB for RAG).

## 2. Execution Workflow (How to Run)

To start the application:

1.  **Open Terminal**: Navigate to the project root (`C:\Users\sanja\Desktop\chatbot 2`).
2.  **Run Command**:
    ```powershell
    streamlit run streamlit_app/main.py
    ```
3.  **Access Application**:
    The application will open in your default browser at `http://localhost:8501`.

## 3. User Interaction & Data Flow

### Phase 1: Information Collection (Chat Loop)
1.  **User Input**: User types in the Streamlit chat box.
2.  **Processing**:
    -   Streamlit passes the input to `ConversationManager` (imported from `backend`).
    -   The Manager updates the internal state (Destination, Duration, Month).
3.  **Response**:
    -   Streamlit updates the UI with the bot's reply (e.g., asking for missing info).

### Phase 2: Agent Orchestration
Once the user confirms the details:

1.  **Director Agent** (`backend/app/agents/director.py`):
    -   Called directly by `main.py`.
    -   coordinates the creation of the itinerary.
2.  **Writer & Resource Agents**:
    -   Fetch data (Wikipedia) and generate the narrative.
3.  **Result**:
    -   The final dictionary (Narrative + Metadata) is returned to the Streamlit app.

### Phase 3: Rendering & Tools
1.  **Itinerary Display**:
    -   `st.markdown` renders the generated travel plan.
    -   `st.image` displays destination photos (if available).
    -   `st.map` displays coordinates.
2.  **Travel Tools**:
    -   **Travel Agent**: calculates flight estimates and generates Google Flights links.
    -   **Resource Agent**: Generates "Travel Kits" (Packing lists, Budget, Lingo) displayed in Expanders.

## 4. Key Files

-   **`streamlit_app/main.py`**: The application entry point. Contains all UI logic and the main even loop.
-   **`backend/app/conversation_manager.py`**: Logic for parsing user intent and managing the state machine.
-   **`backend/app/agents/`**:
    -   `director.py`: Main orchestrator.
    -   `travel_agent.py`: Handles logistics and flight links.
    -   `resource_agent.py`: Handles packing lists and local info.
