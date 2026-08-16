import sys
import os
import json
import logging
from typing import Dict, Any, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.base_agent import BaseAgent
from agents.schemas.base_agent_schema import AgentInput, AgentOutput
from agents.schemas.traceability_schemas import TraceabilityReport

logger = logging.getLogger("TraceabilityAgent")

class TraceabilityAgent(BaseAgent[TraceabilityReport]):
    """
    Analyzes the entire QA ecosystem to build a Requirements Traceability Matrix (RTM).
    Identifies orphaned nodes, un-automated high-risk items, and computes coverage metrics.
    """
    def __init__(self, provider_name: str = None):
        super().__init__("TraceabilityAgent", provider_name)

    def generate_rtm(self, raw_ecosystem_data: List[Dict[str, Any]]) -> AgentOutput[TraceabilityReport]:
        logger.info("Generating Requirements Traceability Matrix from %d nodes...", len(raw_ecosystem_data))
        
        system_prompt = (
            "You are an expert QA Traceability Agent. You will receive a list of nodes representing "
            "items in the SDLC (Requirements, Risks, Scenarios, Automation, Goldens, Defects). "
            "Analyze the entire graph to connect the dots. "
            "You must output a strictly structured JSON TraceabilityReport. "
            "Calculate 'CoverageMetrics' based on the percentage of Requirements that trace all the way "
            "down to at least one AutomationTest, grouped by their 'severity' (Critical, High, Medium, Low). "
            "In the 'gaps' section, explicitly identify the IDs of: "
            "1) requirements_without_tests "
            "2) high_risk_without_automation (severity High/Critical with no linked automation) "
            "3) tests_without_requirements "
            "4) goldens_without_requirements "
            "5) automation_without_test_cases "
            "6) defects_without_test_coverage "
            "Pass all input nodes through to the 'nodes' array."
        )

        prompt = f"""
        Raw Ecosystem Data:
        {json.dumps(raw_ecosystem_data, indent=2)}
        """
        
        input_data = AgentInput(
            prompt=prompt,
            system_instruction=system_prompt
        )
        return self.execute(input_data, TraceabilityReport)
