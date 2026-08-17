from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any, Dict

T = TypeVar('T', bound=BaseModel)

class AgentMetadata(BaseModel):
    agent_name: str = Field(description="Name of the agent that executed the task")
    correlation_id: str = Field(description="Unique correlation ID for tracing the request")
    latency_ms: int = Field(description="Execution latency in milliseconds")
    prompt_tokens: Optional[int] = Field(default=None, description="Number of tokens used in prompt")
    completion_tokens: Optional[int] = Field(default=None, description="Number of tokens generated")
    total_tokens: Optional[int] = Field(default=None, description="Total tokens used for the request")

class AgentError(BaseModel):
    error_code: str = Field(description="Error classification code")
    message: str = Field(description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Optional diagnostic details")

class AgentInput(BaseModel):
    prompt: str = Field(description="The primary user prompt or context to evaluate")
    system_instruction: Optional[str] = Field(default=None, description="The system instruction defining agent behavior")
    
class AgentOutput(BaseModel, Generic[T]):
    data: Optional[T] = Field(default=None, description="The structured schema response from the LLM")
    metadata: AgentMetadata = Field(description="Telemetry and tracing metadata")
    error: Optional[AgentError] = Field(default=None, description="Error information if the execution failed")
    
    @property
    def is_success(self) -> bool:
        return self.error is None and self.data is not None
