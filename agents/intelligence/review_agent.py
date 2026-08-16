import logging
import json

from agents.base_agent import BaseAgent
from agents.schemas.base_agent_schema import AgentInput, AgentOutput
from agents.schemas.execution_schemas import AutomationTest
from agents.schemas.qa_schemas import ReviewAnalysis

logger = logging.getLogger("ReviewAgent")

class ReviewAgent(BaseAgent[ReviewAnalysis]):
    """
    AI Agent that reviews generated Playwright code to ensure enterprise framework compliance.
    """

    def __init__(self, provider_name: str = None):
        super().__init__("ReviewAgent", provider_name)

    def review_code(self, automation_test: AutomationTest) -> AgentOutput[ReviewAnalysis]:
        logger.info("Reviewing code for test_case_id: %s", automation_test.test_case_id)
        
        system_prompt = (
            "You are a strict QA Automation Code Reviewer. Review the provided Playwright Pytest code.\n"
            "Fail the review (is_approved=False) if any of the following are true:\n"
            "1. It uses hardcoded waits (e.g. time.sleep).\n"
            "2. It uses direct locators (page.locator, page.click) instead of the Page Object Model.\n"
            "3. It is missing strict assertions (expect).\n"
            "4. It is missing traceability decorators (@pytest.mark.story_id, etc).\n"
            "5. It contains hardcoded credentials or API keys.\n"
            "If approved, set is_approved=True and score > 0.8.\n"
            "If rejected, set is_approved=False, score < 0.8, and explicitly list suggested_fixes.\n"
            "Output must strictly match the JSON schema."
        )

        prompt = f"Please review this AutomationTest code:\n\n{automation_test.model_dump_json(indent=2)}"

        input_data = AgentInput(
            prompt=prompt,
            system_instruction=system_prompt
        )
        
        result = self.execute(input_data, ReviewAnalysis)
        
        # Deterministic Verification
        if result.is_success and result.data:
            # Deterministic override: if 'time.sleep' is in the code, but the AI approved it, reject it!
            if "time.sleep" in automation_test.code and result.data.is_approved:
                logger.error("AI incorrectly approved code with time.sleep. Overriding to reject.")
                result.data.is_approved = False
                result.data.score = 0.0
                result.data.suggested_fixes.append("Remove time.sleep and use Playwright auto-waiting.")
                
            # Deterministic override: if 'page.locator' is in code, reject it
            if "page.locator" in automation_test.code and result.data.is_approved:
                logger.error("AI incorrectly approved code with direct locators. Overriding to reject.")
                result.data.is_approved = False
                result.data.score = 0.0
                result.data.suggested_fixes.append("Use Page Object Model instead of direct page locators.")
                
        return result
