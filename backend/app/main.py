from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.models import ChatRequest, ChatResponse
from app.conversation_manager import ConversationManager
from app.itinerary_generator import ItineraryGenerator

# Load environment variables
load_dotenv()

app = FastAPI(title="Travel Chatbot MVP", description="Phase 1 Backend for Agentic Travel Planner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversation_mgr = ConversationManager()
itinerary_gen = ItineraryGenerator()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Process message and update state
        bot_reply, new_state, status = conversation_mgr.process_message(request.message, request.state)
        
        if status == "ready_to_generate":
            # If all info is collected, generate the itinerary
            itinerary = itinerary_gen.generate_itinerary(new_state)
            return ChatResponse(
                response=itinerary,
                state=new_state,
                status="completed"
            )
        else:
            # Continue conversation
            return ChatResponse(
                response=bot_reply,
                state=new_state,
                status="collecting_info"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Travel Chatbot Service is Running"}
