import pytest
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from unittest.mock import MagicMock
from agents.orchestration.automation_orchestrator import AutomationOrchestrator as AutomationAgent
from agents.schemas.execution_schemas import ManualTestCase, TestDataSet
from agents.schemas.llm_schema import LLMResponse, LLMResponseMetadata

def load_goldens():
    filepath = os.path.join(os.path.dirname(__file__), "..", "test_data", "ai", "golden_automation_code.json")
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
def test_automation_agent_golden(golden, mock_gateway):
    agent = AutomationAgent()
    agent.gateway = mock_gateway
    
    input_tc = ManualTestCase(**golden["input"]["test_case"])
    input_ds = TestDataSet(**golden["input"]["dataset"])
    
    mock_code = "import pytest\ndef test_login(page):\n    pass"
    if golden["type"] == "time_sleep_rejection":
        mock_code = "import time\nimport pytest\ndef test_login(page):\n    time.sleep(5)\n    pass"
        
    mock_response = {
        "test_case_id": input_tc.test_case_id,
        "story_id": input_tc.story_id,
        "requirement_id": input_tc.requirement_id,
        "scenario_id": input_tc.scenario_id,
        "code": mock_code,
        "framework": "playwright"
    }
    
    mock_gateway.generate_text.return_value = get_mock_llm_response(json.dumps(mock_response))
    
    result = agent.generate_playwright_test(input_tc, input_ds)
    
    if golden["type"] == "time_sleep_rejection":
        assert not result.is_success
        assert "time.sleep" in result.error.message
    else:
        assert result.is_success
