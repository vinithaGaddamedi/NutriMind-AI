import pytest
from pytest_bdd import scenario, given, when, then
import requests
import allure

from pytest_bdd import scenario, given, when, then, parsers

BASE_URL = "http://localhost:8000/api"

@scenario('../features/nutrition.feature', 'Validate nutrition calculation based on goals')
def test_nutrition_logic():
    pass

@given(parsers.parse('a user profile with age "{age}", weight "{weight}", height "{height}", gender "{gender}", and goal "{goal}"'), target_fixture="user_profile")
def user_profile(age, weight, height, gender, goal):
    return {
        "name": "TestUser",
        "age": int(age),
        "weight": float(weight),
        "height": float(height),
        "gender": gender,
        "goal": goal,
        "allergies": [],
        "dislikes": [],
        "pantry": []
    }

@when('I request a meal plan', target_fixture="request_meal_plan")
def request_meal_plan(user_profile):
    payload = {"profile": user_profile, "diet": "vegetarian"}
    response = requests.post(f"{BASE_URL}/meal/meal-plan/single", json=payload)
    assert response.status_code == 200, f"API failed with {response.text}"
    return response.json()

@then(parsers.parse('the calculated calories should be around "{expected_calories}"'))
def verify_calories(request_meal_plan, expected_calories):
    actual_cal = request_meal_plan["calories"]
    expected = int(expected_calories)
    assert abs(actual_cal - expected) < (expected * 0.25), f"Calories {actual_cal} out of acceptable range near {expected}"

@then('the protein ratio should match the goal')
def verify_macros(request_meal_plan, user_profile):
    macros = request_meal_plan["macros"]
    goal = user_profile["goal"]
    if goal == "muscle_gain":
        assert macros["protein_g"] > 90, "Protein too low for muscle gain"
    elif goal == "weight_loss":
        assert macros["protein_g"] > 50, "Protein too low for weight loss"
