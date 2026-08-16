from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from agents.schemas.base_agent_schema import AgentInput, AgentOutput

class PlannerInput(AgentInput):
    test_scenario: str
    acceptance_criteria: List[str]

class PlannerOutput(AgentOutput):
    test_id: str
    objective: str
    preconditions: List[str]
    steps: List[str]
    expected_results: List[str]
    selectors_or_elements: List[str]
    validation_points: List[str]
    automation_priority: str
    requires_ai_evaluation: bool

class GeneratorInput(AgentInput):
    plan: PlannerOutput
    existing_page_objects: List[str]

class GeneratorOutput(AgentOutput):
    pytest_code: str
    imports_required: List[str]

class ValidatorInput(AgentInput):
    generated_code: str
    original_requirement: str

class ValidatorOutput(AgentOutput):
    coverage_status: str = Field(description="INSUFFICIENT or SUFFICIENT")
    covered_requirements: List[str]
    missing_requirements: List[str]
    risk: str
    recommended_changes: List[str]
