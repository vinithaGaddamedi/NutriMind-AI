import allure
from playwright.sync_api import expect
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from ui_tests.pages.base_page import BasePage
from ui_tests.pages.locators.locators import LoginLocators, MealLocators, PantryLocators, ShoppingLocators, CartLocators

BASE_URL = "http://localhost:5173"

class LoginPage(BasePage):
    @allure.step("Navigate to Login Page")
    def navigate(self):
        self.page.goto(f"{BASE_URL}/login")

    @allure.step("Login with username: {username}")
    def login(self, username):
        expect(self.page.locator(LoginLocators.LOGIN_BUTTON)).to_be_visible()
        self.page.fill(LoginLocators.USERNAME_INPUT, username)
        self.page.click(LoginLocators.LOGIN_BUTTON)
        expect(self.page).to_have_url(f"{BASE_URL}/dashboard")

class MealPlannerPage(BasePage):
    @allure.step("Fill profile and generate meal plan")
    def fill_profile_and_generate(self, age, weight, height):
        self.page.click(MealLocators.MEAL_MENU)
        expect(self.page).to_have_url(f"{BASE_URL}/meal-planner")
        
        self.page.fill(MealLocators.NAME_INPUT, "CSV User")
        self.page.fill(MealLocators.AGE_INPUT, str(age))
        self.page.fill(MealLocators.WEIGHT_INPUT, str(weight))
        self.page.fill(MealLocators.HEIGHT_INPUT, str(height))
        
        self.page.click(MealLocators.GENERATE_BTN)
        expect(self.page.locator(MealLocators.DAY_HEADER).first).to_be_visible(timeout=10000)
        self.page.click(MealLocators.PROCEED_BTN)

class PantryPage(BasePage):
    @allure.step("Mark items in stock and proceed")
    def mark_in_stock_and_proceed(self):
        expect(self.page).to_have_url(f"{BASE_URL}/pantry")
        btn = self.page.locator(PantryLocators.IN_STOCK_BTN).first
        expect(btn).to_be_visible()
        btn.click()
        self.page.click(PantryLocators.SAVE_BTN)

class ShoppingPage(BasePage):
    @allure.step("Add generated items to cart")
    def add_all_to_cart(self):
        expect(self.page).to_have_url(f"{BASE_URL}/shopping")
        btn = self.page.locator(ShoppingLocators.ADD_CART_BTN)
        expect(btn).to_be_visible(timeout=10000)
        btn.click()

class CartPage(BasePage):
    @allure.step("Checkout and verify order tracking")
    def checkout(self):
        expect(self.page).to_have_url(f"{BASE_URL}/cart")
        self.page.click(CartLocators.CHECKOUT_BTN)
        expect(self.page).to_have_url(f"{BASE_URL}/order-success")
        expect(self.page.locator(CartLocators.SUCCESS_HEADER).first).to_contain_text("Order Placed Successfully!")

    @allure.step("Track Order")
    def verify_order_and_track(self):
        self.page.click(CartLocators.TRACK_BTN)
        # Using correct assertion logic to pass test properly
        expect(self.page.locator(CartLocators.ORDERS_HEADER).first).to_contain_text("Your Orders")
        expect(self.page.locator(CartLocators.ORDER_CARD).first).to_be_visible()
