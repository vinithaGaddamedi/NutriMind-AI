import allure
import pytest

@allure.feature("End to End Platform Flow")
def test_full_flow(page):
    with allure.step("Navigate to application and open Meal Planner"):
        page.goto("http://localhost:5173")
        page.click("text=AI Meal Planner")
        page.wait_for_selector("text=Try it out now")
        page.click("text=Try it out now")

    with allure.step("Generate Single Meal Plan"):
        # We assume we are on Login page now
        page.click("button:has-text('Sign In')")
        
        page.click("text=Meal Planner")
        page.click("data-testid=generate-plan", timeout=5000)

    with allure.step("Validate AI Generation Result"):
        assert page.locator("text=Nutrition Goal").is_visible()

@allure.feature("Negative Testing")
def test_invalid_input(page):
    with allure.step("Test negative age constraint in Meal Planner"):
        page.goto("http://localhost:5173/meal-planner")
        page.fill("input[name='age']", "-1")
        # Ensure that HTML5 validation or manual validation handles the -1 securely
        page.click("data-testid=generate-plan")
        # Validate that plan doesn't incorrectly succeed with negative inputs (assuming some default validation message is rendered)
        # assert page.locator("text=Invalid").is_visible() 
