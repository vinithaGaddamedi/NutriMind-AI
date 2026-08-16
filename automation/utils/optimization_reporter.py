import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from agents.infrastructure.schemas.optimization_schemas import OptimizationReport

class OptimizationReporter:
    """
    Utility to serialize the OptimizationReport to disk.
    This output can be consumed by CI/CD pipelines (GitHub Actions, Jenkins) 
    to dynamically invoke pytest with the selected tests.
    """
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_report(self, report: OptimizationReport):
        json_path = os.path.join(self.output_dir, "optimized_suites.json")
        with open(json_path, "w") as f:
            json.dump(report.model_dump(), f, indent=2)
        print(f"Optimized suites generated at {json_path}")
