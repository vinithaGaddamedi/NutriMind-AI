from agents.base_agent import BaseAgent
from agents.schemas.base_agent_schema import AgentInput, AgentOutput
from agents.automation.planner_agent import PlannerAgent
from agents.automation.generator_agent import GeneratorAgent
from agents.automation.validator_agent import ValidatorAgent
from agents.schemas.automation_schemas import PlannerInput, GeneratorInput, ValidatorInput
from pydantic import BaseModel, Field

class AutomationOrchestratorInput(AgentInput):
    test_scenario: str
    acceptance_criteria: list[str]
    original_requirement: str

class AutomationOrchestratorOutput(AgentOutput):
    pytest_code: str
    coverage_status: str
    plan_objective: str

class AutomationOrchestrator(BaseAgent):
    """
    Orchestrates the entire Automation lifecycle:
    Planner -> Generator -> Validator -> (Execution placeholder) -> (Healer placeholder)
    """
    def __init__(self):
        super().__init__(name="AutomationOrchestrator", role="Automation Director")
        self.planner = PlannerAgent()
        self.generator = GeneratorAgent()
        self.validator = ValidatorAgent()

    def execute(self, input_data: AutomationOrchestratorInput) -> AutomationOrchestratorOutput:
        # 1. Invoke Planner
        planner_input = PlannerInput(
            test_scenario=input_data.test_scenario,
            acceptance_criteria=input_data.acceptance_criteria
        )
        plan_output = self.planner.execute(planner_input)
        
        # 2. Invoke Generator
        generator_input = GeneratorInput(
            plan=plan_output,
            existing_page_objects=[]
        )
        gen_output = self.generator.execute(generator_input)
        
        # 3. Invoke Validator
        val_input = ValidatorInput(
            generated_code=gen_output.pytest_code,
            original_requirement=input_data.original_requirement
        )
        val_output = self.validator.execute(val_input)
        
        return AutomationOrchestratorOutput(
            pytest_code=gen_output.pytest_code,
            coverage_status=val_output.coverage_status,
            plan_objective=plan_output.objective
        )
