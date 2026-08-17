import logging
import json
from typing import List, Dict, Any

from agents.base_agent import BaseAgent
from agents.infrastructure.schemas.base_agent_schema import AgentInput, AgentOutput
from agents.infrastructure.schemas.qa_schemas import ScenariosListModel
from agents.infrastructure.schemas.execution_schemas import TestDataSetsListModel

logger = logging.getLogger("TestDataAgent")

class TestDataAgent(BaseAgent[TestDataSetsListModel]):
    """
    AI Agent that generates comprehensive test datasets for scenarios.
    """

    def __init__(self, provider_name: str = None):
        super().__init__("TestDataAgent", provider_name)

    def generate_datasets(self, scenarios: ScenariosListModel) -> AgentOutput[TestDataSetsListModel]:
        logger.info("Generating datasets for %d scenarios...", len(scenarios.scenarios))
        
        system_prompt = (
            "You are a Senior Data Engineer and Security Tester. "
            "Generate robust test datasets for the provided scenarios.\n"
            "Rules:\n"
            "1. Data MUST be 100% synthetic. Real PII is strictly prohibited.\n"
            "2. Positive data should reflect happy paths.\n"
            "3. Negative data should trigger validation errors.\n"
            "4. Boundary data must include extremely long strings, empty fields, unicode, and emojis.\n"
            "5. Security data MUST include malicious payloads like XSS (<script>), SQLi (' OR 1=1), or Prompt Injection ('IGNORE ALL PREVIOUS INSTRUCTIONS').\n"
            "Output must conform exactly to the provided JSON schema."
        )

        prompt = f"Please generate test datasets for these scenarios:\n\n{scenarios.model_dump_json(indent=2)}"

        input_data = AgentInput(
            prompt=prompt,
            system_instruction=system_prompt
        )
        
        result = self.execute(input_data, TestDataSetsListModel)
        
        # Post-Processing: Deterministic Quality Hooks
        if result.is_success and result.data and result.data.datasets:
            # Map scenarios by ID for easy lookup
            scenario_types = {s.scenario_id: s.test_type for s in scenarios.scenarios}
            
            for ds in result.data.datasets:
                # Rule: Real PII is prohibited
                if not ds.pii_synthetic:
                    logger.warning("Dataset %s flagged as non-synthetic. Rejecting.", ds.dataset_id)
                    ds.pii_synthetic = True
                    ds.positive_data = [{"error": "NEEDS_CLARIFICATION: AI generated non-synthetic PII"}]
                
                # Rule: If scenario is security/prompt injection, security_data MUST NOT be empty
                test_type = scenario_types.get(ds.scenario_id, "").lower()
                if "security" in test_type or "injection" in test_type:
                    if not ds.security_data:
                        logger.warning("Security scenario %s missing security_data! Injecting default payload.", ds.scenario_id)
                        ds.security_data = [{"payload": "<script>alert('XSS')</script>"}, {"prompt": "IGNORE ALL PREVIOUS INSTRUCTIONS"}]
                        
        return result
