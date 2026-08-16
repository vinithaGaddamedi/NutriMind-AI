from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, model_validator

class ChatbotGoldenCategory(str, Enum):
    BASIC = "basic"
    DIETARY = "dietary"
    ALLERGY = "allergy"
    NUTRITION = "nutrition"
    MULTI_TURN = "multi-turn"
    AMBIGUITY = "ambiguity"
    HALLUCINATION = "hallucination"
    SAFETY = "safety"
    PROMPT_INJECTION = "prompt injection"
    ROLE_ADHERENCE = "role adherence"
    CONTEXT_RETENTION = "context retention"
    CONFLICTING_CONSTRAINTS = "conflicting constraints"

class GoldenMessage(BaseModel):
    role: str = Field(..., description="Role of the sender (e.g., user, assistant)")
    content: str = Field(..., description="Content of the message")

class GoldenContext(BaseModel):
    dietary_preferences: Optional[List[str]] = Field(default_factory=list)
    allergies: Optional[List[str]] = Field(default_factory=list)
    pantry_items: Optional[List[str]] = Field(default_factory=list)
    budget: Optional[float] = None
    goals: Optional[List[str]] = Field(default_factory=list)

class EvaluationMetrics(BaseModel):
    relevance: bool = Field(default=True)
    safety: bool = Field(default=True)
    accuracy: bool = Field(default=True)
    tone: bool = Field(default=True)

class ChatbotGolden(BaseModel):
    golden_id: str = Field(..., description="Unique identifier for the golden scenario")
    category: ChatbotGoldenCategory = Field(..., description="Category of the test scenario")
    conversation: List[GoldenMessage] = Field(..., min_length=1, description="Message history including the final user prompt")
    context: Optional[GoldenContext] = Field(default_factory=GoldenContext)
    constraints: List[str] = Field(default_factory=list, description="Specific rules the AI must follow")
    expected_behavior: str = Field(..., description="Description of how the AI should respond")
    forbidden_behavior: List[str] = Field(default_factory=list, description="Behaviors the AI must explicitly avoid")
    evaluation_metrics: EvaluationMetrics = Field(default_factory=EvaluationMetrics)
    severity: str = Field(default="medium", description="Severity if this test fails (low, medium, high, critical)")

class ChatbotGoldenDataset(BaseModel):
    goldens: List[ChatbotGolden] = Field(..., min_length=1)

    @model_validator(mode='after')
    def check_duplicate_ids(self) -> 'ChatbotGoldenDataset':
        seen = set()
        duplicates = set()
        for golden in self.goldens:
            if golden.golden_id in seen:
                duplicates.add(golden.golden_id)
            seen.add(golden.golden_id)
        if duplicates:
            raise ValueError(f"Duplicate golden_ids found: {', '.join(duplicates)}")
        return self

class AgentQualityMetrics(BaseModel):
    task_completion: bool = Field(default=True)
    correctness: bool = Field(default=True)
    schema_adherence: bool = Field(default=True)
    hallucination_free: bool = Field(default=True)
    consistency: bool = Field(default=True)
    traceability: bool = Field(default=True)
    unnecessary_output: bool = Field(default=False)
    instruction_adherence: bool = Field(default=True)

class AgentGolden(BaseModel):
    golden_id: str = Field(..., description="Unique ID for agent golden")
    agent_name: str = Field(..., description="Target agent (e.g. RequirementAgent, AutomationAgent)")
    input_data: Dict[str, Any] = Field(..., description="The inputs passed to the agent")
    constraints: List[str] = Field(default_factory=list, description="Specific instructions the agent must follow")
    expected_behavior: str = Field(..., description="Description of the ideal output")
    forbidden_behavior: List[str] = Field(default_factory=list, description="Things the agent MUST NOT do (e.g., invent APIs)")
    quality_metrics: AgentQualityMetrics = Field(default_factory=AgentQualityMetrics)
    severity: str = Field(default="high")

class AgentGoldenDataset(BaseModel):
    goldens: List[AgentGolden] = Field(..., min_length=1)

    @model_validator(mode='after')
    def check_duplicate_ids(self) -> 'AgentGoldenDataset':
        seen = set()
        duplicates = set()
        for golden in self.goldens:
            if golden.golden_id in seen:
                duplicates.add(golden.golden_id)
            seen.add(golden.golden_id)
        if duplicates:
            raise ValueError(f"Duplicate golden_ids found: {', '.join(duplicates)}")
        return self
