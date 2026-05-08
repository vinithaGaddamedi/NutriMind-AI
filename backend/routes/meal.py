from fastapi import APIRouter
from schemas.meal import (
    SinglePlanRequest, SinglePlanResponse,
    FamilyPlanRequest, FamilyPlanResponse
)
from services import meal_service
from services.nutrition_score import calculate_meal_score

router = APIRouter()

@router.post("/meal-plan/single", response_model=SinglePlanResponse)
def create_single_meal_plan(request: SinglePlanRequest):
    user_dict = request.profile.model_dump()
    plan = meal_service.generate_single_plan(
        user=user_dict,
        diet=request.diet
    )
    score = calculate_meal_score(plan["meal_plan"])
    plan["nutrition_score"] = score
    return plan

@router.post("/meal-plan/family", response_model=FamilyPlanResponse)
def create_family_meal_plan(request: FamilyPlanRequest):
    users_dict = [m.model_dump() for m in request.members]
    plan = meal_service.generate_family_plan(
        users=users_dict,
        diet=request.diet
    )
    score = calculate_meal_score(plan["family_plan"])
    plan["nutrition_score"] = score
    return plan
