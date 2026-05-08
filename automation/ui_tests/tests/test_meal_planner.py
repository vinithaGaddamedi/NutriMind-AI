from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.base_page import BasePage

class MealPlannerPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.diet_select = page.locator("select").nth(0)
        self.goal_select = page.locator("select").nth(1)
        self.allergies_input = page.locator("input[placeholder='e.g. nuts, dairy']")
        self.generate_btn = page.locator("button:has-text('Generate Weekly Plan')")
        self.grocery_btn = page.locator("button:has-text('Generate Grocery List')")

    def generate_plan(self, diet, goal, allergies):
        self.navigate("http://localhost:5173/meal-planner")
        self.diet_select.select_option(value=diet)
        self.goal_select.select_option(value=goal)
        self.allergies_input.fill(allergies)
        self.generate_btn.click()

def test_meal_plan_generation_flow(page):
    # Setup login
    login_page = LoginPage(page)
    login_page.login("testuser")
    
    # Generate Plan
    meal_planner = MealPlannerPage(page)
    meal_planner.generate_plan("vegetarian", "weight_loss", "nuts")
    
    # Assert plan is generated (Monday header should be visible)
    assert page.locator("h4:has-text('Monday')").is_visible()
    
    # Generate Grocery List
    meal_planner.grocery_btn.click()
    
    # Assert grocery list appears
    assert page.locator("h4:has-text('Smart Grocery List')").is_visible()
