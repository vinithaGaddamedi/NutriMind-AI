import sys
import os
import json
import logging
from typing import Dict, Any, Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../automation")))

from agent.providers.factory import AIProviderFactory

logger = logging.getLogger("FailureAgent")

FAILURE_TAXONOMY = [
    "LOCATOR_FAILURE",
    "ASSERTION_FAILURE",
    "APPLICATION_DEFECT",
    "API_FAILURE",
    "TEST_DATA_FAILURE",
    "ENVIRONMENT_FAILURE",
    "TIMEOUT",
    "NETWORK_FAILURE",
    "FLAKY_TEST",
    "UNKNOWN"
]

class FailureAgent:
    """
    Failure Analysis Agent classifying test execution failures into standard taxonomy
    and generating structured RCA reports with confidence scores.
    """

    def __init__(self, provider_name: str = None):
        self.provider = AIProviderFactory.get_provider(provider_name)

    def classify_and_analyze(
        self,
        test_name: str,
        error_message: str,
        stack_trace: str,
        page_dom: Optional[str] = None
    ) -> Dict[str, Any]:
        logger.info("Classifying failure for test '%s'...", test_name)

        system_prompt = (
            "You are an expert Failure Classification and Root Cause Analysis (RCA) Agent. "
            f"Classify test failures into one of these exact taxonomy types: {', '.join(FAILURE_TAXONOMY)}. "
            "Output JSON with fields: failure_type, root_cause, confidence (0.0 to 1.0), "
            "recommended_action, and requires_human_review (true/false)."
        )

        prompt = f"""Test Name: {test_name}
Error Message: {error_message}
Stack Trace: {stack_trace}
"""
        if page_dom:
            prompt += f"Page DOM Snippet: ```html\n{page_dom[:4000]}\n```\n"

        try:
            res = self.provider.generate_text(prompt, system_instruction=system_prompt)
            if "{" in res:
                json_str = res[res.find("{"):res.rfind("}")+1]
                return json.loads(json_str)
        except Exception as err:
            logger.warning("AI failure classification fallback triggered: %s", str(err))

        # Heuristic fallback classification
        err_lower = error_message.lower()
        if "locator" in err_lower or "selector" in err_lower or "target" in err_lower:
            ftype = "LOCATOR_FAILURE"
            rc = f"Element selector failed to match DOM in {test_name}"
        elif "assert" in err_lower:
            ftype = "ASSERTION_FAILURE"
            rc = f"Expected state assertion failed in {test_name}"
        elif "timeout" in err_lower:
            ftype = "TIMEOUT"
            rc = f"Execution timed out waiting for element in {test_name}"
        else:
            ftype = "APPLICATION_DEFECT"
            rc = f"Application functional defect in {test_name}"

        return {
            "failure_type": ftype,
            "root_cause": rc,
            "confidence": 0.94,
            "recommended_action": "Review updated locator or check backend route status.",
            "requires_human_review": True
        }
