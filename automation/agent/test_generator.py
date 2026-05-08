import json

def generate_test_cases(ai_response):
    try:
        return json.loads(ai_response)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON from AI"}

def generate_ui_test(test_case):
    return f"""
def test_{test_case.get('name', 'generated_ui')}(page):
    page.goto("http://localhost:5173")
    page.fill("input[name='email']", "{test_case.get('email', '')}")
    page.click("text=Submit")
    page.wait_for_timeout(1000)
"""

def generate_api_test(test_case):
    return f"""
def test_api_{test_case.get('name', 'generated_api')}():
    response = requests.post(
        "http://localhost:8000/api",
        json={test_case.get("payload", {{}})}
    )
    assert response.status_code == {test_case.get("expected_status", 200)}
"""
