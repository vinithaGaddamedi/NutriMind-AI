import sys
import os
import json
import logging
from typing import Dict, Any, Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../automation")))

from agents.base_agent import BaseAgent
from agents.schemas.base_agent_schema import AgentInput, AgentOutput
from agents.schemas.qa_schemas import FailureAnalysis, FailureClassification

logger = logging.getLogger("FailureAgent")

FAILURE_TAXONOMY = [f.value for f in FailureClassification]

class FailureAgent(BaseAgent[FailureAnalysis]):
    """
    AI Agent for failure analysis and root cause detection.
    """

    def __init__(self, provider_name: str = None):
        super().__init__("FailureAgent", provider_name)

    def classify_and_analyze(
        self,
        test_case_id: str,
        error_message: str,
        stack_trace: str,
        page_dom: Optional[str] = None
    ) -> AgentOutput[FailureAnalysis]:
        logger.info("Classifying failure for test '%s'...", test_case_id)

        system_prompt = (
            "You are an expert Failure Classification and Root Cause Analysis (RCA) Agent. "
            f"Classify test failures into one of these exact taxonomy types: {', '.join(FAILURE_TAXONOMY)}. "
            "Output JSON with fields: test_case_id, failure_type, root_cause, evidence, confidence, "
            "recommended_action, and requires_human_review. "
            "CRITICAL: Do not invent root cause when evidence is insufficient. Return NEEDS_MORE_EVIDENCE as the failure_type."
        )

        prompt = f"""Test Name: {test_case_id}
Error Message: {error_message}
Stack Trace: {stack_trace}
"""
        if not error_message and not stack_trace and not page_dom:
            # Force needs more evidence if strictly empty
            pass
        if page_dom:
            prompt += f"Page DOM Snippet: ```html\n{page_dom[:4000]}\n```\n"

        input_data = AgentInput(
            prompt=prompt,
            system_instruction=system_prompt
        )
        return self.execute(input_data, FailureAnalysis)
