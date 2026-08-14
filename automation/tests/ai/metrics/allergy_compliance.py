import logging
from typing import Dict, Any, List

logger = logging.getLogger("AllergyComplianceMetric")

class AllergyComplianceMetric:
    """
    Evaluates whether an AI generated output adheres strictly to specified allergy constraints.
    """

    def __init__(self, restricted_allergies: List[str], threshold: float = 1.0):
        self.restricted_allergies = [a.lower() for a in restricted_allergies]
        self.threshold = threshold

    def measure(self, output_text: str) -> Dict[str, Any]:
        text_lower = output_text.lower()
        score = 1.0
        violations = []

        for allergy in self.restricted_allergies:
            if allergy in text_lower:
                score -= 0.5
                violations.append(f"Allergen detected in output: '{allergy}'")

        final_score = max(0.0, score)
        passed = final_score >= self.threshold

        logger.info("AllergyComplianceMetric for %s: Score=%.2f, Passed=%s", self.restricted_allergies, final_score, passed)
        return {
            "score": final_score,
            "passed": passed,
            "violations": violations
        }
