from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class QualityGateDecision(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"

class QualityGateInput(BaseModel):
    critical_functional_pass_rate: float = Field(..., description="Percentage of critical functional tests passed")
    critical_constraint_pass_rate: float = Field(..., description="Percentage of deterministic constraint validations passed")
    ai_safety_score: float = Field(..., description="Average DeepEval safety score")
    ai_relevance_score: float = Field(..., description="Average DeepEval relevance score")
    ai_faithfulness_score: float = Field(..., description="Average DeepEval faithfulness score")
    ai_hallucination_rate: float = Field(..., description="Percentage of responses containing hallucination")
    security_critical_failures: int = Field(..., description="Count of critical security test failures")
    p0_p1_defects: int = Field(..., description="Count of open P0/P1 defects linked to the build")

class QualityGateReport(BaseModel):
    decision: QualityGateDecision = Field(description="The final gate decision")
    violations: List[str] = Field(default_factory=list, description="List of thresholds that were breached")
    warnings: List[str] = Field(default_factory=list, description="List of non-critical thresholds that were soft-breached")
    input_metrics: QualityGateInput = Field(description="The original metrics evaluated")
