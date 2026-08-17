from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class TraceNode(BaseModel):
    id: str = Field(description="The unique identifier for the node (e.g., REQ-123, TS-01, BUG-42)")
    type: str = Field(description="The type of node (Requirement, Risk, TestScenario, AutomationTest, Golden, Execution, Defect)")
    severity: str = Field(default="Medium", description="Severity or Priority (Critical, High, Medium, Low)")
    linked_ids: List[str] = Field(default_factory=list, description="IDs of linked downstream or upstream items")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context")

class CoverageMetrics(BaseModel):
    critical_coverage_percent: float
    high_coverage_percent: float
    medium_coverage_percent: float
    low_coverage_percent: float
    total_coverage_percent: float

class TraceabilityGaps(BaseModel):
    requirements_without_tests: List[str] = Field(default_factory=list)
    high_risk_without_automation: List[str] = Field(default_factory=list)
    tests_without_requirements: List[str] = Field(default_factory=list)
    goldens_without_requirements: List[str] = Field(default_factory=list)
    automation_without_test_cases: List[str] = Field(default_factory=list)
    defects_without_test_coverage: List[str] = Field(default_factory=list)

class TraceabilityReport(BaseModel):
    nodes: List[TraceNode] = Field(description="The graph of traced nodes")
    metrics: CoverageMetrics = Field(description="Coverage percentage broken down by priority")
    gaps: TraceabilityGaps = Field(description="Detected traceability gaps")
