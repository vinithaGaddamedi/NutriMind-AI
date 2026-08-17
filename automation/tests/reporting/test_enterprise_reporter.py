import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from agents.infrastructure.schemas.enterprise_report_schemas import ConsolidatedReport, ExecutiveSummary
from automation.utils.enterprise_reporter import EnterpriseReporter

def test_enterprise_reporter_generation(tmp_path):
    reporter = EnterpriseReporter(output_dir=str(tmp_path))
    
    summary = ExecutiveSummary(
        overall_quality="FAIL",
        functional_pass_rate=99.5,
        api_pass_rate=100.0,
        automation_pass_rate=95.0,
        ai_quality_score=92.5,
        security_pass_rate=100.0,
        coverage_percentage=88.0,
        critical_issues_count=1 # Triggered the FAIL
    )
    
    report = ConsolidatedReport(
        executive_summary=summary,
        quality_gate_decision={"decision": "FAIL", "violations": ["1 Critical Issue"]}
    )
    
    reporter.generate_all(report)
    
    json_path = os.path.join(tmp_path, "enterprise_report.json")
    md_path = os.path.join(tmp_path, "enterprise_report.md")
    csv_path = os.path.join(tmp_path, "enterprise_report.csv")
    html_path = os.path.join(tmp_path, "enterprise_report.html")
    
    assert os.path.exists(json_path)
    assert os.path.exists(md_path)
    assert os.path.exists(csv_path)
    assert os.path.exists(html_path)
    
    # Read back to ensure format is correct
    with open(md_path, "r") as f:
        md_text = f.read()
        assert "FAIL" in md_text
        assert "92.5%" in md_text
        
    with open(csv_path, "r") as f:
        csv_text = f.read()
        assert "Overall Quality,FAIL" in csv_text
        
    with open(html_path, "r") as f:
        html_text = f.read()
        assert "color: white; background-color: red;" in html_text # Because it FAILed
