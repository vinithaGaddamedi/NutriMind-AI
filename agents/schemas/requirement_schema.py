from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RequirementAnalysis(BaseModel):
    story_id: str = Field(..., description="Jira Story ID, e.g. MEAL-101. If unknown, use 'NEEDS_CLARIFICATION'")
    requirement_id: str = Field(..., description="Unique Requirement ID. If unknown, use 'NEEDS_CLARIFICATION'")
    title: str = Field(..., description="Story summary title")
    description: str = Field(..., description="Story description")
    business_rules: List[str] = Field(default_factory=list, description="Extracted business rules")
    acceptance_criteria: List[Dict[str, str]] = Field(default_factory=list, description="List of ACs e.g. [{'acceptance_criteria_id': 'AC-01', 'rule': '...'}]")
    functional_requirements: List[str] = Field(default_factory=list, description="Extracted functional requirements")
    non_functional_requirements: List[str] = Field(default_factory=list, description="Extracted non-functional requirements")
    testable_conditions: List[str] = Field(default_factory=list, description="Testable conditions")
    assumptions: List[str] = Field(default_factory=list, description="Identified assumptions")
    ambiguities: List[str] = Field(default_factory=list, description="Identified ambiguities")
    dependencies: List[str] = Field(default_factory=list, description="Identified dependencies")
    risks: List[str] = Field(default_factory=list, description="Identified risks")
    missing_information: List[str] = Field(default_factory=list, description="Missing information or missing acceptance criteria")
