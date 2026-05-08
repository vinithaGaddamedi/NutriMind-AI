import pytest
import requests

BASE_URL = "http://localhost:8000/api/meal"

# Unit tests embedded per instructions
def test_bmr_calculation():
    from services.nutrition_service import calculate_bmr
    bmr = calculate_bmr(70, 170, 30, "male")
    assert bmr > 1500

def test_meal_plan_structure():
    from services.meal_service import generate_weekly_meal
    plan = generate_weekly_meal("vegetarian", "weight_loss")
    assert "Monday" in plan
    assert "breakfast" in plan["Monday"]

def test_family_plan():
    from services.meal_service import generate_family_plan
    users = [
        {"name": "A", "age": 30, "weight": 70, "height": 170, "goal": "weight_loss"},
        {"name": "B", "age": 60, "weight": 65, "height": 160, "goal": "weight_loss"}
    ]
    plan = generate_family_plan(users, "vegetarian")
    assert "Monday" in plan["family_plan"]
    assert "portions" in plan["family_plan"]["Monday"]

def test_goal_calorie_difference():
    from services.nutrition_service import calculate_nutrition
    user1 = {"age":30,"weight":70,"height":170,"goal":"weight_loss"}
    user2 = {"age":30,"weight":70,"height":170,"goal":"muscle_gain"}

    cal1 = calculate_nutrition(user1)["calories"]
    cal2 = calculate_nutrition(user2)["calories"]

    assert cal2 > cal1

# API Level Tests
def test_api_single_meal_plan():
    payload = {
        "profile": {
            "name": "Vinitha",
            "age": 30,
            "weight": 70,
            "height": 170,
            "gender": "female",
            "goal": "weight_loss"
        },
        "diet": "vegetarian"
    }
    response = requests.post(f"{BASE_URL}/meal-plan/single", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user"] == "Vinitha"
    assert "calories" in data
    assert "macros" in data
    assert "meal_plan" in data
    assert "Monday" in data["meal_plan"]

def test_api_family_meal_plan():
    payload = {
        "members": [
            {"name": "User1", "age": 30, "weight": 70, "height": 170, "gender": "male", "goal": "weight_loss"},
            {"name": "User2", "age": 60, "weight": 65, "height": 160, "gender": "female", "goal": "weight_loss"}
        ],
        "diet": "vegetarian"
    }
    response = requests.post(f"{BASE_URL}/meal-plan/family", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "family_plan" in data
    assert "Monday" in data["family_plan"]
    monday = data["family_plan"]["Monday"]
    assert "meals" in monday
    assert "portions" in monday
    assert "User1" in monday["portions"]
    assert "User2" in monday["portions"]
