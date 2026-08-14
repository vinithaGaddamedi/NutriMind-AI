from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message text", min_length=1)
    conversation_id: Optional[str] = Field(default=None, description="Optional unique conversation session identifier")
    user_context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="User contextual data like diet, goals, or user_id")

class ChatResponse(BaseModel):
    response: str = Field(..., description="NutriMind AI assistant generated message")
    conversation_id: str = Field(..., description="Conversation session identifier")
    model: str = Field(..., description="AI model used for generating the response")
