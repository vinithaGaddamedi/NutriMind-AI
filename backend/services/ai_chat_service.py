import json
from google import genai
from google.genai import types
from typing import List, Dict
from backend.schemas.chat import ChatMessage

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
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.tools = [get_user_preferences, get_pantry, calculate_nutrition]

    def process_message(self, messages: List[ChatMessage]) -> str:
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
