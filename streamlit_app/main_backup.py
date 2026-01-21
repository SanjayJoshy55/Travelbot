import streamlit as st
import sys
import os
import time

# Add backend to python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(current_dir, '..', 'backend')
sys.path.append(backend_path)

from app.itinerary_generator import ItineraryGenerator

# --- Page Config ---
st.set_page_config(
    page_title="ExploreAI | Premium Travel Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS (Glassmorphism & Premium UI) ---
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(33, 46, 74) 90%);
        color: #e2e8f0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    /* Titles/Headers */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    
    /* Inputs */
    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        background-color: rgba(30, 41, 59, 0.5);
        color: #f8fafc;
        border-radius: 8px;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    /* Chat/Status Container */
    .element-container {
        border-radius: 12px;
    }
    
    /* Custom Card for Itinerary */
    .itinerary-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

import streamlit as st
import sys
import os
import time

# Add backend to python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(current_dir, '..', 'backend')
sys.path.append(backend_path)

from app.agents.director import DirectorAgent
from app.conversation_manager import ConversationManager

# --- Page Config ---
st.set_page_config(
    page_title="ExploreAI | Agentic Travel Assistant",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS (Glassmorphism & Premium UI) ---
st.markdown("""
<style>
    /* Global Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(33, 46, 74) 90%);
        color: #e2e8f0;
    }
    
    /* Header Overlay */
    header {
        background: transparent !important;
    }
    
    /* Chat Bubbles */
    .stChatMessage {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    [data-testid="stChatMessageAvatarUser"] {
        background-color: #3b82f6;
    }
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #ec4899;
    }

    /* Titles/Headers */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Input Area */
    .stChatInput > div {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        color: white !important;
        border-radius: 24px !important;
    }
    
    /* Status styling */
    .stStatus {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🌍 ExploreAI Assistant")
st.caption("Chat with me to plan your perfect trip!")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hey traveler! Where are you dreaming of going?"}
    ]

if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = {} # Stores gathered info (dest, duration, etc.)

if "manager" not in st.session_state:
    st.session_state.manager = ConversationManager()

# --- Helper to Display Chat ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Logic ---
if prompt := st.chat_input("Type your answer here..."):
    # 1. User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Process message
    current_stage = st.session_state.conversation_state.get("stage")
    print(f"DEBUG: Current Stage: {current_stage}")
    
    # Logic: If we are in a specific stage (Reviewing/Origin), let Manager handle it.
    # Otherwise, if we have a result, assume it's a modification request.
    # Otherwise, it's normal info collection.
    
    if current_stage in ["reviewing_itinerary", "collecting_origin"]:
         response_text, updated_state, status = st.session_state.manager.process_message(
            prompt, 
            st.session_state.conversation_state
        )
         st.session_state.conversation_state = updated_state
         
    elif "final_result" in st.session_state and st.session_state.final_result:
        # User is asking for a change (and we aren't in a specific flow)
        print("DEBUG: Entering Modifying Block")
        status = "modifying"
        response_text = "Thinking..." 
        updated_state = st.session_state.conversation_state
        
    else:
        # Normal flow
        response_text, updated_state, status = st.session_state.manager.process_message(
            prompt, 
            st.session_state.conversation_state
        )
        st.session_state.conversation_state = updated_state
    
    # 3. Handle Status
    if status in ["collecting_info", "collecting_origin"]:
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        
    elif status == "ready_to_generate":
        # Ack the final input
        with st.chat_message("assistant"):
            ack_msg = f"Awesome! Planning a {updated_state.get('travel_type', 'trip')} to **{updated_state.get('destination')}** for **{updated_state.get('duration')} days** in **{updated_state.get('month')}**."
            st.markdown(ack_msg)
        st.session_state.messages.append({"role": "assistant", "content": ack_msg})
        
        # 4. Generate Itinerary (Via Director)
        status_container = st.status("🎬 Director Agent taking charge...", expanded=True)
        try:
            status_container.write("🕵️ Researcher: Scouting locations & Wiki data...")
            # Instantiate Director
            director = DirectorAgent()
            
            # Use 'state' dict directly
            result = director.create_itinerary(updated_state)
            
            status_container.update(label="✅ Itinerary Ready!", state="complete", expanded=False)
            
            # Save result for replanning
            st.session_state.final_result = result
            
            # 5. Display Result
            with st.chat_message("assistant"):
                # Handle Structure (Dict)
                if isinstance(result, dict):
                    meta = result.get("meta", {})
                    narrative_text = result.get("narrative", "")
                    
                    # 1. Hero Image
                    if meta.get("image"):
                        st.image(meta["image"], caption=f"Welcome to {meta.get('destination')}", use_container_width=True)
                    
                    # 2. Map
                    coords = meta.get("coordinates")
                    if coords and coords.get("lat") != 0:
                        import pandas as pd
                        df = pd.DataFrame([coords])
                        st.map(df, size=20, zoom=10)
                        
                    # 3. Text
                    st.markdown(narrative_text)
                    st.session_state.messages.append({"role": "assistant", "content": narrative_text})
            
            # Allow follow-up
            follow_up = "Need any changes? You can say 'Add a dinner' or 'Remove museums'."
            st.session_state.messages.append({"role": "assistant", "content": follow_up})
            with st.chat_message("assistant"):
                 st.markdown(f"_{follow_up}_")
                 
        except Exception as e:
            status_container.update(label="❌ Error occurred", state="error")
            st.error(f"Details: {e}")
            
        # Update stage to allow review
        st.session_state.conversation_state["stage"] = "reviewing_itinerary"

    elif status == "showing_travel_options":
        # User Provided Origin -> Get Travel Details
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        
        # Call Travel Agent
        from app.agents.travel_agent import TravelAgent
        travel_agent = TravelAgent()
        
        origin = updated_state.get("origin")
        dest = updated_state.get("destination")
        
        options = travel_agent.plan_trip(origin, dest)
        
        # Render Travel Card
        with st.chat_message("assistant"):
            st.info(f"✈️ **Travel Estimate: {options.get('origin', 'Origin')} ➡️ {options.get('destination', 'Destination')}**")
            st.markdown(f"**Estimated Time:** {options.get('estimated_duration', 'N/A')} ({options.get('distance', 'Distance N/A')})")
            
            st.markdown(f"👉 [**Google Flights**]({options.get('booking_link', '#')})")
                
            st.caption(f"💡 Tip: {options.get('tips', 'Check flights early.')}")
            
            # Save card to history
            card_md = f"✈️ **Travel Estimate**\n\n*Time:* {options.get('estimated_duration', 'N/A')}\n\n[Google Flights]({options.get('booking_link', '#')})"
            st.session_state.messages.append({"role": "assistant", "content": card_md})

        # --- NEW: Travel Resources (Parallel Call) ---
        from app.agents.resource_agent import ResourceAgent
        resource_agent = ResourceAgent()
        
        with st.status("🧳 Assembling your Travel Kit...", expanded=True) as status_box:
            resources = resource_agent.get_resources(dest, updated_state.get('month', 'Any'), updated_state.get('travel_type', 'Any'))
            status_box.update(label="✅ Travel Kit Ready!", state="complete", expanded=False)

        # Render Travel Kit
        with st.chat_message("assistant"):
            st.markdown("### 🧳 Your Travel Kit")
            
            # 1. Packing List
            with st.expander("🎒 Smart Packing List", expanded=True):
                st.markdown(f"**Essentials for {updated_state.get('month')}**:")
                for item in resources.get('packing_list', []):
                    st.checkbox(item, key=f"pack_{item}")
            
            # 2. Lingo & Budget
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 🗣️ Local Lingo")
                for phrase in resources.get('lingo', []):
                    st.text(f"{phrase['phrase']} -> {phrase['translation']}")
            
            with c2:
                st.markdown("#### 💰 Budget Est.")
                for item in resources.get('budget', []):
                    st.markdown(f"**{item['item']}**: {item['cost']}")
            
            if resources.get('tip'):
                st.info(f"**Cultural Tip**: {resources['tip']}")
        
        # Save kit to history (Simplified)
        kit_md = "🧳 **Travel Kit Generated** (Packing, Lingo, Budget)"
        st.session_state.messages.append({"role": "assistant", "content": kit_md})

        # Final State
        st.session_state.conversation_state["stage"] = "complete"

    elif status == "modifying":
        # Interactive Replanning 
        with st.chat_message("assistant"):
            st.markdown(f"_{response_text}_") # Just a spinner effect usually
            
        status_container = st.status("🔄 Updating Plan...", expanded=True)
        try:
            director = DirectorAgent()
            current_result = st.session_state.final_result
            
            updated_result = director.modify_itinerary(current_result, prompt)
            
            status_container.update(label="✅ Updated!", state="complete", expanded=False)
            
            # Update state
            st.session_state.final_result = updated_result
            
            # Display new narrative ONLY (don't repay map/image unless requested, keeps it clean)
            with st.chat_message("assistant"):
                st.markdown(updated_result["narrative"])
            st.session_state.messages.append({"role": "assistant", "content": updated_result["narrative"]})
            
        except Exception as e:
             st.error(f"Modification failed: {e}")

# --- Sidebar Reset ---
with st.sidebar:
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "👋 Hey traveler! Where are you dreaming of going?"}]
        st.session_state.conversation_state = {}
        st.session_state.final_result = None
        st.rerun()
