import pytest
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from unittest.mock import MagicMock
from agents.intelligence.review_agent import ReviewAgent
from agents.infrastructure.schemas.execution_schemas import AutomationTest
from agents.infrastructure.schemas.llm_schema import LLMResponse, LLMResponseMetadata

def load_goldens():
    filepath = os.path.join(os.path.dirname(__file__), "..", "..", "ai_testing", "golden_datasets", "golden_code_reviews.json")
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
def test_review_agent_golden(golden, mock_gateway):
    agent = ReviewAgent()
    agent.gateway = mock_gateway
    
    input_test = AutomationTest(**golden["input"]["automation_test"])
    
    # We simulate the LLM hallucinating and approving bad code
    mock_response = {
        "is_approved": True,
        "score": 0.9,
        "comments": ["Looks great!"],
        "suggested_fixes": []
    }
    
    mock_gateway.generate_text.return_value = get_mock_llm_response(json.dumps(mock_response))
    
    result = agent.review_code(input_test)
    
    assert result.is_success
    # The deterministic hook should have overridden the AI and rejected it
    assert result.data.is_approved == False
    assert result.data.score == 0.0
    
    if golden["type"] == "time_sleep_override":
        assert any("time.sleep" in f for f in result.data.suggested_fixes)
    elif golden["type"] == "direct_locator_override":
        assert any("Page Object Model" in f for f in result.data.suggested_fixes)
