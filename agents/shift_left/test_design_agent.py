import sys
import os
import json
import logging
from typing import Dict, Any, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../automation")))

from agents.base_agent import BaseAgent
from agents.schemas.base_agent_schema import AgentInput, AgentOutput
from agents.schemas.requirement_schema import RequirementAnalysis
from agents.schemas.qa_schemas import ScenariosListModel, RiskAnalysis

logger = logging.getLogger("TestDesignAgent")

class TestDesignAgent(BaseAgent[ScenariosListModel]):
    """
    AI Agent that generates Test Scenarios.
    """
    
    def __init__(self, provider_name: str = None):
        super().__init__("TestDesignAgent", provider_name)

    def generate_scenarios(self, req: RequirementAnalysis, risk: RiskAnalysis = None) -> AgentOutput[ScenariosListModel]:
        logger.info("Generating test scenarios for story %s...", req.story_id)
        
        system_prompt = (
            "You are a Senior Test Architect. Generate a comprehensive set of test scenarios "
            "for the provided requirements and risk matrix.\n"
            "Scenarios must cover: positive, negative, boundary, validation, integration, API, UI, "
            "accessibility, security, AI behavior, hallucination, prompt injection, "
            "conversation/memory, error handling, and regression.\n"
            "Rules:\n"
            "1. Avoid duplicate scenarios.\n"
            "2. Map scenarios to specific risk_id where applicable.\n"
            "3. If mapping to a critical risk, the scenario priority must reflect that criticality.\n"
            "4. Provide exact preconditions, test data, and expected behavior.\n"
            "Output must strictly conform to the provided JSON schema."
        )

        prompt = f"Please analyze the following Requirement and Risk matrix and generate a comprehensive ScenariosListModel:\n\nRequirement:\n{req.model_dump_json(indent=2)}\n"
        if risk:
            prompt += f"\nRisk Matrix:\n{risk.model_dump_json(indent=2)}\n"

        input_data = AgentInput(
            prompt=prompt,
            system_instruction=system_prompt
        )
        result = self.execute(input_data, ScenariosListModel)
        
        # Post-Processing: Risk-based prioritization and Duplicate Detection
        if result.is_success and result.data and result.data.scenarios:
            unique_scenarios = []
            seen_titles = set()
            
            # Map risk priorities for easy lookup
            risk_priority_map = {}
            if risk:
                for r in risk.risks:
                    risk_priority_map[r.risk_id] = r.priority
                    
            for scenario in result.data.scenarios:
                # Basic duplicate detection by title string comparison
                title_lower = scenario.title.lower().strip()
                if title_lower in seen_titles:
                    logger.warning("Duplicate scenario detected and removed: %s", scenario.title)
                    continue
                seen_titles.add(title_lower)
                
                # Risk-based Prioritization Hook
                if scenario.risk_id != "NONE" and scenario.risk_id in risk_priority_map:
                    linked_priority = risk_priority_map[scenario.risk_id]
                    if linked_priority in ["P0", "P1"]:
                        if scenario.priority not in ["Critical", "High"]:
                            scenario.priority = "Critical" if linked_priority == "P0" else "High"
                            
                unique_scenarios.append(scenario)
                
            result.data.scenarios = unique_scenarios
            
        return result
