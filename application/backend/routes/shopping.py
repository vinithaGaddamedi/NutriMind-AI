import logging
from fastapi import APIRouter
from schemas.shopping import ShoppingPlanRequest, ShoppingPlanResponse
from services.grocery_service import generate_grocery_list
from services.pantry_service import remove_pantry_items
from services.budget_service import optimize_for_budget
from services.store_service import optimize_store_route
from services.price_service import compare_prices

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/shopping-plan", response_model=ShoppingPlanResponse)
def shopping_plan(payload: ShoppingPlanRequest):
    logger.info("Generating shopping plan")
    grocery = generate_grocery_list(payload.meal_plan)
    grocery = remove_pantry_items(grocery, payload.pantry)

    store = payload.store if hasattr(payload, 'store') else "walmart"
    grocery = optimize_store_route(grocery, store)

    optimized, total, status = optimize_for_budget(grocery, payload.budget)
    
    comparison = compare_prices(optimized)

    return ShoppingPlanResponse(
        grocery_list=optimized,
        total_cost=total,
        status=status,
        store_totals=comparison["store_totals"],
        best_store=comparison["best_store"]
    )
