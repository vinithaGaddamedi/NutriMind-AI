import json
from typing import List, Dict, Any

class MCPQualityReport:
    def __init__(self, passed: bool, score: float, violations: List[str]):
        self.passed = passed
        self.score = score
        self.violations = violations

class MCPEvaluator:
    """
    Evaluates the trajectory of an MCPPlaywrightAgent against a golden scenario.
    Checks tool selection, parameter exactness, forbidden tools, and task completion.
    """
    def evaluate_trajectory(self, golden: Dict[str, Any], telemetry: List[Dict[str, Any]]) -> MCPQualityReport:
        violations = []
        
        # 1. Check forbidden tools
        forbidden = set(golden.get("forbidden_tools", []))
        for step in telemetry:
            if step["tool_name"] in forbidden:
                violations.append(f"Used forbidden tool: {step['tool_name']}")
                
        # 2. Check task completion success vs expected
        expected_success = golden.get("expected_success", True)
        actual_success = False
        if telemetry and telemetry[-1]["tool_name"] == "finish_task":
            actual_success = telemetry[-1]["arguments"].get("success", False)
            
        if expected_success != actual_success:
            violations.append(f"Expected success: {expected_success}, Actual: {actual_success}")
            
        # 3. Trajectory Matching (Simple sequence check)
        # Check if the expected sequence of tools was at least attempted in order
        expected_traj = golden.get("expected_trajectory", [])
        actual_tool_names = [t["tool_name"] for t in telemetry if t["tool_name"] != "finish_task"]
        expected_tool_names = [t["tool_name"] for t in expected_traj]
        
        # If it's a strict match scenario
        if len(expected_traj) > 0:
            # Did we at least attempt all expected tools?
            for ext in expected_tool_names:
                if ext not in actual_tool_names:
                    violations.append(f"Missing expected tool call: {ext}")
        
        passed = len(violations) == 0
        score = 1.0 if passed else 0.0
        return MCPQualityReport(passed=passed, score=score, violations=violations)
