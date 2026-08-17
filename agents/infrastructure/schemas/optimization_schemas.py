from pydantic import BaseModel, Field
from typing import List, Dict, Any

class TestMetadata(BaseModel):
    test_id: str = Field(description="The unique identifier for the test")
    requirement_risk: str = Field(description="Critical, High, Medium, Low")
    duration_ms: int = Field(description="Execution duration in milliseconds")
    historical_failure_rate: float = Field(description="Failure rate between 0.0 and 1.0")
    is_flaky: bool = Field(description="Whether the test is known to be flaky")
    dependencies: List[str] = Field(default_factory=list, description="Code modules this test explicitly covers")

class OptimizationInput(BaseModel):
    changed_code: List[str] = Field(description="List of files or modules modified in the current diff")
    available_tests: List[TestMetadata] = Field(description="The complete pool of all available automated tests")
    target_pr_duration_ms: int = Field(default=300000, description="Target maximum duration for the PR suite in ms")

class SelectedTest(BaseModel):
    test_id: str = Field(description="The selected test ID")
    reasoning: str = Field(description="Detailed reasoning for why this test was selected for this suite")

class TestSuiteSelection(BaseModel):
    tests: List[SelectedTest] = Field(default_factory=list, description="List of tests selected for this suite")

class OptimizationReport(BaseModel):
    pr_suite: TestSuiteSelection = Field(description="Fast, highly relevant tests mapped to code changes and high risk")
    nightly_suite: TestSuiteSelection = Field(description="Broader suite including flaky and long-running tests")
    release_suite: TestSuiteSelection = Field(description="The comprehensive suite of all tests")
