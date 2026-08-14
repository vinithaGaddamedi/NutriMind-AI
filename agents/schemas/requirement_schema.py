from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RequirementModel(BaseModel):
    story_id: str = Field(..., description="Jira Story ID, e.g. MEAL-101")
    title: str = Field(..., description="Story summary title")
    description: str = Field(..., description="Story description")
    business_rules: List[str] = Field(default_factory=list, description="Extracted business rules")
    acceptance_criteria: List[Dict[str, str]] = Field(default_factory=list, description="List of ACs e.g. [{'ac_id': 'AC-01', 'rule': '...'}]")
    testable_conditions: List[str] = Field(default_factory=list, description="Testable conditions")
    ambiguities: List[str] = Field(default_factory=list, description="Identified ambiguities or missing details")
    risks: List[str] = Field(default_factory=list, description="Identified risks")
