import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from google.genai.errors import APIError

client = TestClient(app)

class TestBackendChatRoute(unittest.TestCase):

    def test_post_chat_success(self):
        payload = {
            "message": "Suggest a healthy breakfast with bananas and oats.",
            "conversation_id": "test-conv-001",
            "user_context": {"dietary_preferences": ["vegetarian"]}
        }
        response = client.post("/api/chat/", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertEqual(data["conversation_id"], "test-conv-001")
        self.assertIn("model", data)
        self.assertTrue(len(data["response"]) > 0)

    def test_post_chat_empty_message_validation(self):
        payload = {
            "message": "  ",
            "conversation_id": "test-conv-002"
        }
        response = client.post("/api/chat/", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Message field cannot be empty", response.json()["detail"])

    @patch('services.ai_chat_service.genai.Client')
    def test_post_chat_api_timeout_fallback(self, mock_genai_client):
        # We need to simulate the client throwing a TimeoutError
        mock_client_instance = MagicMock()
        mock_client_instance.models.generate_content.side_effect = TimeoutError("Connection timed out")
        
        # Reset the service client
        from services.ai_chat_service import chat_service
        chat_service.client = mock_client_instance
        
        payload = {
            "message": "Timeout test",
            "conversation_id": "test-conv-003"
        }
        
        response = client.post("/api/chat/", json=payload)
        self.assertEqual(response.status_code, 200) # Should fallback safely, not 500
        data = response.json()
        self.assertIn("Your request took too long to process", data["response"])
        
    @patch('services.ai_chat_service.genai.Client')
    def test_post_chat_api_error_fallback(self, mock_genai_client):
        # Simulate an APIError
        mock_client_instance = MagicMock()
        mock_client_instance.models.generate_content.side_effect = APIError("503 Service Unavailable", {})
        
        from services.ai_chat_service import chat_service
        chat_service.client = mock_client_instance
        
        payload = {
            "message": "API Error test",
            "conversation_id": "test-conv-004"
        }
        
        response = client.post("/api/chat/", json=payload)
        self.assertEqual(response.status_code, 200) # Fallback safely
        data = response.json()
        self.assertIn("currently experiencing high traffic or a temporary service disruption", data["response"])

if __name__ == "__main__":
    unittest.main()
