from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ManualTestCase(BaseModel):
    test_case_id: str = Field(..., description="Unique Test Case ID. Use 'NEEDS_CLARIFICATION' if unknown.")
    story_id: str = Field(..., description="Associated Story ID. Use 'NEEDS_CLARIFICATION' if unknown.")
    requirement_id: str = Field(..., description="Associated Requirement ID. Use 'NEEDS_CLARIFICATION' if unknown.")
    acceptance_criteria_id: str = Field(..., description="Associated AC ID. Use 'NEEDS_CLARIFICATION' if unknown.")
    risk_id: str = Field(..., description="Associated Risk ID. Use 'NONE' if no specific risk.")
    scenario_id: str = Field(..., description="Associated Scenario ID. Use 'NEEDS_CLARIFICATION' if unknown.")
    title: str = Field(description="Title of the test case")
    objective: str = Field(description="Objective of the test case")
    preconditions: List[str] = Field(default_factory=list, description="Preconditions required before testing")
    test_data: str = Field(description="Test data required")
    steps: List[Dict[str, str]] = Field(description="List of steps, e.g. [{'step': '...', 'expected_result': '...'}]")
    expected_result: str = Field(description="Overall expected result for the entire test case")
    priority: str = Field(description="Priority: Critical, High, Medium, Low")
    severity: str = Field(description="Severity: Critical, High, Medium, Low")
    test_type: str = Field(description="Test Type, e.g., Functional, Security, AI Behavior")
    automation_candidate: bool = Field(description="Whether this scenario is a candidate for automation")
    golden_id: str = Field(default="NONE", description="Golden ID if applicable")
    ai_specific_test: bool = Field(default=False, description="Whether this test is specifically an AI/LLM test")

class ManualTestCasesListModel(BaseModel):
    test_cases: List[ManualTestCase] = Field(description="List of generated manual test cases")

class TestDataSet(BaseModel):
    dataset_id: str = Field(..., description="Unique ID for this dataset")
    scenario_id: str = Field(..., description="Associated Scenario ID")
    description: str = Field(description="Description of what this data tests")
    positive_data: List[Dict[str, Any]] = Field(default_factory=list, description="Valid, happy-path test data")
    negative_data: List[Dict[str, Any]] = Field(default_factory=list, description="Invalid data expected to fail")
    boundary_data: List[Dict[str, Any]] = Field(default_factory=list, description="Edge cases, extremely long strings, etc.")
    security_data: List[Dict[str, Any]] = Field(default_factory=list, description="Malicious payloads (XSS, SQLi, Prompt Injection)")
    expected_validation_errors: List[str] = Field(default_factory=list, description="Expected error messages for negative data")
    pii_synthetic: bool = Field(default=True, description="Must be true. Real PII is strictly prohibited.")

class TestDataSetsListModel(BaseModel):
    datasets: List[TestDataSet] = Field(description="List of generated test datasets")

class AutomationTest(BaseModel):
    test_case_id: str = Field(..., description="Unique Test Case ID being automated. Use 'NEEDS_CLARIFICATION' if unknown.")
    story_id: str = Field(..., description="Associated Story ID.")
    requirement_id: str = Field(..., description="Associated Requirement ID.")
    scenario_id: str = Field(..., description="Associated Scenario ID.")
    code: str = Field(description="The executable test script code")
    framework: str = Field(default="playwright", description="Test framework used")

class AutomationTestListModel(BaseModel):
    tests: List[AutomationTest] = Field(description="List of generated automation tests")

class HealingProposal(BaseModel):
    test_case_id: str = Field(..., description="The ID of the failing test. Use 'NEEDS_CLARIFICATION' if unknown.")
    patch_file_path: str = Field(description="The path to the .patch file generated")
    git_diff: str = Field(description="The diff of the proposed fix")
    status: str = Field(description="e.g. 'PROPOSED_PATCH_WAITING_HUMAN_APPROVAL'")

class JiraDefect(BaseModel):
    defect_id: str = Field(..., description="Jira Defect ID. Use 'NEEDS_CLARIFICATION' if unknown.")
    test_case_id: str = Field(..., description="Associated Test Case ID. Use 'NEEDS_CLARIFICATION' if unknown.")
    title: str = Field(description="Defect title")
    description: str = Field(description="Defect description")
    priority: str = Field(description="Priority of the defect")

class TestReport(BaseModel):
    report_id: str = Field(..., description="Unique Report ID. Use 'NEEDS_CLARIFICATION' if unknown.")
    execution_date: str = Field(description="Date of test execution")
    total_tests: int
    passed: int
    failed: int
    skipped: int
    pass_rate: float

class AIQualityEvaluation(BaseModel):
    golden_id: str = Field(..., description="Associated golden standard ID. Use 'NEEDS_CLARIFICATION' if unknown.")
    metric_name: str = Field(description="Name of the metric evaluated (e.g. 'AnswerRelevancy')")
    score: float = Field(description="Score from 0.0 to 1.0")
    reasoning: str = Field(description="AI explanation for the score")
    passed: bool = Field(description="Whether the score met the threshold")
