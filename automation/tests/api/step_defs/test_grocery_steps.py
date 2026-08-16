import pytest
from pytest_bdd import scenario, given, when, then
import requests

BASE_URL = "http://localhost:8000/api"

@scenario('../features/grocery.feature', 'Generate grocery list from complex meal plan')
def test_meal_to_grocery_integration():
    pass

@given('a complex weekly meal plan containing "Brown rice + dal + salad"', target_fixture="complex_meal_plan")
def complex_meal_plan():
    # Mocking a subset of a generated plan matching the schema
    return {
        "Monday": {
            "lunch": {"name": "Brown rice + dal + salad", "reason": "High fiber"}
        }
    }

@when('I submit the plan to the grocery engine', target_fixture="submit_to_grocery")
def submit_to_grocery(complex_meal_plan):
    payload = {
        "meal_plan": complex_meal_plan,
        "pantry": [],
        "budget": 100.0,
        "store": "walmart"
    }
    response = requests.post(f"{BASE_URL}/shopping/shopping-plan", json=payload)
    assert response.status_code == 200, f"API failed: {response.text}"
    return response.json()

@then('the grocery list should contain "Brown rice" and "Dal"')
def verify_grocery_items(submit_to_grocery):
    # Flatten the grocery list from category dict to a flat list of names
    items = []
    for category, category_items in submit_to_grocery.get("grocery_list", {}).items():
        for item in category_items:
            items.append(item["item"].lower())
            
    assert any("rice" in i for i in items), f"Rice not found in grocery list. Found: {items}"
    assert any("dal" in i for i in items), f"Dal not found in grocery list. Found: {items}"

@then('the total cost should be calculated')
def verify_cost(submit_to_grocery):
    assert "total_cost" in submit_to_grocery
    assert submit_to_grocery["total_cost"] > 0
