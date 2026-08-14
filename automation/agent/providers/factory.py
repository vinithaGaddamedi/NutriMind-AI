import os
import logging
from typing import Optional
from agent.providers.base_provider import AIProvider
from agent.providers.gemini_provider import GeminiProvider

logger = logging.getLogger("AIProviderFactory")

class AIProviderFactory:
    """
    Factory pattern to dynamically manage and instantiate AI providers.
    """

    @staticmethod
    def get_provider(provider_type: Optional[str] = None) -> AIProvider:
        selected_provider = (provider_type or os.getenv("AI_PROVIDER", "gemini")).lower()

        if selected_provider == "gemini":
            return GeminiProvider()

        logger.info("Provider '%s' requested. Defaulting to GeminiProvider.", selected_provider)
        return GeminiProvider()
