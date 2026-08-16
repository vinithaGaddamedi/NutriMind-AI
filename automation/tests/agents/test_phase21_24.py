import os
import sys
import json
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from automation.utils.mcp_evaluator import MCPEvaluator
from agents.intelligence.failure_agent import FailureAgent
from automation.utils.self_healing_service import SelfHealingService
from agents.intelligence.golden_learning_agent import GoldenLearningAgent, stage_regression_golden
from agents.infrastructure.schemas.evaluation_schemas import ChatbotGolden

def test_mcp_evaluator():
    evaluator = MCPEvaluator()
    golden = {
        "expected_success": True,
        "forbidden_tools": ["execute_sql"],
        "expected_trajectory": [{"tool_name": "navigate"}]
    }
    
    # 1. Valid telemetry
    telemetry = [
        {"tool_name": "navigate", "arguments": {"url": "http://localhost"}},
        {"tool_name": "finish_task", "arguments": {"success": True}}
    ]
    report = evaluator.evaluate_trajectory(golden, telemetry)
    assert report.passed is True
    
    # 2. Forbidden tool telemetry
    telemetry_bad = [
        {"tool_name": "execute_sql", "arguments": {"query": "DROP TABLE"}},
        {"tool_name": "finish_task", "arguments": {"success": True}}
    ]
    report_bad = evaluator.evaluate_trajectory(golden, telemetry_bad)
    assert report_bad.passed is False
    assert "Used forbidden tool: execute_sql" in report_bad.violations

def test_failure_agent_needs_more_evidence():
    os.environ["MOCK_LLM_EVALS"] = "true"
    agent = FailureAgent()
    
    # Mocking execution to return Needs More Evidence
    agent.execute = lambda input_data, schema: schema(
        test_case_id="TC-1",
        failure_type="NEEDS_MORE_EVIDENCE",
        root_cause="Not enough info",
        evidence="None",
        confidence=0.1,
        recommended_action="Provide logs",
        requires_human_review=True
    )
    
    result = agent.classify_and_analyze("TC-1", "", "", None)
    assert result.failure_type == "NEEDS_MORE_EVIDENCE"

def test_self_healing_service_mock():
    os.environ["MOCK_LLM_EVALS"] = "true"
    service = SelfHealingService()
    
    proposal = service.generate_healing_proposal(
        failed_locator=".brittle-class",
        dom_snippet="<button id='submit'>Submit</button>",
        file_path="tests/login.py"
    )
    
    assert proposal.confidence >= 0.7
    assert "button:has-text('Submit')" in proposal.candidate_locator
    assert ".patch" not in proposal.patch_content # It's just content
    
    # Verify it doesn't write unless requested
    # We test the write logic
    tmp_dir = "/tmp"
    patch_path = service.write_patch(proposal, tmp_dir)
    assert os.path.exists(patch_path)
    os.remove(patch_path)

def test_golden_learning_agent_staging(tmp_path):
    os.environ["MOCK_LLM_EVALS"] = "true"
    agent = GoldenLearningAgent()
    
    # Mock the return
    agent.execute = lambda input, schema: schema(
        golden_id="CHAT-REG-001",
        category="multi-turn",
        conversation=[{"role": "user", "content": "mock"}],
        expected_behavior="Fix this bug",
        severity="high"
    )
    
    result = agent.generate_regression_golden({"bug": "ignored allergy"}, [])
    assert result.golden_id == "CHAT-REG-001"
    
    staging_file = os.path.join(tmp_path, "regression_goldens_staging.json")
    stage_regression_golden(result, staging_file)
    
    assert os.path.exists(staging_file)
    with open(staging_file, "r") as f:
        data = json.load(f)
    assert len(data["goldens"]) == 1
    assert data["goldens"][0]["golden_id"] == "CHAT-REG-001"
