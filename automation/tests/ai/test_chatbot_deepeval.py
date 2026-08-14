import pytest
import requests
from tests.ai.metrics.dietary_compliance import DietaryComplianceMetric

CHAT_API_URL = "http://localhost:8000/api/chat/"

@pytest.mark.deepeval
@pytest.mark.agentic
def test_chatbot_high_protein_vegetarian_dinner():
    input_query = "Suggest a high protein vegetarian dinner."
    payload = {
        "message": input_query,
        "conversation_id": "deepeval-chatbot-001",
        "user_context": {"diet": "vegetarian"}
    }

    response = requests.post(CHAT_API_URL, json=payload)
    assert response.status_code == 200, f"Chat API call failed: {response.text}"

    actual_output = response.json().get("response", "")
    assert len(actual_output) > 0, "Chatbot returned empty output"

    # Evaluate using Dietary Compliance Metric
    metric = DietaryComplianceMetric(target_diet="vegetarian", threshold=0.8)
    res = metric.measure(actual_output)

    assert res["passed"], f"Dietary compliance metric failed: {res['violations']}"
    print(f"\n✅ Chatbot DeepEval Test Passed (Dietary Score: {res['score']:.2f})")
