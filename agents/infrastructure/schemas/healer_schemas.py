from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from agents.infrastructure.schemas.base_agent_schema import AgentInput, AgentOutput

class HealerInput(AgentInput):
    failed_test_name: str
    error_message: str
    dom_snapshot: Optional[str] = None
    old_locator: Optional[str] = None

class HealerOutput(AgentOutput):
    old_locator: str = Field(description="The broken locator")
    proposed_locator: str = Field(description="The new semantic locator")
    reason: str = Field(description="Why the change is correct")
    confidence: float = Field(description="Confidence from 0.0 to 1.0")
    status: str = Field(description="PROPOSED or HEALED")
