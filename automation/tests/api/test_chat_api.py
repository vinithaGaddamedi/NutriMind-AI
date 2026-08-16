import pytest
import requests

BASE_URL = "http://localhost:8000/api/chat"

def test_chat_api_valid_request():
    payload = {
        "message": "What high-protein snacks do you recommend for weight loss?",
        "conversation_id": "test-api-conv-101",
        "user_context": {
            "diet": "high-protein",
            "goal": "weight_loss"
        }
    }
    response = requests.post(f"{BASE_URL}/", json=payload)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}: {response.text}"
    
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0
    assert data["conversation_id"] == "test-api-conv-101"
    assert "model" in data

def test_chat_api_empty_message_validation():
    payload = {
        "message": "   ",
        "conversation_id": "test-api-conv-102"
    }
    response = requests.post(f"{BASE_URL}/", json=payload)
    assert response.status_code == 400, f"Expected 400 Bad Request, got {response.status_code}"
    assert "Message field cannot be empty" in response.json()["detail"]

def test_chat_api_auto_generated_conversation_id():
    payload = {
        "message": "How do I scan pantry items?"
    }
    response = requests.post(f"{BASE_URL}/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"].startswith("conv-")
