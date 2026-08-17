import os
import time
import logging
from typing import Optional, Any
from agents.providers.factory import AIProviderFactory
from agents.infrastructure.schemas.llm_schema import LLMResponse, LLMProviderError, LLMRateLimitError, LLMTimeoutError
from google.genai.errors import APIError

logger = logging.getLogger("AIGateway")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

class AIGateway:
    """
    Centralized AI Gateway providing resiliency (retries, timeouts) 
    and observability (structured telemetry logging) for LLM interactions.
    """
    def __init__(self, provider_name: Optional[str] = None):
        self.provider = AIProviderFactory.get_provider(provider_name)
        self.max_retries = int(os.getenv("LLM_MAX_RETRIES", "3"))
        self.base_delay = int(os.getenv("LLM_RETRY_DELAY", "2"))

    def generate_text(self, prompt: str, system_instruction: Optional[str] = None, response_schema: Optional[Any] = None) -> LLMResponse:
        """
        Executes a prompt through the LLM Provider with exponential backoff and telemetry logging.
        Returns the content (string or parsed schema object) from the response.
        """
        retries = 0
        while retries <= self.max_retries:
            try:
                # The provider returns an LLMResponse which includes metadata
                response: LLMResponse = self.provider.generate_text(
                    prompt=prompt,
                    system_instruction=system_instruction,
                    response_schema=response_schema
                )
                
                # Structured Telemetry Logging
                meta = response.metadata
                logger.info(
                    "AIGateway Request Successful | CorrelationID: %s | Latency: %dms | Tokens (P/C/T): %s/%s/%s",
                    meta.correlation_id, meta.latency_ms,
                    meta.prompt_tokens, meta.completion_tokens, meta.total_tokens
                )
                
                return response
                
            except APIError as api_err:
                err_code = getattr(api_err, 'code', 500)
                err_msg = str(api_err).lower()
                
                # Classify Error
                if err_code in [429] or "quota" in err_msg or "rate limit" in err_msg:
                    mapped_err = LLMRateLimitError(f"Rate limited by provider: {api_err}")
                elif err_code in [503, 504] or "timeout" in err_msg or "deadline" in err_msg:
                    mapped_err = LLMTimeoutError(f"Provider timed out: {api_err}")
                else:
                    mapped_err = LLMProviderError(f"Provider error: {api_err}")
                
                if isinstance(mapped_err, (LLMRateLimitError, LLMTimeoutError)) and retries < self.max_retries:
                    delay = self.base_delay * (2 ** retries)
                    logger.warning("AIGateway caught transient error: %s. Retrying in %ds (Attempt %d/%d)", 
                                   mapped_err, delay, retries + 1, self.max_retries)
                    time.sleep(delay)
                    retries += 1
                else:
                    logger.error("AIGateway exhausted retries or hit fatal error: %s", mapped_err)
                    raise mapped_err
            except Exception as e:
                logger.error("AIGateway encountered unexpected error: %s", e)
                raise LLMProviderError(f"Unexpected error: {e}")
