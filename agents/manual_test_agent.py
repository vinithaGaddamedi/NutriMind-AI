import os
import csv
import logging
from typing import List, Dict, Any

logger = logging.getLogger("ManualTestAgent")

class ManualTestAgent:
    """
    Transforms Test Scenarios into detailed Manual Test Cases and exports CSV / Excel reports.
    """

    def generate_manual_test_cases(self, scenarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        test_cases = []
        for i, sc in enumerate(scenarios, 1):
            tc = {
                "test_case_id": f"TC-{sc['requirement_id']}-{i:03d}",
                "scenario_id": sc["scenario_id"],
                "requirement_id": sc["requirement_id"],
                "title": f"Verify {sc['description']}",
                "type": sc["type"],
                "priority": sc["priority"],
                "preconditions": "User logged into NutriMind AI platform",
                "steps": "1. Navigate to section.\n2. Enter inputs.\n3. Click Submit.",
                "expected_result": "System processes request matching acceptance criteria.",
                "automation_candidate": "Yes" if sc["automation_candidate"] else "No"
            }
            test_cases.append(tc)
        return test_cases

    def export_to_csv(self, test_cases: List[Dict[str, Any]], output_path: str = "reports/manual-test-cases.csv"):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if not test_cases:
            return

        keys = test_cases[0].keys()
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(test_cases)
        logger.info("Successfully exported %d manual test cases to '%s'", len(test_cases), output_path)
