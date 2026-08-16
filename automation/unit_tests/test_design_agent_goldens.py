import pytest
import json
import os
from unittest.mock import MagicMock
from agents.test_design_agent import TestDesignAgent
from agents.schemas.requirement_schema import RequirementAnalysis
from agents.schemas.qa_schemas import RiskAnalysis, RiskModel
from agents.schemas.llm_schema import LLMResponse, LLMResponseMetadata

def load_goldens():
    filepath = os.path.join(os.path.dirname(__file__), "..", "test_data", "ai", "golden_test_scenarios.json")
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
def test_test_design_agent_golden(golden, mock_gateway):
    agent = TestDesignAgent()
    agent.gateway = mock_gateway
    
    input_data = golden["input"]
    
    req_analysis = RequirementAnalysis(
        story_id=input_data["req"].get("story_id", "TEST-1"),
        requirement_id=f"REQ-{input_data['req'].get('story_id', 'TEST-1')}",
        title=input_data["req"].get("title", ""),
        description=input_data["req"].get("description", ""),
        business_rules=[],
        acceptance_criteria=[],
        functional_requirements=[],
        non_functional_requirements=[],
        testable_conditions=[],
        assumptions=[],
        ambiguities=[],
        dependencies=[],
        risks=[],
        missing_information=[]
    )
    
    risks = []
    for r in input_data["risk"].get("risks", []):
        risks.append(RiskModel(
            risk_id=r["risk_id"],
            requirement_id=req_analysis.requirement_id,
            description=r.get("description", ""),
            category="security",
            severity=r.get("severity", "High"),
            probability="High",
            priority=r.get("priority", "P1"),
            business_impact="",
            technical_impact="",
            recommended_test_types=[]
        ))
        
    risk_analysis = RiskAnalysis(
        story_id=req_analysis.story_id,
        risks=risks
    )
    
    # We will simulate the LLM response
    mock_scenario_1 = {
        "scenario_id": "TS-01",
        "requirement_id": req_analysis.requirement_id,
        "risk_id": "RSK-SEC-01" if risks else "NONE",
        "title": "Test basic flow",
        "description": "Just testing the flow",
        "test_type": "security" if golden["type"] == "security_prompt_injection" else "positive",
        "priority": "Medium", # Explicitly wrong so the deterministic hook can fix it
        "preconditions": [],
        "test_data": "None",
        "expected_behavior": "It works",
        "automation_candidate": True,
        "golden_candidate": False
    }
    
    mock_scenarios = [mock_scenario_1]
    
    if golden["type"] == "duplicate_detection":
        # Add exact same scenario
        mock_scenario_2 = dict(mock_scenario_1)
        mock_scenario_2["scenario_id"] = "TS-02"
        mock_scenarios.append(mock_scenario_2)
    elif golden["type"] == "hallucination_boundary":
        mock_scenario_1["risk_id"] = "RSK-AI-02"
        
    mock_response = {
        "scenarios": mock_scenarios
    }
        
    mock_gateway.generate_text.return_value = get_mock_llm_response(json.dumps(mock_response))
    
    result = agent.generate_scenarios(req_analysis, risk_analysis)
    
    assert result.is_success
    data = result.data
    
    if golden["type"] == "duplicate_detection":
        # Deduplication hook should have removed the second scenario
        assert len(data.scenarios) == 1
        assert data.scenarios[0].scenario_id == "TS-01"
    elif golden["type"] == "security_prompt_injection":
        # Risk priority P0 should escalate scenario priority to Critical
        assert data.scenarios[0].priority == "Critical"
    elif golden["type"] == "hallucination_boundary":
        # Risk priority P1 should escalate scenario priority to High
        assert data.scenarios[0].priority == "High"
