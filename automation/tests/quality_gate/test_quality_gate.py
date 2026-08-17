import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from agents.infrastructure.schemas.quality_gate_schemas import QualityGateInput, QualityGateDecision
from automation.utils.quality_gate import QualityGateEvaluator

def test_quality_gate_pass():
    evaluator = QualityGateEvaluator()
    metrics = QualityGateInput(
        critical_functional_pass_rate=100.0,
        critical_constraint_pass_rate=100.0,
        ai_safety_score=100.0,
        ai_relevance_score=95.0,
        ai_faithfulness_score=100.0,
        ai_hallucination_rate=0.0,
        security_critical_failures=0,
        p0_p1_defects=0
    )
    
    report = evaluator.evaluate(metrics)
    assert report.decision == QualityGateDecision.PASS
    assert len(report.violations) == 0

def test_quality_gate_fail_hallucination():
    evaluator = QualityGateEvaluator()
    metrics = QualityGateInput(
        critical_functional_pass_rate=100.0,
        critical_constraint_pass_rate=100.0,
        ai_safety_score=100.0,
        ai_relevance_score=100.0,
        ai_faithfulness_score=100.0,
        ai_hallucination_rate=10.0, # Violates max (5.0)
        security_critical_failures=0,
        p0_p1_defects=0
    )
    
    report = evaluator.evaluate(metrics)
    assert report.decision == QualityGateDecision.FAIL
    assert "AI Hallucination rate (10.0%) exceeds maximum" in report.violations[0]

def test_quality_gate_fail_security():
    evaluator = QualityGateEvaluator()
    metrics = QualityGateInput(
        critical_functional_pass_rate=100.0,
        critical_constraint_pass_rate=100.0,
        ai_safety_score=100.0,
        ai_relevance_score=100.0,
        ai_faithfulness_score=100.0,
        ai_hallucination_rate=0.0,
        security_critical_failures=1, # Violates max (0)
        p0_p1_defects=0
    )
    
    report = evaluator.evaluate(metrics)
    assert report.decision == QualityGateDecision.FAIL
    assert "Found 1 critical security failures" in report.violations[0]

def test_quality_gate_warn_relevance():
    evaluator = QualityGateEvaluator()
    metrics = QualityGateInput(
        critical_functional_pass_rate=100.0,
        critical_constraint_pass_rate=100.0,
        ai_safety_score=100.0,
        ai_relevance_score=80.0, # Soft breach of 85.0
        ai_faithfulness_score=100.0,
        ai_hallucination_rate=0.0,
        security_critical_failures=0,
        p0_p1_defects=0
    )
    
    report = evaluator.evaluate(metrics)
    assert report.decision == QualityGateDecision.WARN
    assert len(report.violations) == 0
    assert len(report.warnings) == 1
    assert "AI Relevance score" in report.warnings[0]
