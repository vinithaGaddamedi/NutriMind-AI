import pytest
import json
import os
from unittest.mock import MagicMock
from agents.intelligence.data_agent import TestDataAgent
from agents.infrastructure.schemas.qa_schemas import ScenariosListModel, TestScenario
from agents.infrastructure.schemas.execution_schemas import TestDataSetsListModel, TestDataSet
from agents.infrastructure.schemas.llm_schema import LLMResponse, LLMResponseMetadata

def load_goldens():
    filepath = os.path.join(os.path.dirname(__file__), "..", "..", "ai_testing", "golden_datasets", "golden_data_sets.json")
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
def test_data_agent_golden(golden, mock_gateway):
    agent = TestDataAgent()
    agent.gateway = mock_gateway
    
    input_data = golden["input"]
    scenarios_list = []
    for s in input_data["scenarios"]:
        scenarios_list.append(TestScenario(**s))
        
    scenarios = ScenariosListModel(scenarios=scenarios_list)
    
    mock_dataset = {
        "dataset_id": "DS-01",
        "scenario_id": scenarios_list[0].scenario_id,
        "description": "Mock dataset",
        "positive_data": [{"email": "test@test.com"}],
        "negative_data": [],
        "boundary_data": [],
        "security_data": [], # Intentionally empty to test fallback
        "expected_validation_errors": [],
        "pii_synthetic": False if golden["type"] == "pii_violation" else True
    }
    
    mock_response = {
        "datasets": [mock_dataset]
    }
    
    mock_gateway.generate_text.return_value = get_mock_llm_response(json.dumps(mock_response))
    
    result = agent.generate_datasets(scenarios)
    assert result.is_success
    
    ds = result.data.datasets[0]
    
    if golden["type"] == "security_injection_fallback":
        # Hook should have injected default payload
        assert len(ds.security_data) > 0
        assert "payload" in ds.security_data[0]
    elif golden["type"] == "pii_violation":
        # Hook should have forced pii_synthetic to true and clobbered positive data
        assert ds.pii_synthetic == True
        assert "NEEDS_CLARIFICATION" in ds.positive_data[0].get("error", "")
