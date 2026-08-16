import sys
import os
import json
import logging
from typing import Dict, Any, Optional

# Ensure automation and agents directories are accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../automation")))

from agents.base_agent import BaseAgent
from agents.infrastructure.schemas.base_agent_schema import AgentInput, AgentOutput
from agents.infrastructure.schemas.requirement_schema import RequirementAnalysis

logger = logging.getLogger("RequirementAgent")

class RequirementAgent(BaseAgent[RequirementAnalysis]):
    """
    Agent responsible for translating Jira Stories into structured requirement models.
    """

    def __init__(self, provider_name: str = None):
        super().__init__("RequirementAgent", provider_name)

    def analyze_jira_story(
        self, 
        story_id: str, 
        title: str, 
        description: str, 
        acceptance_criteria: str, 
        comments: Optional[str] = None
    ) -> AgentOutput[RequirementAnalysis]:
        logger.info("Analyzing Jira Story %s: '%s'", story_id, title)
        
        system_prompt = (
            "You are a Senior Business Analyst and Test Architect. "
            "Analyze raw Jira stories and extract structured requirement JSON. "
            "You MUST follow these rules:\n"
            "1. Do not invent requirements.\n"
            "2. Preserve exact acceptance criteria.\n"
            "3. Distinguish explicit requirements from your own AI interpretation.\n"
            "4. Identify ambiguity and explicitly list it.\n"
            "5. Identify missing acceptance criteria or information.\n"
            "6. Generate requirement IDs where applicable.\n"
            "7. Maintain traceability.\n"
            "Output ONLY valid JSON matching the schema."
        )

        prompt = f"""Jira Story ID: {story_id}
Title: {title}
Description: {description}
Acceptance Criteria: {acceptance_criteria}
"""
        if comments:
            prompt += f"Comments: {comments}\n"
            
        prompt += "\nExtract structured requirement output in JSON format."

        input_data = AgentInput(
            prompt=prompt,
            system_instruction=system_prompt
        )
        return self.execute(input_data, RequirementAnalysis)

