class LoginLocators:
    USERNAME_INPUT = "input[id='username']"
    LOGIN_BUTTON = "button:has-text('Login')"

class MealLocators:
    MEAL_MENU = "h3:has-text('AI Meal Planner')"
    HEADER = "h2"
    NAME_INPUT = "input[name='name']"
    AGE_INPUT = "input[name='age']"
    WEIGHT_INPUT = "input[name='weight']"
    HEIGHT_INPUT = "input[name='height']"
    GENERATE_BTN = "button:has-text('Generate Weekly Plan')"
    DAY_HEADER = "h4:has-text('Monday')"
    PROCEED_BTN = "button:has-text('Proceed to Pantry')"

class PantryLocators:
    HEADER = "h1"
    IN_STOCK_BTN = "button:has-text('In Stock ✓')"
    SAVE_BTN = "button:has-text('Save & Proceed to Shopping')"

class ShoppingLocators:
    HEADER = "h2"
    ADD_CART_BTN = "button:has-text('Add All Checked & Checkout')"

class CartLocators:
    HEADER = "h2"
    CHECKOUT_BTN = "button:has-text('Checkout')"
    SUCCESS_HEADER = "h1"
    TRACK_BTN = "button:has-text('Track Order')"
    ORDERS_HEADER = "h1"
    ORDER_CARD = "div.glass-panel"
