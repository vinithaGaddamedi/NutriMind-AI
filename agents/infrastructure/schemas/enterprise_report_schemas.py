from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class ExecutiveSummary(BaseModel):
    overall_quality: str = Field(description="PASS, FAIL, or WARN")
    functional_pass_rate: float = Field(description="Percentage of functional tests passed")
    api_pass_rate: float = Field(description="Percentage of API tests passed")
    automation_pass_rate: float = Field(description="Percentage of automated tests passed")
    ai_quality_score: float = Field(description="Aggregated average of DeepEval metrics")
    security_pass_rate: float = Field(description="Percentage of security tests passed")
    coverage_percentage: float = Field(description="Aggregated requirement traceability coverage")
    critical_issues_count: int = Field(description="Total count of P0/P1 defects and security failures")

class ConsolidatedReport(BaseModel):
    executive_summary: ExecutiveSummary
    
    # Raw Subsystem Data (Optional depending on availability in CI run)
    traceability_data: Optional[Dict[str, Any]] = None
    coverage_data: Optional[Dict[str, Any]] = None
    quality_gate_decision: Optional[Dict[str, Any]] = None
    ai_observability: Optional[Dict[str, Any]] = None
    failures_and_rca: Optional[List[Dict[str, Any]]] = None
    self_healing_proposals: Optional[List[Dict[str, Any]]] = None
