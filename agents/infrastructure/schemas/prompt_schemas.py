from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime

class PromptStatus(str, Enum):
    DRAFT = "DRAFT"
    PROMOTED = "PROMOTED"
    REJECTED = "REJECTED"

class PromptVersion(BaseModel):
    prompt_id: str = Field(description="Unique identifier for the prompt (e.g. failure_agent_v1)")
    version: str = Field(description="Semantic version string (e.g. 1.0.0)")
    description: str = Field(description="Description of what changed in this version")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    owner: str = Field(description="The engineer or agent who authored the prompt")
    status: PromptStatus = Field(default=PromptStatus.DRAFT)
    prompt_text: str = Field(description="The actual system instruction string")

class QualityMetrics(BaseModel):
    relevance: float = Field(0.0)
    faithfulness: float = Field(0.0)
    safety: float = Field(0.0)
    constraint_compliance: float = Field(0.0)
    hallucination: float = Field(0.0)
    latency_ms: int = Field(0)

class PromptRegressionReport(BaseModel):
    baseline_id: str
    candidate_id: str
    is_promoted: bool = Field(description="Whether the candidate prompt passed regression and was promoted")
    rejection_reasons: List[str] = Field(default_factory=list)
    baseline_metrics: QualityMetrics
    candidate_metrics: QualityMetrics
