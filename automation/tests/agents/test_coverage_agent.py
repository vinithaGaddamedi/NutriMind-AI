import sys
import os
import pytest
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from agents.intelligence.coverage_agent import CoverageAgent
from agents.schemas.coverage_schemas import CoverageReport, CoverageMetricsBreakdown, SeverityCoverage, CoverageGapRecommendation
from automation.utils.coverage_reporter import CoverageReporter

def test_coverage_agent_mock():
    os.environ["MOCK_LLM_EVALS"] = "true"
    agent = CoverageAgent()
    
    agent.execute = lambda input, schema: schema(
        metrics=CoverageMetricsBreakdown(
            critical=SeverityCoverage(
                requirement_coverage=100.0,
                risk_coverage=100.0,
                automation_coverage=100.0,
                ai_behavior_coverage=100.0,
                golden_coverage=100.0
            ),
            high=SeverityCoverage(
                requirement_coverage=0.0, # Intentional 0% due to no execution
                risk_coverage=0.0,
                automation_coverage=100.0, # Automation exists but not executed
                ai_behavior_coverage=0.0,
                golden_coverage=0.0
            ),
            medium=SeverityCoverage(
                requirement_coverage=0.0, risk_coverage=0.0, automation_coverage=0.0, ai_behavior_coverage=0.0, golden_coverage=0.0
            ),
            low=SeverityCoverage(
                requirement_coverage=0.0, risk_coverage=0.0, automation_coverage=0.0, ai_behavior_coverage=0.0, golden_coverage=0.0
            ),
            overall=SeverityCoverage(
                requirement_coverage=50.0, risk_coverage=50.0, automation_coverage=100.0, ai_behavior_coverage=50.0, golden_coverage=50.0
            )
        ),
        recommendations=[
            CoverageGapRecommendation(
                gap_type="UNEXECUTED_TEST",
                target_id="TS-02",
                recommendation="Test TS-02 exists but lacks a passing execution record. Run the suite.",
                priority="High"
            )
        ]
    )
    
    # Mock data: A requirement with a test that never executed
    raw_data = [
        {"id": "REQ-01", "type": "Requirement", "severity": "Critical", "execution": "passed"},
        {"id": "REQ-02", "type": "Requirement", "severity": "High", "execution": "none"}
    ]
    
    report = agent.analyze_coverage(raw_data)
    
    # Verify execution-based coverage rule
    assert report.metrics.high.requirement_coverage == 0.0
    assert report.recommendations[0].gap_type == "UNEXECUTED_TEST"

def test_coverage_reporter(tmp_path):
    reporter = CoverageReporter(output_dir=str(tmp_path))
    
    report = CoverageReport(
        metrics=CoverageMetricsBreakdown(
            critical=SeverityCoverage(requirement_coverage=100.0, risk_coverage=100.0, automation_coverage=100.0, ai_behavior_coverage=100.0, golden_coverage=100.0),
            high=SeverityCoverage(requirement_coverage=0.0, risk_coverage=0.0, automation_coverage=0.0, ai_behavior_coverage=0.0, golden_coverage=0.0),
            medium=SeverityCoverage(requirement_coverage=0.0, risk_coverage=0.0, automation_coverage=0.0, ai_behavior_coverage=0.0, golden_coverage=0.0),
            low=SeverityCoverage(requirement_coverage=0.0, risk_coverage=0.0, automation_coverage=0.0, ai_behavior_coverage=0.0, golden_coverage=0.0),
            overall=SeverityCoverage(requirement_coverage=25.0, risk_coverage=25.0, automation_coverage=25.0, ai_behavior_coverage=25.0, golden_coverage=25.0)
        ),
        recommendations=[]
    )
    
    reporter.generate_report(report)
    json_path = os.path.join(tmp_path, "coverage_report.json")
    
    assert os.path.exists(json_path)
    with open(json_path, "r") as f:
        data = json.load(f)
        assert data["metrics"]["critical"]["ai_behavior_coverage"] == 100.0
