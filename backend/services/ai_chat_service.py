import os
import uuid
import logging
from typing import Optional, Dict, Any
from google import genai
from google.genai import types
from google.genai.errors import APIError

from schemas.chat import UserContext

logger = logging.getLogger("NutriMindAIChatService")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

NUTRIMIND_SYSTEM_PROMPT = """You are NutriMind AI, an intelligent, friendly, and expert nutritional assistant and smart grocery advisor.
Your expertise covers:
1. Personalized weekly meal planning based on calorie, macro, and dietary goals (vegetarian, keto, high-protein, etc.).
2. Smart pantry inventory management, expiry tracking, and barcode scanning advice.
3. Budget-optimized grocery lists and price comparisons across stores.
4. Recipe ideas utilizing items currently in the user's pantry.

Always keep your tone encouraging, concise, clear, and actionable.
Format your responses using clean Markdown formatting (bullet points, bold text, headers where appropriate).
If the user provides context (such as diet preference or fitness goal), tailor your recommendations strictly to their profile."""

class AIChatService:
    def __init__(self, model_name: Optional[str] = None, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        if not self.api_key or self.api_key == "your_key_here":
            logger.warning("GOOGLE_API_KEY not configured. AIChatService running in fallback demonstration mode.")
            self.client = None
        else:
            masked = f"{self.api_key[:4]}...{self.api_key[-4:]}" if len(self.api_key) > 8 else "***"
            logger.info("AIChatService initialized with Gemini model '%s' and key [%s]", self.model_name, masked)
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as err:
                logger.error("Failed to initialize genai.Client in backend: %s", str(err))
                self.client = None

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
            
            # 1. Greetings
            if any(w in msg_clean for w in ["hi", "hello", "hey", "hola"]):
                fallback_text = (
                    "🥗 **NutriMind AI Assistant**\n\n"
                    "Hello! I am your NutriMind AI nutritional assistant. I can help you with:\n"
                    "- **Meal Planning:** Build customized 7-day single or family plans matching calories and macros.\n"
                    "- **Smart Pantry Scanner:** Search barcode information and track ingredient inventory.\n"
                    "- **Grocery Budgeting:** Auto-deduct pantry inventory and compare prices between Walmart, Target, and Kroger.\n\n"
                    "How can I assist you with your health goals today?"
                )
            
            # 2. Meal Planning / Vegetarian / Protein / Keto
            elif any(w in msg_clean for w in ["meal", "dinner", "vegetarian", "vegan", "protein", "keto", "calorie"]):
                fallback_text = (
                    "🥗 **NutriMind AI Assistant**\n\n"
                    "Here is a recommended **High-Protein Vegetarian Dinner** matching your NutriMind preferences:\n\n"
                    "### 🍲 Quinoa & Chickpea Tofu Bowl\n"
                    "- **Ingredients:** 1/2 cup cooked quinoa, 1/2 cup roasted chickpeas, 150g grilled tofu, steamed broccoli, tahini dressing.\n"
                    "- **Nutritional Metrics:**\n"
                    "  - **Calories:** ~540 kcal\n"
                    "  - **Protein:** 28g 💪\n"
                    "  - **Fiber:** 11g 🌾\n"
                    "  - **Healthy Fats:** 16g 🥑\n\n"
                    "*Tip:* This recipe combines quinoa and chickpeas to build a complete essential amino acid profile. Let me know if you would like me to add these items to your **Smart Cart**!"
                )
            
            # 3. Pantry / Allergy / Scanner
            elif any(w in msg_clean for w in ["pantry", "allergy", "peanut", "scan", "barcode"]):
                fallback_text = (
                    "🥗 **NutriMind AI Assistant**\n\n"
                    "### 🚫 Allergen & Pantry Inventory Guidance\n"
                    "- **Safety Gate:** I check all recipe ingredients to flag specified allergens (such as *Peanuts*). Prohibited ingredients are automatically filtered out from your cart suggestions.\n"
                    "- **Inventory Deduction:** Items marked as **In Stock** in your **Pantry Scanner** are automatically subtracted from your weekly shopping list to avoid food waste.\n\n"
                    "Try using the barcode scanning camera on the **Pantry** tab to scan barcodes directly!"
                )
            
            # 4. Default Fallback
            else:
                fallback_text = (
                    "🥗 **NutriMind AI Assistant**\n\n"
                    "Thank you for your message! I am here to help you plan your weekly meals, track your pantry inventory, and optimize your grocery list for budget and freshness.\n\n"
                    "Feel free to ask questions like:\n"
                    "1. *\"Suggest a high-protein vegetarian dinner plan\"*\n"
                    "2. *\"How does the Smart Pantry deduction work?\"*\n"
                    "3. *\"Show me a grocery budget comparison\"*"
                )

            return {
                "response": fallback_text,
                "conversation_id": cid,
                "model": "fallback-demo"
            }

        try:
            logger.info("Sending chat query for conversation %s to Gemini model '%s'", cid, self.model_name)
            config = types.GenerateContentConfig(
                temperature=0.3,
                system_instruction=NUTRIMIND_SYSTEM_PROMPT
            )

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            text_output = response.text.strip() if response and hasattr(response, 'text') and response.text else "I am here to help with your NutriMind meal and grocery planning!"

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

# Global backend service singleton
chat_service = AIChatService()
