import pytest
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from unittest.mock import MagicMock
from agents.requirement_agent import RequirementAgent
from agents.schemas.llm_schema import LLMResponse, LLMResponseMetadata

@pytest.fixture
def mock_gateway():
    gateway = MagicMock()
    return gateway

def get_mock_llm_response(content: str) -> LLMResponse:
    metadata = LLMResponseMetadata(correlation_id="mock-err-1", latency_ms=5)
    return LLMResponse(content=content, metadata=metadata)

@pytest.mark.parametrize("invalid_response_content,expected_error_code", [
    (
        "This is not json { at all", 
        "JSON_PARSE_ERROR"
    ),
    (
        json.dumps({
            "story_id": "MEAL-101",
            "title": "Missing required requirement_id",
            "description": "Missing stuff"
        }),
        "SCHEMA_VALIDATION_ERROR"
    ),
    (
        json.dumps({
            "story_id": "MEAL-101",
            "requirement_id": "REQ-1",
            "title": "Bad types",
            "description": "Desc",
            "business_rules": "This should be a list, not a string"
        }),
        "SCHEMA_VALIDATION_ERROR"
    )
])
def test_requirement_agent_negative_schema_validation(mock_gateway, invalid_response_content, expected_error_code):
    agent = RequirementAgent()
    agent.gateway = mock_gateway
    
    # Mock LLM returning invalid data
    mock_gateway.generate_text.return_value = get_mock_llm_response(invalid_response_content)
    
    result = agent.analyze_jira_story(
        story_id="MEAL-101", 
        title="Title", 
        description="Desc",
        acceptance_criteria=""
    )
    
    assert not result.is_success
    assert result.error is not None
    assert result.error.error_code == expected_error_code
    assert result.data is None
    assert result.metadata.agent_name == "RequirementAgent"
