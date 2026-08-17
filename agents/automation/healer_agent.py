import json
from agents.base_agent import BaseAgent
from agents.infrastructure.schemas.healer_schemas import HealerInput, HealerOutput
from agents.providers.ai_gateway import AIGateway

class HealerAgent(BaseAgent):
    """
    Answers: 'Can we safely repair the automation?'
    """
    def __init__(self):
        super().__init__(agent_name="HealerAgent")
        self.gateway = AIGateway()

    def execute(self, input_data: HealerInput) -> HealerOutput:
        prompt = f"""
        You are an AI Self-Healing Expert.
        A Playwright test has failed due to a locator mismatch.
        
        Old Locator: {input_data.old_locator}
        Error: {input_data.error_message}
        DOM Snapshot Snippet: {input_data.dom_snapshot}
        
        Analyze the DOM and propose a new locator. Calculate your confidence.
        You must output JSON matching the HealerOutput schema.
        """
        response = self.gateway.generate_structured_response(
            prompt=prompt,
            schema_class=HealerOutput
        )
        return response
