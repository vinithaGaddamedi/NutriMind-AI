import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from agents.schemas.quality_gate_schemas import QualityGateInput, QualityGateDecision, QualityGateReport

class QualityGateEvaluator:
    """
    Evaluates aggregated QA metrics against configurable thresholds to determine 
    if a CI/CD build should PASS, FAIL, or WARN.
    """
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "../config/quality_gate_thresholds.json"
            ))
        
        with open(config_path, "r") as f:
            self.thresholds = json.load(f)

    def evaluate(self, metrics: QualityGateInput) -> QualityGateReport:
        violations = []
        warnings = []
        
        # 1. Critical Hard Stops
        if metrics.critical_functional_pass_rate < self.thresholds["critical_functional_pass_rate"]:
            violations.append(f"Critical functional pass rate ({metrics.critical_functional_pass_rate}%) is below required ({self.thresholds['critical_functional_pass_rate']}%)")
            
        if metrics.critical_constraint_pass_rate < self.thresholds["critical_constraint_pass_rate"]:
            violations.append(f"Critical constraint pass rate ({metrics.critical_constraint_pass_rate}%) is below required ({self.thresholds['critical_constraint_pass_rate']}%)")
            
        if metrics.security_critical_failures > self.thresholds["max_security_critical_failures"]:
            violations.append(f"Found {metrics.security_critical_failures} critical security failures (Max allowed: {self.thresholds['max_security_critical_failures']})")
            
        if metrics.p0_p1_defects > self.thresholds["max_p0_p1_defects"]:
            violations.append(f"Found {metrics.p0_p1_defects} P0/P1 defects (Max allowed: {self.thresholds['max_p0_p1_defects']})")
            
        # 2. AI Quality Thresholds
        if metrics.ai_safety_score < self.thresholds["ai_safety_min"]:
            violations.append(f"AI Safety score ({metrics.ai_safety_score}) is below minimum ({self.thresholds['ai_safety_min']})")
            
        if metrics.ai_relevance_score < self.thresholds["ai_relevance_min"]:
            warnings.append(f"AI Relevance score ({metrics.ai_relevance_score}) is below preferred ({self.thresholds['ai_relevance_min']})")
            
        if metrics.ai_faithfulness_score < self.thresholds["ai_faithfulness_min"]:
            violations.append(f"AI Faithfulness score ({metrics.ai_faithfulness_score}) is below minimum ({self.thresholds['ai_faithfulness_min']})")
            
        if metrics.ai_hallucination_rate > self.thresholds["ai_hallucination_max"]:
            violations.append(f"AI Hallucination rate ({metrics.ai_hallucination_rate}%) exceeds maximum ({self.thresholds['ai_hallucination_max']}%)")

        # Decision Logic
        if len(violations) > 0:
            decision = QualityGateDecision.FAIL
        elif len(warnings) > 0:
            decision = QualityGateDecision.WARN
        else:
            decision = QualityGateDecision.PASS

        return QualityGateReport(
            decision=decision,
            violations=violations,
            warnings=warnings,
            input_metrics=metrics
        )
