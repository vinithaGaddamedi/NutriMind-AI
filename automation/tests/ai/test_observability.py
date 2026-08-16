import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from agents.schemas.observability_schemas import AIObservabilityRecord
from automation.utils.observability_tracker import AIObservabilityTracker

def test_observability_aggregation(tmp_path):
    tracker = AIObservabilityTracker(output_dir=str(tmp_path))
    
    # Record 1: Success
    tracker.track(AIObservabilityRecord(
        agent="RequirementAgent",
        model="gemini-1.5-pro",
        prompt_version="1.0",
        correlation_id="test_run_1",
        latency_ms=1000,
        evaluation_score=0.9,
        status="SUCCESS"
    ))
    
    # Record 2: Success
    tracker.track(AIObservabilityRecord(
        agent="RequirementAgent",
        model="gemini-1.5-pro",
        prompt_version="1.0",
        correlation_id="test_run_2",
        latency_ms=2000,
        evaluation_score=1.0,
        status="SUCCESS"
    ))
    
    # Record 3: Failure
    tracker.track(AIObservabilityRecord(
        agent="RiskAgent",
        model="gemini-1.5-flash",
        prompt_version="2.0",
        correlation_id="test_run_3",
        latency_ms=500,
        status="FAILURE",
        error_type="TimeoutError"
    ))
    
    summary = tracker.aggregate_summary()
    
    # Overall asserts
    assert summary.overall_success_rate == (2/3) * 100.0
    assert summary.overall_failure_rate == (1/3) * 100.0
    assert summary.average_latency_ms == 3500 / 3
    
    # Model usage
    assert summary.model_usage["gemini-1.5-pro"] == 2
    assert summary.model_usage["gemini-1.5-flash"] == 1
    
    # Agent stats
    assert summary.agent_performance["RequirementAgent"].success_rate == 100.0
    assert summary.agent_performance["RequirementAgent"].average_evaluation_score == 0.95
    assert summary.agent_performance["RiskAgent"].success_rate == 0.0

def test_observability_privacy_scrubbing(tmp_path):
    tracker = AIObservabilityTracker(output_dir=str(tmp_path))
    
    # Try to log an agent with a malicious correlation ID containing "api_key"
    malicious_record = AIObservabilityRecord(
        agent="HackedAgent",
        model="gemini-1.5-pro",
        prompt_version="1.0",
        correlation_id="test_run_my_api_key_12345",
        latency_ms=1000,
        status="SUCCESS"
    )
    
    tracker.track(malicious_record)
    
    # Verify it was caught and scrubbed
    assert tracker._records[0].status == "SCRUBBED_FOR_PRIVACY"
    assert tracker._records[0].agent == "SCRUBBED"
    assert tracker._records[0].error_type == "PrivacyViolation"
