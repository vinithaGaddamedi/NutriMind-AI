import json
import os
import sys
from typing import Dict, Any, List

from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, HallucinationMetric

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.gemini_eval_model import GeminiEvalModel
from utils.deterministic_validator import DeterministicValidator
from utils.ai_test_oracle import AITestOracle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../agents')))
from schemas.evaluation_schemas import ChatbotGolden

class UnifiedEvaluator:
    def __init__(self, thresholds_path: str = None):
        if not thresholds_path:
            thresholds_path = os.path.join(os.path.dirname(__file__), '../config/eval_thresholds.json')
        
        with open(thresholds_path, 'r', encoding='utf-8') as f:
            self.thresholds = json.load(f)
            
        self.eval_model = GeminiEvalModel()
        self.deterministic_validator = DeterministicValidator()
        self.oracle = AITestOracle()
        self.mock_llm_evals = os.environ.get("MOCK_LLM_EVALS") == "true"

    def evaluate(self, golden: ChatbotGolden, actual_output: str, retrieval_context: List[str] = None) -> Dict[str, Any]:
        """
        Runs Deterministic Validation first. If passed, runs DeepEval.
        """
        report = {
            "golden_id": golden.golden_id,
            "category": golden.category.value,
            "deterministic_passed": False,
            "oracle_passed": False,
            "deepeval_passed": False,
            "overall_passed": False,
            "hallucination_detected": False,
            "hallucination_evidence": "",
            "hallucination_severity": "",
            "hallucination_confidence": 0.0,
            "deterministic_violations": [],
            "oracle_violations": [],
            "oracle_reason": "",
            "deepeval_metrics": {}
        }

        # 1. Deterministic Validation
        det_result = DeterministicValidator.validate_chatbot_response(
            response_text=actual_output,
            context=golden.context,
            forbidden_behaviors=golden.forbidden_behavior
        )
        
        report["deterministic_passed"] = det_result.passed
        report["deterministic_violations"] = [v.model_dump() for v in det_result.violations]

        if not det_result.passed:
            # Short-circuit logic if deterministic safety fails
            return report

        # Step 2: AI Test Oracle
        # Evaluates generative expectations logically before heavy NLP metrics
        oracle_decision = self.oracle.evaluate(
            actual_output=actual_output,
            expected_behavior=golden.expected_behavior,
            constraints=golden.constraints,
            context=golden.context.model_dump() if golden.context else {}
        )
        report["oracle_passed"] = oracle_decision.passed
        report["oracle_reason"] = oracle_decision.reason
        report["oracle_violations"] = oracle_decision.violations
        
        if not oracle_decision.passed:
            # If Oracle fails, we mark overall failed, but we can still run DeepEval for debugging metrics
            pass

        # Step 3: DeepEval Semantic Validation
        # Construct LLMTestCase
        # The input is the last message content from the user
        user_input = golden.conversation[-1].content if golden.conversation else ""
        
        test_case = LLMTestCase(
            input=user_input,
            actual_output=actual_output,
            expected_output=golden.expected_behavior,
            retrieval_context=retrieval_context or []
        )

        metrics = []
        
        # We selectively initialize metrics based on the thresholds available
        if "answer_relevancy" in self.thresholds:
            metrics.append(AnswerRelevancyMetric(
                threshold=self.thresholds["answer_relevancy"],
                model=self.eval_model,
                include_reason=True
            ))
            
        if "hallucination" in self.thresholds and retrieval_context:
            metrics.append(HallucinationMetric(
                threshold=self.thresholds["hallucination"],
                model=self.eval_model,
                include_reason=True
            ))

        deepeval_passed = True
        for metric in metrics:
            if self.mock_llm_evals:
                # Mock the metric result to avoid burning LLM credits in CI
                report["deepeval_metrics"][metric.__name__] = {
                    "score": 1.0,
                    "reason": "Mocked successful evaluation",
                    "passed": True
                }
                continue
                
            metric.measure(test_case)
            report["deepeval_metrics"][metric.__name__] = {
                "score": metric.score,
                "reason": metric.reason,
                "passed": metric.is_successful()
            }
            
            # Map Hallucination explicitly
            if metric.__name__ == "HallucinationMetric":
                # HallucinationMetric score is 0-1, where higher score means MORE hallucination? 
                # DeepEval HallucinationMetric: lower score is better (0 = no hallucination, 1 = full hallucination).
                # Actually, DeepEval metrics standardizes to: higher is better? Let's assume standard.
                # If metric failed, hallucination was detected.
                if not metric.is_successful():
                    report["hallucination_detected"] = True
                    report["hallucination_evidence"] = metric.reason
                    report["hallucination_severity"] = golden.severity
                    report["hallucination_confidence"] = metric.score

            if not metric.is_successful():
                deepeval_passed = False

        report["deepeval_passed"] = deepeval_passed
        report["overall_passed"] = deepeval_passed and report["deterministic_passed"] and report["oracle_passed"]
        
        return report
