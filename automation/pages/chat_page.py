from playwright.sync_api import Page, expect

class ChatPage:
    def __init__(self, page: Page):
        self.page = page
        self.toggle_btn = page.locator("#nutrimind-chat-toggle")
        self.chat_panel = page.locator("div[role='region'][aria-label='NutriMind AI Chat Window']")
        self.chat_input = page.locator("#nutrimind-chat-input")
        self.send_btn = page.locator("#nutrimind-chat-send")
        self.clear_btn = page.locator("#nutrimind-chat-clear")
        self.user_messages = page.locator("div.chat-message.user .message-content")
        self.ai_messages = page.locator("div.chat-message.ai .message-content")

    def open_chat(self):
        expect(self.toggle_btn).to_be_visible()
        self.toggle_btn.click()
        expect(self.chat_panel).to_be_visible()

    def send_message(self, text: str):
        expect(self.chat_input).to_be_visible()
        self.chat_input.fill(text)
        self.send_btn.click()

    def verify_user_message(self, expected_text: str):
        expect(self.user_messages.last).to_contain_text(expected_text)

    def wait_for_ai_response(self, timeout: int = 15000):
        expect(self.ai_messages.last).to_be_visible(timeout=timeout)

    def verify_ai_response_contains(self, expected_text: str, timeout: int = 15000):
        expect(self.ai_messages.last).to_contain_text(expected_text, timeout=timeout)

    def clear_chat(self):
        self.clear_btn.click()
        expect(self.user_messages).to_have_count(0)
