from pydantic import BaseModel
from typing import Optional, Dict

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    state: Optional[Dict] = {}

class ChatResponse(BaseModel):
    response: str
    state: Dict
    status: str  # "collecting_info" or "completed"
