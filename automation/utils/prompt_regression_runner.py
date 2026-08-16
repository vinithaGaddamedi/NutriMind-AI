import json
from typing import Dict, Any
from agents.schemas.prompt_schemas import PromptVersion, QualityMetrics, PromptRegressionReport, PromptStatus

class PromptRegressionRunner:
    """
    Evaluates a candidate prompt version against a baseline prompt version
    using their execution metrics on a Golden Dataset.
    Automatically rejects prompts that degrade critical quality metrics.
    """
    def __init__(self):
        # Configurable thresholds for rejecting a prompt
        self.thresholds = {
            "relevance_min": 0.85,
            "faithfulness_min": 0.90,
            "safety_min": 0.95,
            "constraint_compliance_min": 0.95,
            "hallucination_max": 0.05,
            "latency_degradation_max_ms": 1500 # max allowable slowdown
        }

    def evaluate_candidate(
        self, 
        baseline: PromptVersion, 
        candidate: PromptVersion,
        baseline_metrics: QualityMetrics,
        candidate_metrics: QualityMetrics
    ) -> PromptRegressionReport:
        
        rejection_reasons = []

        # 1. Absolute Threshold Checks
        if candidate_metrics.relevance < self.thresholds["relevance_min"]:
            rejection_reasons.append(f"Relevance ({candidate_metrics.relevance}) below minimum ({self.thresholds['relevance_min']})")
        if candidate_metrics.faithfulness < self.thresholds["faithfulness_min"]:
            rejection_reasons.append(f"Faithfulness ({candidate_metrics.faithfulness}) below minimum ({self.thresholds['faithfulness_min']})")
        if candidate_metrics.safety < self.thresholds["safety_min"]:
            rejection_reasons.append(f"Safety ({candidate_metrics.safety}) below minimum ({self.thresholds['safety_min']})")
        if candidate_metrics.constraint_compliance < self.thresholds["constraint_compliance_min"]:
            rejection_reasons.append(f"Constraint Compliance ({candidate_metrics.constraint_compliance}) below minimum ({self.thresholds['constraint_compliance_min']})")
        if candidate_metrics.hallucination > self.thresholds["hallucination_max"]:
            rejection_reasons.append(f"Hallucination ({candidate_metrics.hallucination}) above maximum ({self.thresholds['hallucination_max']})")
            
        # 2. Relative Regression Checks (Candidate should not be significantly worse than baseline)
        if candidate_metrics.relevance < baseline_metrics.relevance - 0.05:
            rejection_reasons.append("Relevance regressed significantly compared to baseline.")
        if candidate_metrics.faithfulness < baseline_metrics.faithfulness - 0.05:
            rejection_reasons.append("Faithfulness regressed significantly compared to baseline.")
            
        # Latency check
        latency_diff = candidate_metrics.latency_ms - baseline_metrics.latency_ms
        if latency_diff > self.thresholds["latency_degradation_max_ms"]:
            rejection_reasons.append(f"Latency degraded by {latency_diff}ms (Max allowed: {self.thresholds['latency_degradation_max_ms']}ms).")

        is_promoted = len(rejection_reasons) == 0
        
        # Update the status based on evaluation
        if is_promoted:
            candidate.status = PromptStatus.PROMOTED
        else:
            candidate.status = PromptStatus.REJECTED

        return PromptRegressionReport(
            baseline_id=f"{baseline.prompt_id}_v{baseline.version}",
            candidate_id=f"{candidate.prompt_id}_v{candidate.version}",
            is_promoted=is_promoted,
            rejection_reasons=rejection_reasons,
            baseline_metrics=baseline_metrics,
            candidate_metrics=candidate_metrics
        )
