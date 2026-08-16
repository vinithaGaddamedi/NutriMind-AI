from pydantic import BaseModel, Field
from typing import List, Dict, Any

class SeverityCoverage(BaseModel):
    requirement_coverage: float = Field(..., description="Percentage 0.0 to 100.0 based on trace + execution success")
    risk_coverage: float = Field(...)
    automation_coverage: float = Field(...)
    ai_behavior_coverage: float = Field(...)
    golden_coverage: float = Field(...)

class CoverageMetricsBreakdown(BaseModel):
    critical: SeverityCoverage
    high: SeverityCoverage
    medium: SeverityCoverage
    low: SeverityCoverage
    overall: SeverityCoverage

class CoverageGapRecommendation(BaseModel):
    gap_type: str = Field(description="e.g. MISSING_AI_BEHAVIOR_TEST, MISSING_AUTOMATION, UNEXECUTED_TEST")
    target_id: str = Field(description="The ID of the requirement or risk needing coverage")
    recommendation: str = Field(description="Actionable advice on what exact test to create")
    priority: str = Field(description="Critical, High, Medium, Low")

class CoverageReport(BaseModel):
    metrics: CoverageMetricsBreakdown
    recommendations: List[CoverageGapRecommendation]
