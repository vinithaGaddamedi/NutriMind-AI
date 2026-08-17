import os
import sys
import logging
from typing import Dict, Any

from agents.base_agent import BaseAgent
from agents.infrastructure.schemas.base_agent_schema import AgentInput, AgentOutput, AgentError
from agents.infrastructure.schemas.execution_schemas import AutomationTest, ManualTestCase, TestDataSet

logger = logging.getLogger("AutomationAgent")

class AutomationAgent(BaseAgent[AutomationTest]):
    """
    AI Agent that generates Python Playwright test scripts.
    """

    def __init__(self, provider_name: str = None):
        super().__init__("AutomationAgent", provider_name)

    def generate_playwright_test(self, test_case: ManualTestCase, dataset: TestDataSet) -> AgentOutput[AutomationTest]:
        logger.info("Generating Playwright Python test for %s...", test_case.test_case_id)

        skill_file = os.path.join(os.path.dirname(__file__), "..", "..", ".agents", "skills", "generator", "SKILL.md")
        skill_rules = ""
        if os.path.exists(skill_file):
            try:
                with open(skill_file, "r") as f:
                    skill_rules = f.read()
            except Exception:
                pass

        system_prompt = (
            "You are a Senior SDET. Generate complete, executable Playwright Python test code using pytest.\n"
            f"Adhere strictly to these framework rules:\n{skill_rules}\n"
            "CRITICAL RULES:\n"
            "1. MUST use Page Object Model (POM). Do not use direct page.locator() or page.click() inside the test file.\n"
            "2. MUST include traceability decorators: @pytest.mark.story_id('...'), @pytest.mark.requirement('...'), @pytest.mark.scenario_id('...').\n"
            "3. MUST use robust Playwright `expect` assertions.\n"
            "4. MUST NOT use time.sleep().\n"
            "Output ONLY valid Python code inside the AutomationTest schema. Do not output markdown around the JSON."
        )

        prompt = f"""Test Case:\n{test_case.model_dump_json(indent=2)}\n\nDataset:\n{dataset.model_dump_json(indent=2)}\n\nGenerate Pytest Playwright code reusing existing Page Objects."""

        input_data = AgentInput(
            prompt=prompt,
            system_instruction=system_prompt
        )
        
        result = self.execute(input_data, AutomationTest)
        
        # Deterministic Quality Hook
        if result.is_success and result.data:
            # Inject trace IDs automatically from inputs to ensure they match perfectly
            result.data.story_id = test_case.story_id
            result.data.requirement_id = test_case.requirement_id
            result.data.scenario_id = test_case.scenario_id
            
            code = result.data.code
            if "time.sleep" in code:
                logger.error("AI generated time.sleep(). Rejecting code.")
                result.error = AgentError(error_code="HARDCODED_WAIT", message="AI generated prohibited hardcoded wait (time.sleep).")
                result.data = None
                
        return result
