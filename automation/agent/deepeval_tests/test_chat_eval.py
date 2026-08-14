import pytest
import os
import requests

# Try importing DeepEval components if installed
try:
    from deepeval.test_case import LLMTestCase
    from deepeval.metrics import AnswerRelevancyMetric, GEval
    from deepeval import assert_test
    HAS_DEEPEVAL = True
except ImportError:
    HAS_DEEPEVAL = False

CHAT_API_URL = "http://localhost:8000/api/chat/"

@pytest.mark.deepeval
def test_chat_ai_relevancy_eval():
    user_input = "I want a keto-friendly meal plan for dinner with under 600 calories."
    payload = {
        "message": user_input,
        "conversation_id": "deepeval-test-001",
        "user_context": {"diet": "keto", "goal": "weight_loss"}
    }
    
    response = requests.post(CHAT_API_URL, json=payload)
    assert response.status_code == 200, f"Backend Chat API failed: {response.text}"
    
    actual_output = response.json().get("response", "")
    assert len(actual_output) > 0, "Chat response output was empty"

    if HAS_DEEPEVAL and os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY"):
        test_case = LLMTestCase(
            input=user_input,
            actual_output=actual_output,
            expected_output="A keto-friendly dinner recommendation with low carbs and under 600 calories."
        )
        relevancy_metric = AnswerRelevancyMetric(threshold=0.7)
        assert_test(test_case, [relevancy_metric])
    else:
        # Fallback metric validation checking domain-specific keywords and structure
        lower_output = actual_output.lower()
        domain_keywords = ["keto", "meal", "calorie", "protein", "fat", "dinner", "recipe", "nutrimind"]
        keyword_matches = sum(1 for kw in domain_keywords if kw in lower_output)
        
        assert keyword_matches >= 1, f"Response did not contain expected NutriMind domain context: {actual_output}"
        print(f"\n✅ DeepEval Fallback Evaluation Passed (Domain Context Score: {keyword_matches}/{len(domain_keywords)})")
