import json
from agents.base_agent import BaseAgent
from agents.schemas.automation_schemas import PlannerInput, PlannerOutput
from agents.gateway.ai_gateway import AIGateway

class PlannerAgent(BaseAgent):
    """
    Answers: 'What should Playwright do to accomplish the approved test objective?'
    """
    def __init__(self):
        super().__init__(name="PlannerAgent", role="Automation Test Planner")
        self.gateway = AIGateway()

    def execute(self, input_data: PlannerInput) -> PlannerOutput:
        prompt = f"""
        You are a Test Automation Planner. Do NOT generate Playwright code.
        Create a detailed, step-by-step plan for the following scenario.
        
        Scenario: {input_data.test_scenario}
        Acceptance Criteria: {input_data.acceptance_criteria}
        
        You must output JSON matching the PlannerOutput schema.
        """
        response = self.gateway.generate_structured_response(
            prompt=prompt,
            schema_class=PlannerOutput
        )
        return response
