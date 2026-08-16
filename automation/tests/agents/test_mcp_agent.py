import pytest
import sys
import os
from playwright.sync_api import sync_playwright

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from agents.infrastructure.mcp_playwright_agent import MCPPlaywrightAgent

@pytest.fixture(scope="module")
def browser_page():
    # Provide a simple local mock HTML page if no server is running
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # We will mock the content dynamically in the test or navigate to a dummy page
        yield page
        browser.close()

def test_mcp_agent_execution_loop(browser_page):
    """
    Validates that the MCP agent correctly parses tool execution and captures telemetry.
    """
    agent = MCPPlaywrightAgent(page=browser_page)
    
    # We test the mocked execution loop to prevent breaking CI when API key is missing
    # but still assert the state tracking logic.
    os.environ["MOCK_LLM_EVALS"] = "true"
    
    result = agent.run_objective("Verify that a user can create a vegetarian meal plan.")
    
    assert result["success"] is True
    assert "reason" in result
    assert len(result["telemetry"]) > 0
    
    # Verify telemetry captured tool calls
    tool_names = [t["tool_name"] for t in result["telemetry"]]
    assert "navigate" in tool_names
    assert "click" in tool_names
    assert "finish_task" in tool_names
    
    # Verify success flags in telemetry
    for t in result["telemetry"]:
        assert "success" in t
        assert "timestamp" in t
        assert "arguments" in t
