import os
from typing import Optional
import re
from deepeval.models.base_model import DeepEvalBaseLLM
from google import genai

class GeminiEvalModel(DeepEvalBaseLLM):
    def __init__(self, model_name: str = "gemini-2.5-flash", api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def load_model(self):
        return self.client

    def _strip_json_markdown(self, text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.client:
            return '{"statements": ["Mocked statement"]}'
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return self._strip_json_markdown(response.text)
        except Exception as e:
            return f"Error: {str(e)}"

    async def a_generate(self, prompt: str, **kwargs) -> str:
        if not self.client:
            return '{"statements": ["Mocked statement"]}'
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return self._strip_json_markdown(response.text)
        except Exception as e:
            return f"Error: {str(e)}"

    def get_model_name(self) -> str:
        return self.model_name
