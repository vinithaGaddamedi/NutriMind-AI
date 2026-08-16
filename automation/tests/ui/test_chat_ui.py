import pytest
import allure
from automation.pages.chat_page import ChatPage

BASE_URL = "http://localhost:5173"

@allure.feature("AI Chatbot UI")
@allure.story("Interactive Chat Widget Flow")
def test_chat_widget_meal_planning(page):
    page.goto(BASE_URL)
    chat = ChatPage(page)

    chat.open_chat()
    
    msg = "Give me a 1-day high protein meal plan."
    chat.send_message(msg)
    chat.verify_user_message(msg)
    
    # AI should respond eventually
    chat.wait_for_ai_response()
    
    # Test Clear Chat functionality
    chat.clear_chat()

@allure.feature("AI Chatbot UI")
@allure.story("Pantry Context Queries")
def test_chat_widget_pantry_query(page):
    page.goto(BASE_URL)
    chat = ChatPage(page)

    chat.open_chat()
    
    msg = "What recipes can I make with peanut?"
    chat.send_message(msg)
    chat.verify_user_message(msg)
    
    # The backend handles pantry/peanut/allergy keywords with a safe fallback response for now if API not ready
    chat.wait_for_ai_response()
