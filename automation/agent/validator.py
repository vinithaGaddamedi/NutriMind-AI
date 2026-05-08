def validate_response(response, expected):
    assert response == expected, f"Validation failed: expected {expected}, got {response}"
