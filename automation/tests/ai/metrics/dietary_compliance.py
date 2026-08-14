import logging
from typing import Dict, Any, List

logger = logging.getLogger("DietaryComplianceMetric")

class DietaryComplianceMetric:
    """
    Evaluates whether an AI generated output complies strictly with dietary restrictions
    (e.g., vegetarian, vegan, keto, high-protein).
    """

    MEAT_TERMS = ["chicken", "beef", "pork", "turkey", "bacon", "salmon", "tuna", "fish", "lamb", "steak", "shrimp"]

    def __init__(self, target_diet: str = "vegetarian", threshold: float = 0.9):
        self.target_diet = target_diet.lower()
        self.threshold = threshold

    def measure(self, output_text: str) -> Dict[str, Any]:
        text_lower = output_text.lower()
        score = 1.0
        violations = []

        if "vegetarian" in self.target_diet or "vegan" in self.target_diet:
            for term in self.MEAT_TERMS:
                if term in text_lower:
                    score -= 0.3
                    violations.append(f"Found prohibited meat term: '{term}'")

        if "keto" in self.target_diet:
            prohibited_keto = ["sugar", "pasta", "white bread", "rice", "candy"]
            for term in prohibited_keto:
                if term in text_lower:
                    score -= 0.2
                    violations.append(f"Found high-carb term in keto plan: '{term}'")

        final_score = max(0.0, score)
        passed = final_score >= self.threshold

        logger.info("DietaryComplianceMetric for '%s': Score=%.2f, Passed=%s", self.target_diet, final_score, passed)
        return {
            "score": final_score,
            "passed": passed,
            "violations": violations
        }
