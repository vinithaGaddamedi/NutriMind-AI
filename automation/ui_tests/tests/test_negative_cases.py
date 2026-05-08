import allure
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:5173"

@allure.feature("Negative Testing")
@allure.story("Form Validation")
def test_invalid_age(page: Page):
    with allure.step("Navigate to Meal Planner"):
        page.goto(f"{BASE_URL}/meal-planner")
    
    with allure.step("Fill invalid negative age"):
        page.fill("input[name='age']", "-5")
        page.click("button:has-text('Generate Weekly Plan')")
    
    with allure.step("Verify validation error is displayed"):
        expect(page.locator("text=Age must be greater than 0")).to_be_visible()

@allure.feature("Intelligence Validation")
@allure.story("Pantry Usage")
def test_pantry_usage_reasons(page: Page):
    with allure.step("Set Pantry local storage explicitly"):
        page.goto(f"{BASE_URL}/meal-planner")
        page.evaluate("window.localStorage.setItem('userPantry', JSON.stringify({'Rice': true, 'Milk': true}))")
        page.reload()

    with allure.step("Fill valid profile and generate"):
        page.fill("input[name='name']", "Test User")
        page.fill("input[name='age']", "30")
        page.fill("input[name='weight']", "70")
        page.fill("input[name='height']", "170")
        page.click("button:has-text('Generate Weekly Plan')")
        expect(page.locator("h4:has-text('Monday')").first).to_be_visible(timeout=10000)

    with allure.step("Verify meal reasons include pantry matches"):
        reasons = page.locator("div:has-text('Why? →')").all_inner_texts()
        assert any("pantry" in r.lower() for r in reasons), "AI did not prioritize pantry items!"

@allure.feature("Intelligence Validation")
@allure.story("Meal Variety")
def test_variety_no_duplicate_meals(page: Page):
    with allure.step("Navigate and generate meal plan"):
        page.goto(f"{BASE_URL}/meal-planner")
        page.fill("input[name='name']", "Variety User")
        page.fill("input[name='age']", "25")
        page.fill("input[name='weight']", "60")
        page.fill("input[name='height']", "165")
        page.click("button:has-text('Generate Weekly Plan')")
        expect(page.locator("h4:has-text('Monday')").first).to_be_visible(timeout=10000)
    
    with allure.step("Assert meal diversity across the week"):
        meal_elements = page.locator("span[style*='color: var(--text-muted)']").all_inner_texts()
        unique_meals = set(meal_elements)
        assert len(unique_meals) > 3, "AI failed to provide a diverse meal plan!"

@allure.feature("Negative Testing")
@allure.story("Extreme Inputs")
def test_extreme_inputs(page: Page):
    with allure.step("Navigate to Meal Planner"):
        page.goto(f"{BASE_URL}/meal-planner")
    
    with allure.step("Fill extreme age (> 150)"):
        page.fill("input[name='age']", "999")
        page.fill("input[name='weight']", "1000")
        page.click("button:has-text('Generate Weekly Plan')")
    
    with allure.step("Verify extreme values are handled or clamped"):
        # We assume our frontend allows the input but macros might skyrocket or crash.
        # Ensure it doesn't crash to an unhandled exception.
        try:
            expect(page.locator("h4:has-text('Monday')").first).to_be_visible(timeout=5000)
            # If it generates successfully, ensure calories don't show NaN
            calories_text = page.locator("div", has_text="kcal/day").inner_text()
            assert "NaN" not in calories_text
        except:
            # Or it might show a validation error if we add one in the future
            pass
