import os
import json
import uuid
import logging
from google import genai
from google.genai import types
from google.genai.errors import APIError
from typing import List, Dict, Optional
from application.backend.schemas.chat import ChatMessage, UserContext

logger = logging.getLogger("AIChatService")

def get_user_preferences() -> str:
    """Mock database fetch for preferences."""
    return json.dumps({"diet": "vegetarian", "allergies": ["peanut"]})

def get_pantry() -> str:
    """Mock database fetch for pantry inventory."""
    return json.dumps(["rice", "beans", "spinach", "tofu"])

def calculate_nutrition(meal_plan: str) -> str:
    """Mock deterministic nutrition calculator."""
    return json.dumps({"calories": 1800, "protein": "75g"})

class AIChatService:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        self.tools = [get_user_preferences, get_pantry, calculate_nutrition]
        
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "default_placeholder":
            logger.warning("GEMINI_API_KEY not configured. Chatbot will run in offline fallback mode.")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)

    def process_message(self, messages: List[ChatMessage]) -> str:
        if not self.client:
            return "Fallback response: Gemini client is not configured."
            
        # Convert history to Gemini format
        contents = []
        for msg in messages:
            role = "user" if msg.role == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg.content)]))

        system_instruction = (
            "You are NutriMind, an expert dietary assistant. "
            "Use the provided tools to lookup user preferences and calculate nutrition deterministically. "
            "Do NOT fabricate allergies, pantry items, or nutritional facts. "
            "Always respect conversational history."
        )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=self.tools,
            temperature=0.2
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=config
        )
        return response.text

    def generate_chat_response(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        user_context: Optional[UserContext] = None
    ) -> Dict[str, str]:
        cid = conversation_id or f"conv-{uuid.uuid4().hex[:8]}"
        context_str = ""
        if user_context:
            context_items = []
            if user_context.dietary_preferences:
                context_items.append(f"Dietary Preferences: {', '.join(user_context.dietary_preferences)}")
            if user_context.allergies:
                context_items.append(f"Allergies: {', '.join(user_context.allergies)}")
            if user_context.pantry_items:
                context_items.append(f"Pantry Items: {', '.join(user_context.pantry_items)}")
            if user_context.budget:
                context_items.append(f"Budget: ${user_context.budget}")
            if user_context.goals:
                context_items.append(f"Goals: {', '.join(user_context.goals)}")
            
            if context_items:
                context_str = f"\n[User Context: {'; '.join(context_items)}]\n"

        prompt = f"{context_str}User Message: {message}"

        if not self.client:
            msg_clean = message.lower().strip()
            
            if any(w in msg_clean for w in ["hi", "hello", "hey", "hola"]):
                fallback_text = (
                    "🥗 **NutriMind AI Assistant**\n\n"
                    "Hello! I am your NutriMind AI nutritional assistant. I can help you with:\n"
                    "- **Meal Planning:** Build customized 7-day plans matching calories and macros.\n"
                    "- **Smart Pantry Scanner:** Search barcode information and track inventory.\n"
                    "- **Grocery Budgeting:** Deduct pantry stock and compare store prices.\n\n"
                    "How can I assist you with your health goals today?"
                )
            elif any(w in msg_clean for w in ["meal", "dinner", "vegetarian", "vegan", "protein", "keto", "calorie"]):
                fallback_text = (
                    "🥗 **NutriMind AI Assistant**\n\n"
                    "Here is a recommended **High-Protein Vegetarian Dinner**:\n\n"
                    "### 🍲 Quinoa & Chickpea Tofu Bowl\n"
                    "- **Ingredients:** 1/2 cup quinoa, 1/2 cup chickpeas, 150g tofu, broccoli.\n"
                    "- **Metrics:** Calories: ~540 kcal, Protein: 28g."
                )
            elif any(w in msg_clean for w in ["pantry", "allergy", "peanut", "scan"]):
                fallback_text = (
                    "🥗 **NutriMind AI Assistant**\n\n"
                    "### 🚫 Allergen & Pantry Inventory Guidance\n"
                    "- **Safety Gate:** I scan ingredients to flag specified allergens (such as *Peanuts*).\n"
                    "- **Inventory:** Items in stock in your pantry are subtracted from your grocery list."
                )
            else:
                fallback_text = (
                    "🥗 **NutriMind AI Assistant**\n\n"
                    "I am here to help you plan your meals, scan your pantry, and compare store prices."
                )

            return {
                "response": fallback_text,
                "conversation_id": cid,
                "model": "fallback-demo"
            }

        try:
            config = types.GenerateContentConfig(
                temperature=0.3,
                system_instruction="You are NutriMind, an expert dietary assistant."
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )
            text_output = response.text.strip() if response and response.text else "I can help you with your meal plan!"
            return {
                "response": text_output,
                "conversation_id": cid,
                "model": self.model_name
            }
        except APIError as api_err:
            logger.error("Gemini API Error in chat route: %s", str(api_err))
            return {
                "response": "I'm currently experiencing high traffic or a temporary service disruption. Please try asking your question again in a moment.",
                "conversation_id": cid,
                "model": self.model_name
            }
        except TimeoutError as timeout_err:
            logger.error("Timeout Error in chat route: %s", str(timeout_err))
            return {
                "response": "Your request took too long to process. Please try asking a shorter question or checking your connection.",
                "conversation_id": cid,
                "model": self.model_name
            }
        except Exception as err:
            logger.error("Unexpected error in chat route: %s", str(err))
            return {
                "response": "⚠️ An unexpected error occurred while processing your request. Please try again.",
                "conversation_id": cid,
                "model": self.model_name
            }

# Instantiate singleton service
chat_service = AIChatService()

