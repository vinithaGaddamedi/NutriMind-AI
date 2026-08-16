import pytest
import json
import os
from unittest.mock import MagicMock
from agents.shift_left.risk_agent import RiskAgent
from agents.schemas.requirement_schema import RequirementAnalysis
from agents.schemas.llm_schema import LLMResponse, LLMResponseMetadata

def load_goldens():
    filepath = os.path.join(os.path.dirname(__file__), "..", "test_data", "ai", "golden_risks.json")
    with open(filepath, "r") as f:
        return json.load(f)

goldens = load_goldens()

@pytest.fixture
def mock_gateway():
    return MagicMock()

def get_mock_llm_response(content: str) -> LLMResponse:
    metadata = LLMResponseMetadata(correlation_id="mock-1", latency_ms=10)
    return LLMResponse(content=content, metadata=metadata)

@pytest.mark.parametrize("golden", goldens, ids=[g["id"] for g in goldens])
def test_risk_agent_golden(golden, mock_gateway):
    agent = RiskAgent()
    agent.gateway = mock_gateway
    
    input_data = golden["input"]
    
    req_analysis = RequirementAnalysis(
        story_id=input_data["story_id"],
        requirement_id=f"REQ-{input_data['story_id']}",
        title=input_data["title"],
        description=input_data["description"],
        business_rules=input_data.get("business_rules", []),
        acceptance_criteria=input_data.get("acceptance_criteria", []),
        functional_requirements=[],
        non_functional_requirements=[],
        testable_conditions=[],
        assumptions=[],
        ambiguities=[],
        dependencies=[],
        risks=input_data.get("risks", []),
        missing_information=[]
    )
    
    # We will simulate the LLM response
    mock_risk = {
        "risk_id": "RSK-001",
        "requirement_id": req_analysis.requirement_id,
        "description": "Some generic risk",
        "category": "functional",
        "severity": "Medium",
        "probability": "Medium",
        "priority": "P2",
        "business_impact": "Moderate",
        "technical_impact": "Moderate",
        "recommended_test_types": ["UI"]
    }
    
    expected_str = str(golden["expected_behavior"]).lower()
    
    # Adjust mock based on expectations so we can test the deterministic rules
    if "allergy" in expected_str:
        mock_risk["description"] = "User has an allergic reaction due to unsafe recommendation"
        mock_risk["severity"] = "Medium" # LLM is wrong, rule should fix
        mock_risk["priority"] = "P2" # LLM is wrong, rule should fix
    elif "hallucinat" in expected_str:
        mock_risk["description"] = "AI hallucinates incorrect nutrition calories"
        mock_risk["category"] = "AI/LLM"
        mock_risk["severity"] = "Low" # LLM is wrong, rule should fix
        mock_risk["priority"] = "P3" # LLM is wrong, rule should fix
    elif "api" in expected_str:
        mock_risk["category"] = "integration"
        mock_risk["description"] = "API failure"
        
    mock_response = {
        "story_id": input_data["story_id"],
        "risks": [mock_risk]
    }
        
    mock_gateway.generate_text.return_value = get_mock_llm_response(json.dumps(mock_response))
    
    result = agent.evaluate_risks(req_analysis)
    
    assert result.is_success
    data = result.data
    assert data.story_id == input_data["story_id"]
    assert len(data.risks) == 1
    
    risk = data.risks[0]
    
    if golden["type"] == "allergy_safety":
        assert risk.severity == "Critical"
        assert risk.priority == "P0"
    elif golden["type"] == "hallucinated_nutrition":
        assert risk.severity in ["Critical", "High"]
        assert risk.priority in ["P0", "P1"]
        assert risk.category == "AI/LLM"
    elif golden["type"] == "api_failure":
        assert risk.category == "integration"
