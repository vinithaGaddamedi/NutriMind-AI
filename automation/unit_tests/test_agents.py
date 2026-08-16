import pytest
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from unittest.mock import MagicMock
from agents.shift_left.requirement_agent import RequirementAgent
from agents.infrastructure.schemas.requirement_schema import RequirementAnalysis
from agents.shift_left.risk_agent import RiskAgent
from agents.shift_left.test_design_agent import TestDesignAgent
from agents.intelligence.failure_agent import FailureAgent
from agents.automation.self_healing_agent import SelfHealingPatchAgent
from agents.infrastructure.schemas.llm_schema import LLMResponse, LLMResponseMetadata

@pytest.fixture
def mock_gateway():
    gateway = MagicMock()
    return gateway

def get_mock_llm_response(content: str) -> LLMResponse:
    metadata = LLMResponseMetadata(correlation_id="mock-1", latency_ms=10)
    return LLMResponse(content=content, metadata=metadata)

def test_requirement_agent_success(mock_gateway):
    agent = RequirementAgent()
    agent.gateway = mock_gateway
    
    mock_response = {
        "story_id": "MEAL-101",
        "requirement_id": "REQ-101",
        "title": "Vegetarian Plan",
        "description": "User needs vegetarian plan",
        "business_rules": [],
        "acceptance_criteria": [],
        "functional_requirements": [],
        "non_functional_requirements": [],
        "testable_conditions": [],
        "assumptions": [],
        "ambiguities": [],
        "dependencies": [],
        "risks": [],
        "missing_information": []
    }
    
    mock_gateway.generate_text.return_value = get_mock_llm_response(json.dumps(mock_response))
    
    result = agent.analyze_jira_story(
        story_id="MEAL-101", 
        title="Vegetarian Plan", 
        description="User needs vegetarian plan",
        acceptance_criteria="No meat",
        comments="Make it fast"
    )
    
    assert result.is_success
    assert isinstance(result.data, RequirementAnalysis)
    assert result.data.story_id == "MEAL-101"
    assert result.data.title == "Vegetarian Plan"
    assert result.data.requirement_id == "REQ-101"

def test_risk_agent_success(mock_gateway):
    agent = RiskAgent()
    agent.gateway = mock_gateway
    
    req_model = RequirementAnalysis(
        story_id="MEAL-101",
        requirement_id="REQ-101",
        title="Test",
        description="Test",
        business_rules=[],
        acceptance_criteria=[],
        testable_conditions=[],
        ambiguities=[],
        risks=["Allergy risk"]
    )
    
    mock_response = {
        "story_id": "MEAL-101",
        "scenarios": [
            {
                "scenario_id": "TS-01",
                "requirement_id": "REQ-101",
                "risk_id": "NONE",
                "title": "Positive Flow",
                "description": "Test positive flow",
                "test_type": "positive",
                "priority": "High",
                "preconditions": [],
                "test_data": "None",
                "expected_behavior": "Success",
                "automation_candidate": True,
                "golden_candidate": False
            }
        ],
        "risks": [
            {
                "risk_id": "RSK-01",
                "requirement_id": "REQ-MEAL-101",
                "description": "High risk of failure",
                "category": "functional",
                "severity": "High",
                "probability": "Medium",
                "priority": "P1",
                "business_impact": "Loss of users",
                "technical_impact": "Database corruption",
                "recommended_test_types": ["UI", "API"]
            }
        ]
    }
    mock_gateway.generate_text.return_value = get_mock_llm_response(json.dumps(mock_response))
    
    result = agent.evaluate_risks(req_model)
    assert result.is_success
    assert result.data.story_id == "MEAL-101"
    assert len(result.data.risks) == 1
    assert result.data.risks[0].risk_id == "RSK-01"

def test_failure_agent_success(mock_gateway):
    agent = FailureAgent()
    agent.gateway = mock_gateway
    
    mock_response = {
        "test_case_id": "TC-01",
        "failure_type": "LOCATOR_FAILURE",
        "root_cause": "Button ID changed",
        "evidence": "Selector button#submit did not match any elements",
        "confidence": 0.95,
        "recommended_action": "Update locator",
        "requires_human_review": True
    }
    
    mock_gateway.generate_text.return_value = get_mock_llm_response(json.dumps(mock_response))
    
    result = agent.classify_and_analyze("TC-01", "Timeout", "Traceback", "<div></div>")
    assert result.is_success
    assert result.data.failure_type == "LOCATOR_FAILURE"
    assert result.data.confidence == 0.95

def test_self_healing_patch_generation():
    agent = SelfHealingPatchAgent()
    result = agent.propose_patch("test.py", "#old", "#new")
    
    assert result.is_success
    assert result.data.status == "PROPOSED_PATCH_WAITING_HUMAN_APPROVAL"
    assert "--- a/test.py" in result.data.git_diff
    assert "patch_file_path" in result.data.model_dump()
