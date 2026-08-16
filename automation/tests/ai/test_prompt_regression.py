import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from agents.infrastructure.schemas.prompt_schemas import PromptVersion, QualityMetrics, PromptStatus
from automation.utils.prompt_regression_runner import PromptRegressionRunner

def test_prompt_regression_runner_pass():
    runner = PromptRegressionRunner()
    
    baseline = PromptVersion(
        prompt_id="test_agent", version="1.0.0", description="Initial", owner="QE", prompt_text="Do X", status=PromptStatus.PROMOTED
    )
    candidate = PromptVersion(
        prompt_id="test_agent", version="1.1.0", description="Added Y", owner="QE", prompt_text="Do X and Y"
    )
    
    baseline_metrics = QualityMetrics(relevance=0.95, faithfulness=0.95, safety=1.0, constraint_compliance=0.98, hallucination=0.01, latency_ms=1000)
    candidate_metrics = QualityMetrics(relevance=0.96, faithfulness=0.96, safety=1.0, constraint_compliance=0.99, hallucination=0.0, latency_ms=1100)
    
    report = runner.evaluate_candidate(baseline, candidate, baseline_metrics, candidate_metrics)
    
    assert report.is_promoted is True
    assert len(report.rejection_reasons) == 0
    assert candidate.status == PromptStatus.PROMOTED

def test_prompt_regression_runner_reject_threshold():
    runner = PromptRegressionRunner()
    
    baseline = PromptVersion(prompt_id="test_agent", version="1.0.0", description="Initial", owner="QE", prompt_text="Do X", status=PromptStatus.PROMOTED)
    candidate = PromptVersion(prompt_id="test_agent", version="1.2.0", description="Fast but hallucinates", owner="QE", prompt_text="Make it up")
    
    baseline_metrics = QualityMetrics(relevance=0.95, faithfulness=0.95, safety=1.0, constraint_compliance=0.98, hallucination=0.01, latency_ms=1000)
    
    # Candidate violates minimum absolute threshold for hallucination
    candidate_metrics = QualityMetrics(relevance=0.95, faithfulness=0.95, safety=1.0, constraint_compliance=0.98, hallucination=0.10, latency_ms=800)
    
    report = runner.evaluate_candidate(baseline, candidate, baseline_metrics, candidate_metrics)
    
    assert report.is_promoted is False
    assert "above maximum" in report.rejection_reasons[0]
    assert candidate.status == PromptStatus.REJECTED

def test_prompt_regression_runner_reject_relative():
    runner = PromptRegressionRunner()
    
    baseline = PromptVersion(prompt_id="test_agent", version="1.0.0", description="Initial", owner="QE", prompt_text="Do X", status=PromptStatus.PROMOTED)
    candidate = PromptVersion(prompt_id="test_agent", version="1.3.0", description="Worse relevance", owner="QE", prompt_text="Do something")
    
    baseline_metrics = QualityMetrics(relevance=0.99, faithfulness=0.99, safety=1.0, constraint_compliance=1.0, hallucination=0.0, latency_ms=1000)
    
    # Candidate passes absolute min thresholds (0.85), but drops significantly relative to baseline (0.99 -> 0.90)
    candidate_metrics = QualityMetrics(relevance=0.90, faithfulness=0.99, safety=1.0, constraint_compliance=1.0, hallucination=0.0, latency_ms=1000)
    
    report = runner.evaluate_candidate(baseline, candidate, baseline_metrics, candidate_metrics)
    
    assert report.is_promoted is False
    assert "regressed significantly" in report.rejection_reasons[0]
