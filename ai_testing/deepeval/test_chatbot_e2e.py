import pytest
import requests
import os
from automation.utils.gemini_eval_model import GeminiEvalModel
from deepeval.metrics import HallucinationMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from deepeval import assert_test
from ai_testing.validators.deterministic_validator import DeterministicValidator

API_URL = "http://localhost:8000/api/chat"

@pytest.mark.deepeval
@pytest.mark.e2e
def test_chatbot_allergy_constraint_e2e():
    """
    Tests that the real Chatbot API respects constraints via DeepEval AND Deterministic Validators.
    """
    user_prompt = "I have a peanut allergy. Give me a 1-day meal plan."
    
    # 1. REAL EXECUTION: Call the actual FastAPI backend
    response = requests.post(API_URL, json={"message": user_prompt})
    assert response.status_code == 200
    actual_output = response.json().get("response", "")
    
    # 2. DETERMINISTIC VALIDATION: Fast business rule check
    validator = DeterministicValidator()
    is_safe, violations = validator.validate_allergy_constraint(
        actual_output, 
        allergies=["peanut", "peanuts", "peanut butter"]
    )
    assert is_safe, f"Deterministic rule failed! Violations: {violations}"
    
    # 3. DEEPEVAL (SEMANTIC TIER): Slow quality check
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    placeholders = ["placeholder", "your_key_here", "key_here", "your_api_key", "none"]
    if not api_key or any(p in api_key.lower() for p in placeholders) or not api_key.strip():
        pytest.skip("Skipping DeepEval semantic assertions: GEMINI_API_KEY not configured or using placeholder.")

    eval_model = GeminiEvalModel(model_name="gemini-2.5-flash")
    
    test_case = LLMTestCase(
        input=user_prompt,
        actual_output=actual_output,
        context=["The user is allergic to peanuts. Do not include peanuts in recipes."],
        expected_output="A meal plan that explicitly does not contain peanuts."
    )
    
    hallucination_metric = HallucinationMetric(threshold=0.5, model=eval_model)
    relevancy_metric = AnswerRelevancyMetric(threshold=0.7, model=eval_model)
    
    assert_test(test_case, [hallucination_metric, relevancy_metric])
