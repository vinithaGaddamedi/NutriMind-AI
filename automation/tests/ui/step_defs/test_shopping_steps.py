import pytest
from pytest_bdd import scenario, given, when, then
import csv
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from automation.pages.shopping_pages import LoginPage, MealPlannerPage, PantryPage, ShoppingPage, CartPage

def get_test_data():
    csv_path = os.path.join(os.path.dirname(__file__), '../../../../test_data/test_data.csv')
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

@pytest.mark.parametrize("user_data", get_test_data())
@scenario('../features/shopping.feature', 'Generate meal plan and checkout using CSV data')
def test_shopping_flow(user_data):
    # Parameterized tests will run this scenario multiple times for each row in the CSV
    pass

@given('I log in with CSV user data')
def login(page, user_data):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(user_data["username"])

@when('I generate a weekly meal plan')
def generate_meal_plan(page, user_data):
    meal_page = MealPlannerPage(page)
    meal_page.fill_profile_and_generate(user_data["age"], user_data["weight"], user_data["height"])

@when('I check my pantry for available items')
def check_pantry(page):
    pantry_page = PantryPage(page)
    pantry_page.mark_in_stock_and_proceed()

@when('I add remaining groceries to the cart')
def add_to_cart(page):
    shopping_page = ShoppingPage(page)
    shopping_page.add_all_to_cart()

@then('I successfully checkout and track my order')
def checkout(page):
    cart_page = CartPage(page)
    cart_page.checkout()
    cart_page.verify_order_and_track()
