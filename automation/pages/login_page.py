from automation.pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.locator("input[placeholder='Enter your username']")
        self.login_button = page.locator("button:has-text('Login')")

    def login(self, username):
        self.navigate("http://localhost:5173/login") # Default Vite port
        self.username_input.fill(username)
        self.login_button.click()
