from pydantic import BaseModel
from typing import List, Dict, Any

class UserProfile(BaseModel):
    name: str = "User"
    age: int
    weight: float
    height: float
    gender: str = "male"
    goal: str
    allergies: List[str] = []
    dislikes: List[str] = []
    pantry: List[str] = []

class SinglePlanRequest(BaseModel):
    profile: UserProfile
    diet: str

class FamilyPlanRequest(BaseModel):
    members: List[UserProfile]
    diet: str

class Macros(BaseModel):
    protein_g: int
    carbs_g: int
    fats_g: int
    iron_mg: float = 0.0
    calcium_mg: float = 0.0
    vitamin_a_iu: float = 0.0

class MealItem(BaseModel):
    name: str
    reason: str = ""

class DailyMeals(BaseModel):
    breakfast: MealItem
    lunch: MealItem
    dinner: MealItem

class SinglePlanResponse(BaseModel):
    user: str
    calories: int
    macros: Macros
    meal_plan: Dict[str, DailyMeals]
    nutrition_score: float
    insights: List[str] = []

class MemberPortion(BaseModel):
    calories: int

class FamilyDailyPlan(BaseModel):
    meals: DailyMeals
    portions: Dict[str, MemberPortion]

class FamilyPlanResponse(BaseModel):
    family_plan: Dict[str, FamilyDailyPlan]
    nutrition_score: float
    insights: List[str] = []
