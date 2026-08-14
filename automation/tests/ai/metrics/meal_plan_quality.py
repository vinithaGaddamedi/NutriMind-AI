import logging
from typing import Dict, Any

logger = logging.getLogger("MealPlanQualityMetric")

class MealPlanQualityMetric:
    """
    Evaluates the structural completeness and actionable quality of AI meal plan outputs.
    """

    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold

    def measure(self, output_text: str) -> Dict[str, Any]:
        text_lower = output_text.lower()
        score = 0.0
        details = []

        # Check for key structural components
        if any(w in text_lower for w in ["breakfast", "lunch", "dinner", "snack"]):
            score += 0.4
            details.append("Includes meal breakdown")

        if any(w in text_lower for w in ["calorie", "protein", "gram", "macro", "g"]):
            score += 0.3
            details.append("Includes nutritional metrics")

        if any(w in text_lower for w in ["recipe", "ingredient", "prep", "step"]):
            score += 0.3
            details.append("Includes actionable instructions")

        final_score = min(1.0, score)
        passed = final_score >= self.threshold

        logger.info("MealPlanQualityMetric: Score=%.2f, Passed=%s", final_score, passed)
        return {
            "score": final_score,
            "passed": passed,
            "details": details
        }
