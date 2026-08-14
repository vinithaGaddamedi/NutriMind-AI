import pytest
import allure
from playwright.sync_api import expect

BASE_URL = "http://localhost:5173"

@allure.feature("AI Chatbot UI")
@allure.story("Interactive Chat Widget Flow")
def test_chat_widget_toggle_and_send_message(page):
    page.goto(BASE_URL)

    # 1. Verify floating trigger button exists and click it
    toggle_btn = page.locator("#nutrimind-chat-toggle")
    expect(toggle_btn).to_be_visible()
    toggle_btn.click()

    # 2. Verify chat window opens with header
    chat_panel = page.locator("div[role='region'][aria-label='NutriMind AI Chat Window']")
    expect(chat_panel).to_be_visible()
    expect(page.locator("h4:has-text('NutriMind AI Assistant')")).to_be_visible()

    # 3. Type user message and send
    chat_input = page.locator("#nutrimind-chat-input")
    send_btn = page.locator("#nutrimind-chat-send")
    
    expect(chat_input).to_be_visible()
    chat_input.fill("Give me a 1-day high protein meal plan.")
    send_btn.click()

    # 4. Verify user message appears in chat log
    user_msg_bubble = page.locator("div.chat-message.user .message-content")
    expect(user_msg_bubble.last).to_contain_text("Give me a 1-day high protein meal plan.")

    # 5. Verify AI response bubble appears
    ai_msg_bubble = page.locator("div.chat-message.ai .message-content")
    expect(ai_msg_bubble.last).to_be_visible(timeout=10000)

    # 6. Test Clear Chat button functionality
    clear_btn = page.locator("#nutrimind-chat-clear")
    clear_btn.click()

    # Verify messages reset to default welcome message
    expect(page.locator("div.chat-message.user")).to_have_count(0)
