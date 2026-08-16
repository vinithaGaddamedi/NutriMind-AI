from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class UserContext(BaseModel):
    dietary_preferences: Optional[List[str]] = Field(default_factory=list, description="Dietary preferences (e.g., vegetarian, keto)")
    allergies: Optional[List[str]] = Field(default_factory=list, description="User allergies (e.g., peanut, dairy)")
    pantry_items: Optional[List[str]] = Field(default_factory=list, description="Items currently in the user's pantry")
    budget: Optional[float] = Field(default=None, description="Weekly grocery budget")
    goals: Optional[List[str]] = Field(default_factory=list, description="Health or fitness goals")

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message text", min_length=1, max_length=1000)
    conversation_id: Optional[str] = Field(default=None, description="Optional unique conversation session identifier")
    user_context: Optional[UserContext] = Field(default_factory=UserContext, description="User contextual data like diet, goals, or allergies")

class ChatResponse(BaseModel):
    response: str = Field(..., description="NutriMind AI assistant generated message")
    conversation_id: str = Field(..., description="Conversation session identifier")
    model: str = Field(..., description="AI model used for generating the response")

