from fastapi import APIRouter, HTTPException, status
from schemas.chat import ChatRequest, ChatResponse
from services.ai_chat_service import chat_service

router = APIRouter()

@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
def chat_endpoint(payload: ChatRequest):
    """
    POST /api/chat/
    Endpoint for NutriMind AI Chatbot conversations.
    """
    if not payload.message or not payload.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message field cannot be empty."
        )

    result = chat_service.generate_chat_response(
        message=payload.message.strip(),
        conversation_id=payload.conversation_id,
        user_context=payload.user_context
    )

    return ChatResponse(
        response=result["response"],
        conversation_id=result["conversation_id"],
        model=result["model"]
    )
