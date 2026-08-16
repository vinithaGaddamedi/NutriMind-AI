import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from agents.schemas.coverage_schemas import CoverageReport

class CoverageReporter:
    """
    Utility to serialize the CoverageReport to disk.
    """
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_report(self, report: CoverageReport):
        json_path = os.path.join(self.output_dir, "coverage_report.json")
        with open(json_path, "w") as f:
            json.dump(report.model_dump(), f, indent=2)
        print(f"Coverage report generated at {json_path}")
