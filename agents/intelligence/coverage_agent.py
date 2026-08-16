import sys
import os
import json
import logging
from typing import Dict, Any, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.base_agent import BaseAgent
from agents.schemas.base_agent_schema import AgentInput, AgentOutput
from agents.schemas.coverage_schemas import CoverageReport

logger = logging.getLogger("CoverageAgent")

class CoverageAgent(BaseAgent[CoverageReport]):
    """
    Intelligent auditor that evaluates true test coverage.
    Coverage is strictly based on traceability AND execution success, not just existence.
    """
    def __init__(self, provider_name: str = None):
        super().__init__("CoverageAgent", provider_name)

    def analyze_coverage(self, traceability_data: List[Dict[str, Any]]) -> AgentOutput[CoverageReport]:
        logger.info("Analyzing coverage across %d trace nodes...", len(traceability_data))
        
        system_prompt = (
            "You are an expert QA Coverage Agent. "
            "You will receive a graph of SDLC trace nodes (Requirements, Risks, Tests, Executions). "
            "Your objective is to calculate strict coverage metrics and propose recommendations. "
            "CRITICAL RULE: Coverage must be based on traceability AND execution. "
            "If a TestScenario exists but has no linked Execution that 'passed', it contributes 0% to coverage. "
            "Break down your percentages by severity (critical, high, medium, low). "
            "Identify explicit gaps (e.g., 'MISSING_AI_BEHAVIOR_TEST', 'UNEXECUTED_TEST') and provide actionable recommendations."
        )

        prompt = f"""
        Ecosystem Data:
        {json.dumps(traceability_data, indent=2)}
        """
        
        input_data = AgentInput(
            prompt=prompt,
            system_instruction=system_prompt
        )
        return self.execute(input_data, CoverageReport)
