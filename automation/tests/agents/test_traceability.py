import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from agents.traceability_agent import TraceabilityAgent
from agents.schemas.traceability_schemas import TraceabilityReport, CoverageMetrics, TraceabilityGaps, TraceNode
from automation.utils.rtm_generator import RTMGenerator

def test_traceability_agent_mock():
    os.environ["MOCK_LLM_EVALS"] = "true"
    agent = TraceabilityAgent()
    
    # Mocking the LLM execution
    agent.execute = lambda input, schema: schema(
        nodes=[
            TraceNode(id="REQ-01", type="Requirement", severity="High", linked_ids=["TS-01"]),
            TraceNode(id="TS-01", type="TestScenario", severity="High", linked_ids=[]) # Missing Automation
        ],
        metrics=CoverageMetrics(
            critical_coverage_percent=100.0,
            high_coverage_percent=0.0,
            medium_coverage_percent=0.0,
            low_coverage_percent=0.0,
            total_coverage_percent=0.0
        ),
        gaps=TraceabilityGaps(
            high_risk_without_automation=["REQ-01"]
        )
    )
    
    raw_data = [
        {"id": "REQ-01", "type": "Requirement", "severity": "High"},
        {"id": "TS-01", "type": "TestScenario", "links": ["REQ-01"]}
    ]
    
    report = agent.generate_rtm(raw_data)
    
    assert "REQ-01" in report.gaps.high_risk_without_automation
    assert report.metrics.high_coverage_percent == 0.0

def test_rtm_generator(tmp_path):
    generator = RTMGenerator(output_dir=str(tmp_path))
    
    report = TraceabilityReport(
        nodes=[TraceNode(id="REQ-02", type="Requirement", severity="Critical", linked_ids=["AUTO-01"])],
        metrics=CoverageMetrics(
            critical_coverage_percent=100.0,
            high_coverage_percent=100.0,
            medium_coverage_percent=100.0,
            low_coverage_percent=100.0,
            total_coverage_percent=100.0
        ),
        gaps=TraceabilityGaps()
    )
    
    generator.generate_reports(report)
    
    assert os.path.exists(os.path.join(tmp_path, "RTM.json"))
    assert os.path.exists(os.path.join(tmp_path, "RTM.csv"))
    
    with open(os.path.join(tmp_path, "RTM.json"), "r") as f:
        import json
        data = json.load(f)
        assert data["metrics"]["critical_coverage_percent"] == 100.0
