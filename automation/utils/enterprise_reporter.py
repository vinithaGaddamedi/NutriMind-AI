import json
import os
import csv
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from agents.infrastructure.schemas.enterprise_report_schemas import ConsolidatedReport, ExecutiveSummary

class EnterpriseReporter:
    """
    Generates the final Consolidated Enterprise QA Report across multiple formats.
    """
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_all(self, report: ConsolidatedReport):
        self._generate_json(report)
        self._generate_markdown(report)
        self._generate_csv(report)
        self._generate_html(report)

    def _generate_json(self, report: ConsolidatedReport):
        json_path = os.path.join(self.output_dir, "enterprise_report.json")
        with open(json_path, "w") as f:
            json.dump(report.model_dump(), f, indent=2)

    def _generate_csv(self, report: ConsolidatedReport):
        csv_path = os.path.join(self.output_dir, "enterprise_report.csv")
        summary = report.executive_summary
        
        # Following rule: Avoid Excel/openpyxl dependencies, use pure CSV
        with open(csv_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Overall Quality", summary.overall_quality])
            writer.writerow(["Functional Pass Rate (%)", f"{summary.functional_pass_rate:.1f}"])
            writer.writerow(["API Pass Rate (%)", f"{summary.api_pass_rate:.1f}"])
            writer.writerow(["Automation Pass Rate (%)", f"{summary.automation_pass_rate:.1f}"])
            writer.writerow(["AI Quality Score (%)", f"{summary.ai_quality_score:.1f}"])
            writer.writerow(["Security Pass Rate (%)", f"{summary.security_pass_rate:.1f}"])
            writer.writerow(["Coverage (%)", f"{summary.coverage_percentage:.1f}"])
            writer.writerow(["Critical Issues", summary.critical_issues_count])

    def _generate_markdown(self, report: ConsolidatedReport):
        md_path = os.path.join(self.output_dir, "enterprise_report.md")
        summary = report.executive_summary
        
        md_content = f"""# Enterprise QA Executive Summary

**Overall Quality**: `{summary.overall_quality}`

| Metric | Score |
|--------|-------|
| Functional | {summary.functional_pass_rate:.1f}% |
| API | {summary.api_pass_rate:.1f}% |
| Automation | {summary.automation_pass_rate:.1f}% |
| AI Quality | {summary.ai_quality_score:.1f}% |
| Security | {summary.security_pass_rate:.1f}% |
| Coverage | {summary.coverage_percentage:.1f}% |
| **Critical Issues** | **{summary.critical_issues_count}** |

*Note: For deeper subsystem metrics (Traceability, Quality Gates, Observability, Self-Healing), see `enterprise_report.json`.*
"""
        with open(md_path, "w") as f:
            f.write(md_content)

    def _generate_html(self, report: ConsolidatedReport):
        html_path = os.path.join(self.output_dir, "enterprise_report.html")
        summary = report.executive_summary
        
        color = "green" if summary.overall_quality == "PASS" else "red"
        if summary.overall_quality == "WARN":
            color = "orange"
            
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Enterprise QA Report</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; padding: 40px; color: #333; }}
        h1 {{ border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        .badge {{ display: inline-block; padding: 10px 20px; font-weight: bold; color: white; background-color: {color}; border-radius: 5px; }}
        table {{ border-collapse: collapse; width: 400px; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f8f9fa; }}
    </style>
</head>
<body>
    <h1>Enterprise QA Executive Summary</h1>
    <p>Overall Quality: <span class="badge">{summary.overall_quality}</span></p>
    
    <table>
        <tr><th>Metric</th><th>Score</th></tr>
        <tr><td>Functional</td><td>{summary.functional_pass_rate:.1f}%</td></tr>
        <tr><td>API</td><td>{summary.api_pass_rate:.1f}%</td></tr>
        <tr><td>Automation</td><td>{summary.automation_pass_rate:.1f}%</td></tr>
        <tr><td>AI Quality</td><td>{summary.ai_quality_score:.1f}%</td></tr>
        <tr><td>Security</td><td>{summary.security_pass_rate:.1f}%</td></tr>
        <tr><td>Coverage</td><td>{summary.coverage_percentage:.1f}%</td></tr>
        <tr><td><b>Critical Issues</b></td><td><b>{summary.critical_issues_count}</b></td></tr>
    </table>
</body>
</html>
"""
        with open(html_path, "w") as f:
            f.write(html_content)
