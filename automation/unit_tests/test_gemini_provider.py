import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Ensure automation directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.providers.gemini_provider import GeminiProvider
from agents.providers.factory import AIProviderFactory
from google.genai.errors import APIError

class TestGeminiProvider(unittest.TestCase):

    def test_init_without_key_returns_notice(self):
        with patch.dict(os.environ, {}, clear=True):
            provider = GeminiProvider()
            self.assertIsNone(provider.client)
            result = provider.generate_text("Test Prompt")
            self.assertIn("GOOGLE_API_KEY environment variable is not set", result.content)

    def test_init_with_custom_model_env(self):
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "AIzaSyTestKey12345", "GEMINI_MODEL": "gemini-1.5-pro"}):
            with patch("google.genai.Client") as mock_client:
                provider = GeminiProvider()
                self.assertEqual(provider.model_name, "gemini-1.5-pro")
                mock_client.assert_called_once_with(api_key="AIzaSyTestKey12345")

    def test_key_fallback_to_gemini_api_key(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "AIzaSyFallbackKey999"}, clear=True):
            with patch("google.genai.Client") as mock_client:
                provider = GeminiProvider()
                self.assertEqual(provider.api_key, "AIzaSyFallbackKey999")
                mock_client.assert_called_once_with(api_key="AIzaSyFallbackKey999")

    def test_generate_text_success_mocked(self):
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "AIzaSyTestKey12345"}):
            with patch("google.genai.Client") as mock_client_cls:
                mock_instance = MagicMock()
                mock_response = MagicMock()
                mock_response.text = "Generated Gemini response text."
                mock_instance.models.generate_content.return_value = mock_response
                mock_client_cls.return_value = mock_instance

                provider = GeminiProvider()
                output = provider.generate_text("Hello Gemini", system_instruction="Be helpful.")

                self.assertEqual(output.content, "Generated Gemini response text.")
                mock_instance.models.generate_content.assert_called_once()
                call_args = mock_instance.models.generate_content.call_args
                self.assertEqual(call_args.kwargs["model"], "gemini-2.5-flash")
                self.assertEqual(call_args.kwargs["contents"], "Hello Gemini")

    def test_analyze_failure_formatting(self):
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "AIzaSyTestKey12345"}):
            with patch("google.genai.Client") as mock_client_cls:
                mock_instance = MagicMock()
                mock_response = MagicMock()
                mock_response.text = "Root cause: Element button[id='submit'] not found."
                mock_instance.models.generate_content.return_value = mock_response
                mock_client_cls.return_value = mock_instance

                provider = GeminiProvider()
                result = provider.analyze_failure(
                    error_message="TimeoutError: Locator button not found",
                    stack_trace="Traceback line 42",
                    page_dom="<div><button id='other'>Click</button></div>"
                )

                self.assertEqual(result.content, "Root cause: Element button[id='submit'] not found.")
                call_contents = mock_instance.models.generate_content.call_args.kwargs["contents"]
                self.assertIn("TimeoutError: Locator button not found", call_contents)
                self.assertIn("Page DOM Snippet", call_contents)

    def test_generate_test_code_formatting(self):
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "AIzaSyTestKey12345"}):
            with patch("google.genai.Client") as mock_client_cls:
                mock_instance = MagicMock()
                mock_response = MagicMock()
                mock_response.text = "```python\ndef test_sample(page):\n    pass\n```"
                mock_instance.models.generate_content.return_value = mock_response
                mock_client_cls.return_value = mock_instance

                provider = GeminiProvider()
                code = provider.generate_test_code("function App() { return <button>Click</button>; }")

                self.assertIn("def test_sample(page)", code.content)

    def test_api_error_handling(self):
        with patch.dict(os.environ, {"GOOGLE_API_KEY": "AIzaSyTestKey12345"}):
            with patch("google.genai.Client") as mock_client_cls:
                mock_instance = MagicMock()
                mock_instance.models.generate_content.side_effect = Exception("Rate limit reached or network error")
                mock_client_cls.return_value = mock_instance

                provider = GeminiProvider()
                with self.assertRaises(Exception) as context:
                    provider.generate_text("Test prompt")
                self.assertIn("Rate limit reached", str(context.exception))

    def test_factory_returns_gemini_provider(self):
        with patch.dict(os.environ, {"AI_PROVIDER": "gemini"}):
            provider = AIProviderFactory.get_provider()
            self.assertIsInstance(provider, GeminiProvider)

if __name__ == "__main__":
    unittest.main()
