from pydantic import BaseModel, Field
from typing import List, Optional, Any

class ConstraintViolation(BaseModel):
    severity: str = Field(..., description="Severity of the violation (low, medium, high, critical)")
    constraint: str = Field(..., description="The constraint that was violated")
    actual_value: Any = Field(..., description="The value found in the response")
    expected_value: Any = Field(..., description="The value that was expected")

class ValidationResult(BaseModel):
    passed: bool = Field(..., description="True if no constraints were violated")
    violations: List[ConstraintViolation] = Field(default_factory=list, description="List of constraints violated")

