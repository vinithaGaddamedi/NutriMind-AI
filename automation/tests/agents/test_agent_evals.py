import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from automation.utils.golden_validator import validate_agent_golden_dataset
from automation.utils.ai_test_oracle import AITestOracle

AGENT_GOLDENS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../test_data/ai/goldens/agents'))

@pytest.fixture(scope="module")
def agent_goldens():
    all_goldens = []
    if os.path.exists(AGENT_GOLDENS_DIR):
        for file in os.listdir(AGENT_GOLDENS_DIR):
            if file.endswith(".json"):
                dataset = validate_agent_golden_dataset(os.path.join(AGENT_GOLDENS_DIR, file))
                all_goldens.extend(dataset.goldens)
    return all_goldens

@pytest.fixture(scope="module")
def oracle():
    return AITestOracle()

def test_agent_outputs_with_oracle(oracle, agent_goldens):
    """
    Simulates sending inputs to each agent, intercepting their response,
    and evaluating it using the AI Test Oracle.
    """
    if not agent_goldens:
        pytest.skip("No agent goldens found.")
        
    for golden in agent_goldens:
        # Mocking output logic just for testing the Oracle functionality.
        # In a real run, this calls the actual agent logic.
        if golden.golden_id == "AGENT-FAIL-01":
            actual_output = "The failure is due to a missing selector '#login-btn'. I recommend adding page.wait_for_selector('#login-btn')."
        elif golden.golden_id == "AGENT-AUTO-01":
            actual_output = "page.goto('/login')\npage.fill('#user', 'test')\npage.click('#submit')"
        else:
            actual_output = "Generic valid response meeting requirements."
            
        # Oracle Evaluation
        decision = oracle.evaluate(
            actual_output=actual_output,
            expected_behavior=golden.expected_behavior,
            constraints=golden.constraints + golden.forbidden_behavior,
            context=golden.input_data
        )
        
        assert decision.passed is True, f"Agent {golden.agent_name} failed oracle evaluation. Reason: {decision.reason}, Violations: {decision.violations}"
