from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime

class AIObservabilityRecord(BaseModel):
    agent: str = Field(description="Name of the agent executing the task")
    model: str = Field(description="Name of the underlying LLM (e.g. gemini-1.5-pro)")
    prompt_version: str = Field(description="The semantic version of the prompt used")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    correlation_id: str = Field(description="Unique ID tying this execution to a test run or UI interaction")
    latency_ms: int = Field(description="Execution latency in milliseconds")
    input_tokens: Optional[int] = Field(default=None)
    output_tokens: Optional[int] = Field(default=None)
    evaluation_score: Optional[float] = Field(default=None, description="Average DeepEval score, if evaluated")
    status: str = Field(description="SUCCESS, FAILURE, TIMEOUT")
    error_type: Optional[str] = Field(default=None, description="The exception class name, if status is FAILURE")

class AgentPerformance(BaseModel):
    total_invocations: int = Field(0)
    success_rate: float = Field(0.0)
    average_latency_ms: float = Field(0.0)
    average_evaluation_score: float = Field(0.0)

class AIObservabilitySummary(BaseModel):
    overall_success_rate: float = Field(0.0)
    overall_failure_rate: float = Field(0.0)
    average_latency_ms: float = Field(0.0)
    agent_performance: Dict[str, AgentPerformance] = Field(default_factory=dict)
    model_usage: Dict[str, int] = Field(default_factory=dict, description="Count of invocations per model")
    prompt_version_performance: Dict[str, float] = Field(default_factory=dict, description="Average eval score per prompt version")
