# 🧠 ExploreAI Assistant - Project Memory
*A living document of the project's state, architecture, and daily progress.*

## 📅 Latest Update: January 21, 2026

### 🚀 Current State
**Status:** 🚀 Deployed & Verified
**Live App:** [https://travelbot-esmp4m73kkbcfnhpdwhcqz.streamlit.app/](https://travelbot-esmp4m73kkbcfnhpdwhcqz.streamlit.app/)
**Repository:** [https://github.com/SanjayJoshy55/Travelbot](https://github.com/SanjayJoshy55/Travelbot)

### 🛠 Tech Stack & Architecture
*   **Frontend:** Streamlit (Custom Glassmorphism CSS, `streamlit_app/main.py`)
*   **Backend Logic:** Python (Modular Agents in `backend/app/agents/`)
*   **AI Model:** Groq (`llama-3.1-8b-instant`) for fast, free inference.
*   **Data Sources:**
    *   **Wikipedia:** Location summaries, cultural info, and images.
    *   **OpenTripMap:** Geospatial data for attractions and museums.
    *   **Google Flights/Skyscanner:** Deep links for booking (no API integration yet).
*   **State Management:** Streamlit Session State (`st.session_state`) + In-memory conversation manager.

### ✨ Key Features Implemented
1.  **AI Itinerary Director:**
    *   Generates detailed day-by-day travel narratives using Groq.
    *   Fetches real images from Wikipedia.
    *   Displays interactive maps using `pandas` (lat/lon).
2.  **Travel Planner Agent:**
    *   Calculates distance and estimated flight time between Origin & Destination.
    *   Provides direct booking links.
3.  **Resource Agent:**
    *   Generates packing lists, local lingo, and budget estimates based on destination/month.
4.  **UI/UX:**
    *   Premium "Glassmorphism" design.
    *   Chat-based interface with distinct user/assistant bubbles.
    *   Robust error handling and "Director" status indicators.

### 🔐 Security & Deployment
*   **API Keys:** `GROQ_API_KEY` and `OPENTRIPMAP_API_KEY` are scrubbed from code.
*   **Local Run:** Uses `.env` file (User has verified this works).
*   **Cloud Run:** Configured for Streamlit Cloud (Requires Secrets injection).
*   **Dependencies:** `requirements.txt` updated with `pandas`, `httpx`, `groq`, etc.

---

## 📜 History Log

### 2026-01-21 (Today)
*   **Feature:** Implemented secure Git flow; scrubbed leaked API keys from `debug_log.txt` and python scripts.
*   **Fix:** Added `pandas` to `requirements.txt` to fix map rendering on deployment.
*   **Fix:** Added `httpx` to `requirements.txt` for OpenTripMap client.
*   **Infrastructure:** Initialized Git repository and pushed to GitHub main branch.
*   **Ops:** Verified local `.env` setup restores functionality after cleanup.
*   **Release:** Deployed to Streamlit Cloud. Verified "Happy Path" (Paris 3-day trip) on live URL with successful map and image rendering.
