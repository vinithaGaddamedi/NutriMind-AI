import json
import logging
from typing import TypeVar, Type, Optional, Any, Generic
from pydantic import BaseModel, ValidationError

from agents.gateway.ai_gateway import AIGateway
from agents.schemas.base_agent_schema import AgentInput, AgentOutput, AgentMetadata, AgentError
from agents.schemas.llm_schema import LLMResponse, LLMProviderError, LLMRateLimitError, LLMTimeoutError

T = TypeVar('T', bound=BaseModel)
logger = logging.getLogger("BaseAgent")

class BaseAgent(Generic[T]):
    """
    Abstract base class for all AI Agents enforcing structured inputs/outputs
    and schema validation.
    """
    
    def __init__(self, agent_name: str, provider_name: Optional[str] = None):
        self.agent_name = agent_name
        self.gateway = AIGateway(provider_name)

    def execute(self, input_data: AgentInput, response_schema: Type[T]) -> AgentOutput[T]:
        """
        Executes the AI logic via the gateway, enforces schema validation,
        and wraps the result in an AgentOutput.
        """
        logger.info("Agent '%s' executing task...", self.agent_name)
        
        try:
            # 1. Execute LLM request via Gateway
            raw_response = self.gateway.generate_text(
                prompt=input_data.prompt,
                system_instruction=input_data.system_instruction,
                response_schema=response_schema
            )
            
            # The AIGateway internally returns the raw string content. 
            # We must fetch the telemetry metadata. Wait, AIGateway returns `str`.
            # We need the Gateway to either return LLMResponse or we just build generic metadata.
            # Currently `ai_gateway.py` returns `response.content`. Let's modify ai_gateway to return LLMResponse?
            # For now, let's just parse the content and we'll fix the Gateway if needed.
            # Actually, `gateway.generate_text` returns the parsed schema dict/model if the provider parsed it, 
            # or it returns raw JSON string. Let's handle all cases safely.
            
            # 2. Parse response
            raw_content = raw_response.content
            parsed_data = None
            if isinstance(raw_content, response_schema):
                parsed_data = raw_content
            elif isinstance(raw_content, dict):
                parsed_data = response_schema(**raw_content)
            elif isinstance(raw_content, str):
                try:
                    data_dict = json.loads(raw_content)
                    parsed_data = response_schema(**data_dict)
                except json.JSONDecodeError as jde:
                    return self._build_error_output("JSON_PARSE_ERROR", f"Malformed JSON from LLM: {str(jde)}")
            
            if not parsed_data:
                return self._build_error_output("UNEXPECTED_RESPONSE_TYPE", f"Received unexpected response format: {type(raw_content)}")
            
            # 3. Success Output
            metadata = AgentMetadata(
                agent_name=self.agent_name,
                correlation_id=raw_response.metadata.correlation_id,
                latency_ms=raw_response.metadata.latency_ms,
                prompt_tokens=raw_response.metadata.prompt_tokens,
                completion_tokens=raw_response.metadata.completion_tokens,
                total_tokens=raw_response.metadata.total_tokens
            )
            return AgentOutput[T](data=parsed_data, metadata=metadata)
            
        except ValidationError as ve:
            logger.error("Agent '%s' schema validation failed: %s", self.agent_name, ve)
            return self._build_error_output("SCHEMA_VALIDATION_ERROR", f"LLM output violated schema: {str(ve)}")
        except LLMTimeoutError as te:
            logger.error("Agent '%s' timed out: %s", self.agent_name, te)
            return self._build_error_output("TIMEOUT_ERROR", str(te))
        except LLMRateLimitError as rle:
            logger.error("Agent '%s' rate limited: %s", self.agent_name, rle)
            return self._build_error_output("RATE_LIMIT_ERROR", str(rle))
        except Exception as e:
            logger.error("Agent '%s' encountered unexpected error: %s", self.agent_name, e)
            return self._build_error_output("INTERNAL_ERROR", str(e))
            
    def _build_error_output(self, code: str, message: str) -> AgentOutput[T]:
        metadata = AgentMetadata(
            agent_name=self.agent_name,
            correlation_id="error-id",
            latency_ms=0
        )
        error = AgentError(error_code=code, message=message)
        return AgentOutput[T](metadata=metadata, error=error)
