from fastapi import APIRouter
from services.recommendation_service import get_recommendations

router = APIRouter()

@router.get("/{user_id}")
def get_user_recommendations(user_id: int):
    return get_recommendations(user_id)
