from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ShoppingPlanRequest(BaseModel):
    meal_plan: Dict[str, Any]
    pantry: List[str] = []
    budget: float = 100.0
    store: str = "walmart"

class GroceryItem(BaseModel):
    item: str
    quantity: int

class ShoppingPlanResponse(BaseModel):
    grocery_list: Dict[str, List[GroceryItem]]
    total_cost: float
    status: str
    store_totals: Dict[str, float]
    best_store: str
