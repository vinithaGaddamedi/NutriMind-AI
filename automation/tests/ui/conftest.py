import pytest
import allure
import sys
import os

from agents.intelligence.failure_agent import FailureAgent

analyzer = FailureAgent()

def analyze_failure(error_message, stack_trace, page_dom=None, test_name="test"):
    try:
        res = analyzer.classify_and_analyze(
            test_case_id=test_name,
            error_message=error_message,
            stack_trace=stack_trace,
            page_dom=page_dom
        )
        if res.is_success:
            data = res.data
            return (
                f"### 🤖 AI Failure Analysis\n"
                f"- **Test Case ID:** {data.test_case_id}\n"
                f"- **Failure Type:** `{data.failure_type}`\n"
                f"- **Root Cause:** {data.root_cause}\n"
                f"- **Evidence:** {data.evidence}\n"
                f"- **Recommended Action:** {data.recommended_action}\n"
                f"- **Confidence:** {data.confidence * 100:.1f}%\n"
                f"- **Requires Human Review:** {data.requires_human_review}\n"
            )
        else:
            return f"AI Analysis failed: {res.error.message if res.error else 'Unknown error'}"
    except Exception as e:
        return f"AI Analysis skipped or failed: {str(e)}"


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
        
        analysis_result = analyze_failure(
            error_message=error_message,
            stack_trace=error_message,
            page_dom=dom_content,
            test_name=item.name
        )
        
        print(analysis_result)
        print("="*50 + "\n")
        
        # Attach AI analysis to Allure Report
        allure.attach(
            analysis_result,
            name="🤖 AI Failure Analysis",
            attachment_type=allure.attachment_type.TEXT
        )
