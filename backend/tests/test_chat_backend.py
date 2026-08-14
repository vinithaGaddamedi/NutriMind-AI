import sys
import os
import unittest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

client = TestClient(app)

class TestBackendChatRoute(unittest.TestCase):

    def test_post_chat_success(self):
        payload = {
            "message": "Suggest a healthy breakfast with bananas and oats.",
            "conversation_id": "test-conv-001",
            "user_context": {"diet": "vegetarian"}
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

if __name__ == "__main__":
    unittest.main()
