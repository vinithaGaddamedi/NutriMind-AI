import json
import csv
import os
from typing import Dict, Any
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from agents.infrastructure.schemas.traceability_schemas import TraceabilityReport

class RTMGenerator:
    """
    Generates structured RTM reports from the TraceabilityAgent's output.
    Supports JSON and CSV (as a lightweight alternative to XLSX to avoid heavy dependencies).
    """
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_reports(self, report: TraceabilityReport):
        self._generate_json(report)
        self._generate_csv(report)
        print(f"RTM generated successfully at {self.output_dir}/RTM.json and RTM.csv")

    def _generate_json(self, report: TraceabilityReport):
        json_path = os.path.join(self.output_dir, "RTM.json")
        with open(json_path, "w") as f:
            json.dump(report.model_dump(), f, indent=2)

    def _generate_csv(self, report: TraceabilityReport):
        csv_path = os.path.join(self.output_dir, "RTM.csv")
        
        with open(csv_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            # Write Summary Metrics
            writer.writerow(["=== COVERAGE METRICS ==="])
            writer.writerow(["Critical", f"{report.metrics.critical_coverage_percent}%"])
            writer.writerow(["High", f"{report.metrics.high_coverage_percent}%"])
            writer.writerow(["Medium", f"{report.metrics.medium_coverage_percent}%"])
            writer.writerow(["Low", f"{report.metrics.low_coverage_percent}%"])
            writer.writerow(["Total", f"{report.metrics.total_coverage_percent}%"])
            writer.writerow([])
            
            # Write Gaps
            writer.writerow(["=== DETECTED GAPS ==="])
            writer.writerow(["Category", "Node IDs"])
            writer.writerow(["Requirements without tests", ", ".join(report.gaps.requirements_without_tests)])
            writer.writerow(["High risk without automation", ", ".join(report.gaps.high_risk_without_automation)])
            writer.writerow(["Tests without requirements", ", ".join(report.gaps.tests_without_requirements)])
            writer.writerow(["Goldens without requirements", ", ".join(report.gaps.goldens_without_requirements)])
            writer.writerow(["Automation without test cases", ", ".join(report.gaps.automation_without_test_cases)])
            writer.writerow(["Defects without test coverage", ", ".join(report.gaps.defects_without_test_coverage)])
            writer.writerow([])
            
            # Write Nodes (The actual matrix view)
            writer.writerow(["=== FULL TRACEABILITY MATRIX ==="])
            writer.writerow(["Node ID", "Type", "Severity", "Linked IDs", "Metadata"])
            for node in report.nodes:
                writer.writerow([
                    node.id, 
                    node.type, 
                    node.severity, 
                    ", ".join(node.linked_ids), 
                    json.dumps(node.metadata)
                ])
