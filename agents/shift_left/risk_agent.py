import sys
import os
import json
import logging
from typing import Dict, Any, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../automation")))

from agents.base_agent import BaseAgent
from agents.infrastructure.schemas.base_agent_schema import AgentInput, AgentOutput
from agents.infrastructure.schemas.requirement_schema import RequirementAnalysis
from agents.infrastructure.schemas.qa_schemas import RiskAnalysis

logger = logging.getLogger("RiskAgent")

class RiskAgent(BaseAgent[RiskAnalysis]):
    """
    AI Agent that performs risk analysis on requirements.
    """
    
    def __init__(self, provider_name: str = None):
        super().__init__("RiskAgent", provider_name)

    def evaluate_risks(self, req: RequirementAnalysis) -> AgentOutput[RiskAnalysis]:
        logger.info("Evaluating quality risks for story %s...", req.story_id)
        
        system_prompt = (
            "You are a Senior QA Risk Assessor. Evaluate the risks for the provided requirement. "
            "Identify comprehensive risk scenarios across categories: functional, integration, security, "
            "data, performance, accessibility, AI/LLM, privacy, business-critical.\n\n"
            "For NutriMind specifically, actively analyze and surface risks related to:\n"
            "- allergy violations\n"
            "- dietary violations\n"
            "- incorrect nutritional calculations\n"
            "- hallucinated nutrition information\n"
            "- unsafe recommendations\n"
            "- user preference loss\n"
            "- chatbot context loss\n"
            "- API failures\n"
            "- incorrect pantry data\n\n"
            "Do not assume a risk exists without evidence from the requirement.\n"
            "Output must strictly conform to the provided JSON schema."
        )

        prompt = f"Please analyze the following requirement and generate a RiskAnalysis:\n\n{req.model_dump_json(indent=2)}\n"

        input_data = AgentInput(
            prompt=prompt,
            system_instruction=system_prompt
        )
        
        result = self.execute(input_data, RiskAnalysis)
        
        # Deterministic validation hook
        if result.is_success and result.data:
            for risk in result.data.risks:
                desc_lower = risk.description.lower()
                cat_lower = risk.category.lower()
                
                # Rule 1: Allergy or severe dietary violations are Critical
                if "allergy" in desc_lower or "allergies" in desc_lower or "unsafe recommendation" in desc_lower:
                    risk.severity = "Critical"
                    risk.priority = "P0"
                
                # Rule 2: Nutritional hallucinations are High/Critical
                if "hallucinat" in desc_lower and ("nutrition" in desc_lower or "calorie" in desc_lower):
                    if risk.severity not in ["Critical", "High"]:
                        risk.severity = "High"
                    if risk.priority not in ["P0", "P1"]:
                        risk.priority = "P1"
                        
        return result
