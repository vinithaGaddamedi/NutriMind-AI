import sys
import os
import json
import logging
from typing import Dict, Any, Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.base_agent import BaseAgent
from agents.infrastructure.schemas.base_agent_schema import AgentInput, AgentOutput
from agents.infrastructure.schemas.evaluation_schemas import ChatbotGolden

logger = logging.getLogger("GoldenLearningAgent")

class GoldenLearningAgent(BaseAgent[ChatbotGolden]):
    """
    Ingests confirmed defect/RCA reports and converts them into Regression Goldens.
    """
    def __init__(self, provider_name: str = None):
        super().__init__("GoldenLearningAgent", provider_name)

    def generate_regression_golden(self, rca_report: Dict[str, Any], conversation_history: list) -> AgentOutput[ChatbotGolden]:
        logger.info("Generating regression golden from RCA: %s", rca_report.get('test_case_id'))
        
        system_prompt = (
            "You are a Quality Engineering Golden Learning Agent. "
            "You receive a Root Cause Analysis (RCA) report and the original conversation. "
            "Your job is to generate a `ChatbotGolden` schema scenario (Category must be 'multi-turn' or 'regression') "
            "that captures the defect. Set the golden_id to start with 'CHAT-REG-'. "
            "Ensure you explicitly define 'expected_behavior' and 'forbidden_behavior' to prevent "
            "this exact defect from ever recurring in the future."
        )

        prompt = f"""RCA Report:
{json.dumps(rca_report, indent=2)}

Original Conversation Context:
{json.dumps(conversation_history, indent=2)}
"""
        
        input_data = AgentInput(
            prompt=prompt,
            system_instruction=system_prompt
        )
        return self.execute(input_data, ChatbotGolden)

def stage_regression_golden(golden: ChatbotGolden, staging_file: str):
    """
    Saves the new golden to a staging file.
    Does NOT automatically add unreviewed goldens to the official suite.
    """
    os.makedirs(os.path.dirname(staging_file), exist_ok=True)
    
    if os.path.exists(staging_file):
        with open(staging_file, "r") as f:
            data = json.load(f)
    else:
        data = {"goldens": []}
        
    data["goldens"].append(golden.model_dump())
    
    with open(staging_file, "w") as f:
        json.dump(data, f, indent=2)
        
    logger.info(f"Staged new regression golden {golden.golden_id} at {staging_file}")
