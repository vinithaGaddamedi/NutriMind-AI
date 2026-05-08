from ui_tests.pages.base_page import BasePage
import re

class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.add_to_cart_buttons = page.locator("button:has-text('Add to Cart')")

    def add_first_product_to_cart(self):
        self.add_to_cart_buttons.first.click()
        # Handle the JS alert
        self.page.on("dialog", lambda dialog: dialog.accept())
