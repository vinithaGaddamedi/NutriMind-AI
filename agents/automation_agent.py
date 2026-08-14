import os
import sys
import logging
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../automation")))

from agent.providers.factory import AIProviderFactory

logger = logging.getLogger("AutomationAgent")

class AutomationAgent:
    """
    Transforms candidate manual test cases into executable Pytest Playwright code
    following Page Object Model guidelines in .ai/skills/playwright/SKILL.md.
    """

    def __init__(self, provider_name: str = None):
        self.provider = AIProviderFactory.get_provider(provider_name)

    def generate_playwright_test(self, test_case: Dict[str, Any]) -> str:
        logger.info("Generating Playwright Python test for %s...", test_case.get("test_case_id"))

        skill_file = os.path.join(os.path.dirname(__file__), "..", ".ai", "skills", "playwright", "SKILL.md")
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
            "Output ONLY valid Python code inside ```python ``` block."
        )

        prompt = f"""Test Case ID: {test_case.get('test_case_id')}
Title: {test_case.get('title')}
Type: {test_case.get('type')}
Steps: {test_case.get('steps')}
Expected Result: {test_case.get('expected_result')}

Generate Pytest Playwright code reusing existing Page Objects."""

        code = self.provider.generate_text(prompt, system_instruction=system_prompt)
        return code
