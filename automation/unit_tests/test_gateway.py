import pytest
from unittest.mock import MagicMock, patch
from agents.providers.ai_gateway import AIGateway
from agents.infrastructure.schemas.llm_schema import LLMResponse, LLMResponseMetadata, LLMRateLimitError, LLMTimeoutError
from google.genai.errors import APIError

@pytest.fixture
def mock_factory():
    with patch('agents.providers.ai_gateway.AIProviderFactory.get_provider') as mock:
        yield mock

def test_gateway_success(mock_factory):
    mock_provider = MagicMock()
    mock_factory.return_value = mock_provider
    
    mock_metadata = LLMResponseMetadata(
        correlation_id="1234",
        latency_ms=100,
        prompt_tokens=10,
        completion_tokens=20,
        total_tokens=30
    )
    mock_provider.generate_text.return_value = LLMResponse(
        content="Success Data",
        metadata=mock_metadata
    )
    
    gateway = AIGateway()
    result = gateway.generate_text("test prompt")
    
    assert result.content == "Success Data"
    mock_provider.generate_text.assert_called_once()

@patch('agents.providers.ai_gateway.time.sleep')
def test_gateway_retry_on_rate_limit(mock_sleep, mock_factory):
    mock_provider = MagicMock()
    mock_factory.return_value = mock_provider
    
    class MockAPIError(APIError):
        def __init__(self, msg, code):
            Exception.__init__(self, msg)
            self.code = code
            
    # Create an APIError simulating 429 Rate Limit
    rate_limit_err = MockAPIError("Quota exceeded", 429)
    
    mock_metadata = LLMResponseMetadata(correlation_id="1234", latency_ms=100)
    success_response = LLMResponse(content="Success after retry", metadata=mock_metadata)
    
    # First call raises rate limit, second call succeeds
    mock_provider.generate_text.side_effect = [rate_limit_err, success_response]
    
    gateway = AIGateway()
    result = gateway.generate_text("test prompt")
    
    assert result.content == "Success after retry"
    assert mock_provider.generate_text.call_count == 2
    mock_sleep.assert_called_once() # Should have slept once

@patch('agents.providers.ai_gateway.time.sleep')
def test_gateway_exhaust_retries(mock_sleep, mock_factory):
    mock_provider = MagicMock()
    mock_factory.return_value = mock_provider
    
    class MockAPIError(APIError):
        def __init__(self, msg, code):
            Exception.__init__(self, msg)
            self.code = code
            
    timeout_err = MockAPIError("Timeout", 504)
    
    # Always raise timeout
    mock_provider.generate_text.side_effect = timeout_err
    
    gateway = AIGateway()
    # Mocking env var default max_retries = 3, so it should try 4 times total (1 initial + 3 retries)
    gateway.max_retries = 3
    
    with pytest.raises(LLMTimeoutError):
        gateway.generate_text("test prompt")
        
    assert mock_provider.generate_text.call_count == 4
    assert mock_sleep.call_count == 3
