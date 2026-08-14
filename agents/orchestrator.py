import sys
import os
import json
import logging
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../automation")))

from agents.requirement_agent import RequirementAgent
from agents.risk_agent import RiskAgent
from agents.test_design_agent import TestDesignAgent
from agents.manual_test_agent import ManualTestAgent
from agents.automation_agent import AutomationAgent
from agents.failure_agent import FailureAgent
from agents.self_healing_agent import SelfHealingPatchAgent
from agents.jira_agent import JiraAgent
from agents.reporting_agent import ReportingAgent
from agents.mcp_server import NutriMindMCPServer

logger = logging.getLogger("NutriMindOrchestrator")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

class MasterOrchestrator:
    """
    Master Orchestrator coordinating all autonomous QA agents across the lifecycle.
    """

    def __init__(self):
        self.req_agent = RequirementAgent()
        self.risk_agent = RiskAgent()
        self.design_agent = TestDesignAgent()
        self.manual_agent = ManualTestAgent()
        self.auto_agent = AutomationAgent()
        self.failure_agent = FailureAgent()
        self.patch_agent = SelfHealingPatchAgent()
        self.jira_agent = JiraAgent()
        self.reporting_agent = ReportingAgent()
        self.mcp_server = NutriMindMCPServer()

    def run_pipeline(self, story_id: str, title: str, description: str) -> Dict[str, Any]:
        logger.info("=== STARTING NUTRIMIND AGENTIC QA PIPELINE ===")

        # 1. Requirement Analysis
        req_model = self.req_agent.analyze_jira_story(story_id, title, description)

        # 2. Risk Evaluation
        risk_matrix = self.risk_agent.evaluate_risks(req_model)

        # 3. Test Scenario Design
        scenarios = self.design_agent.generate_scenarios(req_model)

        # 4. Manual Test Generation & Export
        manual_tests = self.manual_agent.generate_manual_test_cases(scenarios)
        self.manual_agent.export_to_csv(manual_tests, "reports/manual-test-cases.csv")

        # 5. Automation Code Generation
        auto_code = self.auto_agent.generate_playwright_test(manual_tests[0])

        # 6. Failure Analysis & Jira Defect Simulation
        failure_analysis = self.failure_agent.classify_and_analyze(
            test_name="test_meal_planner_001",
            error_message="TimeoutError: Locator button:has-text('Proceed') not found",
            stack_trace="Traceback line 42 in test_meal_planner.py",
            page_dom="<div><button id='proceed-pantry'>Proceed to Pantry</button></div>"
        )

        patch_proposal = self.patch_agent.propose_patch(
            file_path="automation/ui_tests/pages/locators/locators.py",
            old_selector="button:has-text('Proceed')",
            new_selector="button#proceed-pantry"
        )

        jira_defect = self.jira_agent.format_defect_payload(
            story_id=story_id,
            test_case_id=manual_tests[0]["test_case_id"],
            environment="QA",
            steps=manual_tests[0]["steps"],
            expected=manual_tests[0]["expected_result"],
            actual="Timeout waiting for proceed button",
            analysis=failure_analysis
        )

        # 7. Generate All Reports
        self.reporting_agent.generate_all_reports(
            manual_test_cases=manual_tests,
            failure_analyses=[failure_analysis],
            deepeval_metrics={"relevance": 0.94, "faithfulness": 0.91, "safety": 0.97, "diet_compliance": 0.99}
        )

        logger.info("=== NUTRIMIND AGENTIC QA PIPELINE COMPLETED SUCCESSFULLY ===")
        return {
            "requirement": req_model.model_dump(),
            "risks": risk_matrix,
            "manual_test_count": len(manual_tests),
            "jira_defect_summary": jira_defect["summary"],
            "patch_proposal": patch_proposal["status"]
        }

if __name__ == "__main__":
    orchestrator = MasterOrchestrator()
    result = orchestrator.run_pipeline(
        story_id="MEAL-101",
        title="AI Meal Planner High Protein Vegetarian Selection",
        description="As a health-conscious user, I want the AI Meal Planner to generate 7-day vegetarian plans matching protein requirements."
    )
    print("\n" + "="*60)
    print("🤖 PIPELINE RUN RESULT SUMMARY:")
    print(json.dumps(result, indent=2))
    print("="*60)
