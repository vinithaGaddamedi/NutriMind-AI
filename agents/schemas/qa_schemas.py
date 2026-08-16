from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class FailureClassification(str, Enum):
    LOCATOR_FAILURE = "LOCATOR_FAILURE"
    ASSERTION_FAILURE = "ASSERTION_FAILURE"
    APPLICATION_DEFECT = "APPLICATION_DEFECT"
    API_FAILURE = "API_FAILURE"
    TEST_DATA_FAILURE = "TEST_DATA_FAILURE"
    ENVIRONMENT_FAILURE = "ENVIRONMENT_FAILURE"
    TIMEOUT = "TIMEOUT"
    NETWORK_FAILURE = "NETWORK_FAILURE"
    FLAKY_TEST = "FLAKY_TEST"
    UNKNOWN = "UNKNOWN"
    NEEDS_MORE_EVIDENCE = "NEEDS_MORE_EVIDENCE"

class RiskModel(BaseModel):
    risk_id: str = Field(..., description="Unique identifier for the risk (e.g., RSK-001). Use 'NEEDS_CLARIFICATION' if unknown.")
    requirement_id: str = Field(..., description="The Jira story ID or requirement ID. Use 'NEEDS_CLARIFICATION' if unknown.")
    description: str = Field(description="Description of the risk")
    category: str = Field(description="Risk category e.g. functional, integration, security, data, performance, accessibility, AI/LLM, privacy, business-critical")
    severity: str = Field(description="Severity of the risk: Critical, High, Medium, Low")
    probability: str = Field(description="Probability of occurrence: High, Medium, Low")
    priority: str = Field(description="Priority level: P0, P1, P2, P3")
    business_impact: str = Field(description="Impact on the business if the risk occurs")
    technical_impact: str = Field(description="Impact on the technical system if the risk occurs")
    recommended_test_types: List[str] = Field(description="List of recommended test types to cover this risk (e.g., API, UI, AI behavior)")

class RiskAnalysis(BaseModel):
    story_id: str = Field(..., description="The Jira story ID these risks apply to. Use 'NEEDS_CLARIFICATION' if unknown.")
    risks: List[RiskModel] = Field(description="List of identified risks")

class TestScenario(BaseModel):
    scenario_id: str = Field(..., description="Unique identifier for the scenario (e.g., TS-MEAL-101-001). Use 'NEEDS_CLARIFICATION' if unknown.")
    requirement_id: str = Field(..., description="The Jira story ID or requirement ID. Use 'NEEDS_CLARIFICATION' if unknown.")
    risk_id: str = Field(..., description="The ID of the associated risk, if any. Use 'NONE' if no specific risk.")
    title: str = Field(description="Title of the test scenario")
    description: str = Field(description="Description of the scenario to be tested")
    test_type: str = Field(description="Type of test (e.g., positive, negative, boundary, validation, integration, API, UI, accessibility, security, AI behavior, hallucination, prompt injection, conversation/memory, error handling, regression)")
    priority: str = Field(description="Priority: Critical, High, Medium, Low")
    preconditions: List[str] = Field(default_factory=list, description="Preconditions required before testing")
    test_data: str = Field(description="Required test data for the scenario")
    expected_behavior: str = Field(description="Expected behavior or result of the scenario")
    automation_candidate: bool = Field(description="Whether this scenario is a candidate for automation")
    golden_candidate: bool = Field(default=False, description="Whether this scenario is a candidate for a golden dataset")

class ScenariosListModel(BaseModel):
    # Wrapping for when multiple scenarios are generated
    scenarios: List[TestScenario] = Field(description="List of generated test scenarios")

class ReviewAnalysis(BaseModel):
    is_approved: bool = Field(description="Whether the code meets enterprise standards")
    score: float = Field(description="Code quality score between 0.0 and 1.0")
    comments: List[str] = Field(default_factory=list, description="Review comments")
    suggested_fixes: List[str] = Field(default_factory=list, description="Actionable fix suggestions")

class FailureAnalysis(BaseModel):
    test_case_id: str = Field(..., description="The ID of the failing test. Use 'NEEDS_CLARIFICATION' if unknown.")
    failure_type: FailureClassification = Field(default=FailureClassification.UNKNOWN, description="Classification of the failure type")
    root_cause: str = Field(description="Detailed explanation of the root cause of the failure")
    evidence: str = Field(description="Extract from logs, stack trace, DOM snippet, or screenshot ref")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    recommended_action: str = Field(description="Actionable recommendation to fix the issue")
    requires_human_review: bool = Field(description="Whether the failure requires human review before action is taken")
