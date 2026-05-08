import pytest
import allure
import sys
import os

# Add agent folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from agent.analyzer import AIFailureAnalyzer

analyzer = AIFailureAnalyzer()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        # Check if 'page' fixture is available
        page = item.funcargs.get("page", None)
        dom_content = None
        if page:
            try:
                # Take screenshot for Allure
                screenshot = page.screenshot(full_page=True)
                allure.attach(screenshot, name="failure_screenshot", attachment_type=allure.attachment_type.PNG)
                
                # Grab DOM
                dom_content = page.content()
            except Exception as e:
                print(f"Failed to capture page state: {e}")

        error_message = str(rep.longreprtext) if hasattr(rep, 'longreprtext') and rep.longreprtext else str(rep.longrepr)
        
        print("\n" + "="*50)
        print("🤖 INITIATING AI TEST FAILURE ANALYSIS...")
        
        analysis_result = analyzer.analyze_failure(
            error_message=error_message,
            stack_trace=error_message,
            page_dom=dom_content
        )
        
        print(analysis_result)
        print("="*50 + "\n")
        
        # Attach AI analysis to Allure Report
        allure.attach(
            analysis_result,
            name="🤖 AI Failure Analysis",
            attachment_type=allure.attachment_type.TEXT
        )
