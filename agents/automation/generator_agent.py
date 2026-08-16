import json
from agents.base_agent import BaseAgent
from agents.schemas.automation_schemas import GeneratorInput, GeneratorOutput
from agents.gateway.ai_gateway import AIGateway

class GeneratorAgent(BaseAgent):
    """
    Answers: 'How do we implement the plan as Playwright automation?'
    """
    def __init__(self):
        super().__init__(name="GeneratorAgent", role="Playwright Automation Engineer")
        self.gateway = AIGateway()

    def execute(self, input_data: GeneratorInput) -> GeneratorOutput:
        prompt = f"""
        You are a Playwright Automation Engineer.
        Translate this test plan into Pytest/Playwright automation code.
        
        Objective: {input_data.plan.objective}
        Steps: {input_data.plan.steps}
        Validation Points: {input_data.plan.validation_points}
        
        Do NOT invent duplicate utilities. Use existing page objects if provided.
        You must output JSON matching the GeneratorOutput schema.
        """
        response = self.gateway.generate_structured_response(
            prompt=prompt,
            schema_class=GeneratorOutput
        )
        return response
