import json
from agents.base_agent import BaseAgent
from agents.infrastructure.schemas.automation_schemas import ValidatorInput, ValidatorOutput
from agents.providers.ai_gateway import AIGateway

class ValidatorAgent(BaseAgent):
    """
    Answers: 'Does the generated automation actually test the requirement?'
    """
    def __init__(self):
        super().__init__(agent_name="ValidatorAgent")
        self.gateway = AIGateway()

    def execute(self, input_data: ValidatorInput) -> ValidatorOutput:
        prompt = f"""
        You are an Automation QA Validator.
        Analyze the generated Playwright code to ensure it truly tests the original requirement.
        
        Requirement: {input_data.original_requirement}
        Generated Code:
        {input_data.generated_code}
        
        Identify what is covered and what is missing. Do not let false positives pass.
        You must output JSON matching the ValidatorOutput schema.
        """
        response = self.gateway.generate_structured_response(
            prompt=prompt,
            schema_class=ValidatorOutput
        )
        return response
