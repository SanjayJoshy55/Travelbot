# 🗺️ Travelbot Upgrade Plan due to user request

## 🎯 Objective
Implement two major features to enhance utility and retention:
1.  **Budget Calculator**: Customize itineraries based on spending power.
2.  **"My Trips" History**: Persist itineraries using a database.

---

## 💎 Feature 1: Budget & Style Selector

### 1. Frontend Changes (`streamlit_app/main.py`)
*   **Add Input**: Insert a generic setting for Budget.
    *   *Where*: In the Sidebar (always accessible).
    *   *Component*: `st.select_slider("Budget Style", options=["Backpacker 🎒", "Comfort 🏨", "Luxury 💎"])`.
    *   *State*: Save to `st.session_state['budget_style']`.

### 2. Backend Logic (`backend/app/agents/`)
*   **Director Agent (`director.py`)**:
    *   **Prompt Engineering**: Inject the selected budget style into the LLM prompt.
    *   *Instruction*: "The user has a [Style] budget. Select accommodation, dining, and activities appropriate for this tier."
*   **Travel Agent (`travel_agent.py`)**:
    *   Update flight search tips (e.g., "Look for budget airlines" vs "Direct flights preferred").
*   **Resource Agent (`resource_agent.py`)**:
    *   Update the `budget` section of the JSON response to calculate different estimates based on the tier.

---

## 💾 Feature 2: Trip Persistence ("My Trips")

### 1. Database Architecture
*   **Storage**: SQLite (`trips.db`).
    *   *Note*: On Streamlit Cloud, SQLite files are deleted when the app reboots. For permanent cloud storage, we would migrate this logic to **Supabase** later. For now, SQLite is the fastest way to build the logic.
*   **Schema**:
    ```sql
    CREATE TABLE IF NOT EXISTS trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        destination TEXT,
        summary TEXT,       -- Short description (e.g., "5 days in Paris")
        full_data JSON,     -- The entire 'final_result' object
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ```

### 2. Backend Service (`backend/app/storage.py`)
*   Create a `TripStorage` class.
    *   `save_trip(destination, summary, full_data)`
    *   `get_all_trips()` -> Returns list of (id, summary).
    *   `get_trip(id)` -> Returns full_data.

### 3. Frontend Integration (`streamlit_app/main.py`)
*   **Save Action**:
    *   Add a "💾 Save Trip" button below the generated itinerary.
    *   On click -> Call `TripStorage.save_trip()`.
*   **Load Action (Sidebar)**:
    *   Add a "📂 Load Past Trip" section in the sidebar.
    *   Display a list of saved trips.
    *   On selection -> Replace `st.session_state['final_result']` with the loaded data and re-render the view.

---

## 🚀 Execution Order
1.  **Step 1**: Implement the **Budget Slider** in Frontend & pass it to the Director.
2.  **step 2**: Create `storage.py` (SQLite handler).
3.  **Step 3**: Connect the "Save" and "Load" buttons in the Streamlit UI.
