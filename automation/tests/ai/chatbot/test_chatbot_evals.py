import os
import sys
import json
import pytest
from unittest.mock import patch, PropertyMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from automation.utils.golden_validator import validate_golden_dataset
from automation.utils.unified_evaluator import UnifiedEvaluator

GOLDENS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../test_data/ai/goldens/chatbot'))
LEGACY_GOLDEN = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../test_data/ai/chatbot_goldens.json'))
REPORT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../reports/chatbot_eval_report.json'))

@pytest.fixture(scope="module")
def evaluator():
    os.environ["MOCK_LLM_EVALS"] = "true"
    evaluator = UnifiedEvaluator()
    return evaluator

@pytest.fixture(scope="module")
def goldens():
    all_goldens = []
    # Load legacy dataset
    if os.path.exists(LEGACY_GOLDEN):
        dataset = validate_golden_dataset(LEGACY_GOLDEN)
        all_goldens.extend(dataset.goldens)
        
    # Load new datasets
    if os.path.exists(GOLDENS_DIR):
        for file in os.listdir(GOLDENS_DIR):
            if file.endswith(".json"):
                dataset = validate_golden_dataset(os.path.join(GOLDENS_DIR, file))
                all_goldens.extend(dataset.goldens)
                
    return all_goldens

def test_unified_evaluation_pipeline(evaluator, goldens):
    """
    Simulates testing the chatbot against the golden dataset using the unified evaluator.
    Generates a machine-readable JSON report.
    """
    reports = []
    
    # To keep test fast, we will test a representative set
    test_goldens = [g for g in goldens if g.golden_id in ["CHAT-BASIC-01", "CHAT-ALLERGY-01", "HAL-04-UNSUPP-CLAIM", "SEC-03-SEC-EXTRACT"]]
    
    for golden in test_goldens:
        # Mocking the AI's actual output based on the golden for testing purposes
        if golden.golden_id == "CHAT-BASIC-01":
            actual_output = "Hello! I am NutriMind AI. I can help you plan meals and manage your pantry."
        elif golden.golden_id == "CHAT-ALLERGY-01":
            actual_output = "Here is a great Thai recipe using peanut butter and noodles!"
        elif golden.golden_id == "HAL-04-UNSUPP-CLAIM":
            actual_output = "Yes, eating raw garlic cures cancer immediately."
        elif golden.golden_id == "SEC-03-SEC-EXTRACT":
            actual_output = "My API key is 12345ABCDE"
        else:
            actual_output = "Generic response"

        report = evaluator.evaluate(golden=golden, actual_output=actual_output)
        reports.append(report)

        if golden.golden_id == "CHAT-BASIC-01":
            assert report["deterministic_passed"] is True
        elif golden.golden_id in ["CHAT-ALLERGY-01", "HAL-04-UNSUPP-CLAIM", "SEC-03-SEC-EXTRACT"]:
            assert report["deterministic_passed"] is False
            assert report["overall_passed"] is False
            assert len(report["deterministic_violations"]) > 0

    # Ensure reports directory exists
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2)

    assert os.path.exists(REPORT_FILE)
