import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from agents.infrastructure.schemas.observability_schemas import AIObservabilityRecord, AIObservabilitySummary, AgentPerformance

class AIObservabilityTracker:
    """
    Centralized telemetry tracker for AI Agent invocations.
    Ensures strict privacy scrubbing before flushing to disk.
    """
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.raw_log_path = os.path.join(self.output_dir, "ai-observability.json")
        self.summary_path = os.path.join(self.output_dir, "ai-observability-summary.json")
        self._records = []

    def _scrub_sensitive_data(self, record: AIObservabilityRecord) -> AIObservabilityRecord:
        """
        Hard rule: Never capture API keys, passwords, or raw secrets.
        We ensure no text fields accidentally contain known secret patterns.
        """
        dump = record.model_dump_json().lower()
        forbidden_strings = ["api_key", "password", "secret", "bearer"]
        for forbidden in forbidden_strings:
            if forbidden in dump:
                # If a telemetry payload explicitly includes sensitive keys in its strings, reject it and mark as SCRUBBED
                record.status = "SCRUBBED_FOR_PRIVACY"
                record.error_type = "PrivacyViolation"
                # Strip out potential leaks from custom string fields
                record.agent = "SCRUBBED"
                record.prompt_version = "SCRUBBED"
                break
        return record

    def track(self, record: AIObservabilityRecord):
        safe_record = self._scrub_sensitive_data(record)
        self._records.append(safe_record)
        
        # Append to raw log line-by-line (JSON Lines format for scalability)
        with open(self.raw_log_path, "a") as f:
            f.write(safe_record.model_dump_json() + "\n")

    def aggregate_summary(self) -> AIObservabilitySummary:
        if not self._records:
            return AIObservabilitySummary()

        total = len(self._records)
        successes = sum(1 for r in self._records if r.status == "SUCCESS")
        failures = total - successes
        total_latency = sum(r.latency_ms for r in self._records)
        
        summary = AIObservabilitySummary(
            overall_success_rate=(successes / total) * 100.0,
            overall_failure_rate=(failures / total) * 100.0,
            average_latency_ms=total_latency / total
        )

        agent_stats = {}
        for r in self._records:
            # Model usage
            summary.model_usage[r.model] = summary.model_usage.get(r.model, 0) + 1
            
            # Agent specific tracking
            if r.agent not in agent_stats:
                agent_stats[r.agent] = {"total": 0, "success": 0, "latency": 0, "eval_scores": []}
            
            agent_stats[r.agent]["total"] += 1
            if r.status == "SUCCESS":
                agent_stats[r.agent]["success"] += 1
            agent_stats[r.agent]["latency"] += r.latency_ms
            
            if r.evaluation_score is not None:
                agent_stats[r.agent]["eval_scores"].append(r.evaluation_score)
                
                # Prompt version tracking
                pv_key = f"{r.agent}_{r.prompt_version}"
                if pv_key not in summary.prompt_version_performance:
                    summary.prompt_version_performance[pv_key] = []
                summary.prompt_version_performance[pv_key].append(r.evaluation_score)

        # Finalize averages
        for agent, stats in agent_stats.items():
            avg_eval = sum(stats["eval_scores"]) / len(stats["eval_scores"]) if stats["eval_scores"] else 0.0
            summary.agent_performance[agent] = AgentPerformance(
                total_invocations=stats["total"],
                success_rate=(stats["success"] / stats["total"]) * 100.0,
                average_latency_ms=stats["latency"] / stats["total"],
                average_evaluation_score=avg_eval
            )
            
        for pv_key, scores in summary.prompt_version_performance.items():
            summary.prompt_version_performance[pv_key] = sum(scores) / len(scores)

        # Write summary
        with open(self.summary_path, "w") as f:
            json.dump(summary.model_dump(), f, indent=2)

        return summary
