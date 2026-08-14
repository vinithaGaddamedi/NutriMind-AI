import pytest
import requests

def test_generate_meal_plan(page):
    page.goto("http://localhost:5173/meal-planner")

    page.select_option("select[name='diet']", "vegetarian")
    page.select_option("select[name='goal']", "weight_loss")

    page.fill("input[name='age']", "30")
    page.fill("input[name='weight']", "70")
    page.fill("input[name='height']", "170")

    page.get_by_test_id("generate-btn").click()

    page.wait_for_selector("text=kcal/day")

    assert page.locator("text=Monday").is_visible()


def test_ui_matches_api(page):
    # Call the actual API directly
    api_response = requests.post(
        "http://localhost:8000/api/meal/meal-plan/single",
        json={
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
    ).json()

    # Call the UI
    page.goto("http://localhost:5173/meal-planner")

    page.fill("input[name='age']", "30")
    page.fill("input[name='weight']", "70")
    page.fill("input[name='height']", "170")

    page.get_by_test_id("generate-btn").click()

    page.wait_for_selector("text=kcal/day")
    assert str(api_response["calories"]) in page.content()


def test_invalid_input(page):
    page.goto("http://localhost:5173/meal-planner")

    # Clear the age input (invalid)
    page.fill("input[name='age']", "-5")

    page.get_by_test_id("generate-btn").click()

    # The UI should display validation error and block the API call
    assert page.locator("text=must be greater than 0").is_visible()


def test_family_plan(page):
    page.goto("http://localhost:5173/meal-planner")

    # Switch to family mode
    page.click("button:has-text('Family Mode')")

    # Fill family data
    page.fill("input[name='member1_age']", "30")
    page.fill("input[name='member1_weight']", "70")
    page.fill("input[name='member2_age']", "60")
    page.fill("input[name='member2_weight']", "65")

    page.get_by_test_id("generate-btn").click()

    # Wait for the family results wrapper
    page.wait_for_selector("text=Portions")

    assert page.locator("text=kcal").first.is_visible()
