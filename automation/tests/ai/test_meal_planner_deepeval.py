import pytest
import requests
from tests.ai.metrics.dietary_compliance import DietaryComplianceMetric
from tests.ai.metrics.allergy_compliance import AllergyComplianceMetric
from tests.ai.metrics.meal_plan_quality import MealPlanQualityMetric

MEAL_API_URL = "http://localhost:8000/api/meal/meal-plan/single"

@pytest.mark.deepeval
@pytest.mark.agentic
def test_meal_planner_single_vegetarian_quality():
    payload = {
        "profile": {
            "name": "DeepEval Test User",
            "age": 30,
            "weight": 70,
            "height": 170,
            "gender": "female",
            "goal": "weight_loss"
        },
        "diet": "vegetarian"
    }

    response = requests.post(MEAL_API_URL, json=payload)
    assert response.status_code == 200, f"Meal API failed: {response.text}"

    data = response.json()
    meal_plan_str = str(data.get("meal_plan", {}))

    # Evaluate metrics
    diet_metric = DietaryComplianceMetric(target_diet="vegetarian", threshold=0.9)
    quality_metric = MealPlanQualityMetric(threshold=0.7)

    res_diet = diet_metric.measure(meal_plan_str)
    res_quality = quality_metric.measure(meal_plan_str)

    assert res_diet["passed"], f"Diet metric failed: {res_diet['violations']}"
    assert res_quality["passed"], f"Quality metric failed: {res_quality['details']}"
    print(f"\n✅ Meal Planner DeepEval Evaluation Passed (Quality Score: {res_quality['score']:.2f})")
