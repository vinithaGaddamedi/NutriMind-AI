import sys
import os
import pytest
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from agents.test_optimization_agent import TestOptimizationAgent
from agents.schemas.optimization_schemas import OptimizationInput, TestMetadata, OptimizationReport, TestSuiteSelection, SelectedTest
from automation.utils.optimization_reporter import OptimizationReporter

def test_optimization_agent_mock():
    os.environ["MOCK_LLM_EVALS"] = "true"
    agent = TestOptimizationAgent()
    
    agent.execute = lambda input, schema: schema(
        pr_suite=TestSuiteSelection(
            tests=[
                SelectedTest(test_id="TS-01", reasoning="High risk requirement tied to auth.py changes.")
            ]
        ),
        nightly_suite=TestSuiteSelection(
            tests=[
                SelectedTest(test_id="TS-01", reasoning="Inherited from PR suite."),
                SelectedTest(test_id="TS-FLAKY-02", reasoning="Flaky test isolated to nightly runs.")
            ]
        ),
        release_suite=TestSuiteSelection(
            tests=[
                SelectedTest(test_id="TS-01", reasoning="Core requirement."),
                SelectedTest(test_id="TS-FLAKY-02", reasoning="Required for release."),
                SelectedTest(test_id="TS-SLOW-03", reasoning="Long running test required for release.")
            ]
        )
    )
    
    payload = OptimizationInput(
        changed_code=["auth.py"],
        available_tests=[
            TestMetadata(test_id="TS-01", requirement_risk="High", duration_ms=1000, historical_failure_rate=0.0, is_flaky=False, dependencies=["auth.py"]),
            TestMetadata(test_id="TS-FLAKY-02", requirement_risk="Medium", duration_ms=2000, historical_failure_rate=0.5, is_flaky=True, dependencies=["ui.py"]),
            TestMetadata(test_id="TS-SLOW-03", requirement_risk="Low", duration_ms=150000, historical_failure_rate=0.0, is_flaky=False, dependencies=["db.py"])
        ]
    )
    
    report = agent.optimize_suites(payload)
    
    # Verify the PR suite only contains the high-risk, non-flaky test
    assert len(report.pr_suite.tests) == 1
    assert report.pr_suite.tests[0].test_id == "TS-01"
    
    # Verify the nightly suite contains the flaky test
    nightly_ids = [t.test_id for t in report.nightly_suite.tests]
    assert "TS-FLAKY-02" in nightly_ids
    
    # Verify release contains everything
    assert len(report.release_suite.tests) == 3

def test_optimization_reporter(tmp_path):
    reporter = OptimizationReporter(output_dir=str(tmp_path))
    
    report = OptimizationReport(
        pr_suite=TestSuiteSelection(tests=[SelectedTest(test_id="T1", reasoning="Fast")]),
        nightly_suite=TestSuiteSelection(tests=[SelectedTest(test_id="T1", reasoning="Inherited"), SelectedTest(test_id="T2", reasoning="Flaky")]),
        release_suite=TestSuiteSelection(tests=[SelectedTest(test_id="T1", reasoning="Inherited"), SelectedTest(test_id="T2", reasoning="Flaky"), SelectedTest(test_id="T3", reasoning="Slow")])
    )
    
    reporter.generate_report(report)
    json_path = os.path.join(tmp_path, "optimized_suites.json")
    
    assert os.path.exists(json_path)
    with open(json_path, "r") as f:
        data = json.load(f)
        assert data["pr_suite"]["tests"][0]["test_id"] == "T1"
