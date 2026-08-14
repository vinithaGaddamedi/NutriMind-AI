import logging
from typing import Dict, Any, List
from agents.schemas.requirement_schema import RequirementModel

logger = logging.getLogger("RiskAgent")

class RiskAgent:
    """
    Risk Assessment Agent evaluating quality risks, severity, probability,
    priority matrix, and mapping to recommended test cases.
    """

    def evaluate_risks(self, req: RequirementModel) -> Dict[str, Any]:
        logger.info("Evaluating quality risks for story %s...", req.story_id)
        
        risks = []
        for i, risk_desc in enumerate(req.risks, 1):
            severity = "Critical" if "allergy" in risk_desc.lower() or "prohibited" in risk_desc.lower() else "High"
            priority = "P0" if severity == "Critical" else "P1"
            
            risks.append({
                "risk_id": f"RSK-00{i}",
                "risk": risk_desc,
                "severity": severity,
                "probability": "Medium",
                "priority": priority,
                "recommended_tests": ["AI-002", f"TC-{req.story_id}-00{i}"]
            })

        if not risks:
            risks.append({
                "risk_id": "RSK-001",
                "risk": "Allergy constraint ignored or ingredient mismatch",
                "severity": "Critical",
                "probability": "Medium",
                "priority": "P0",
                "recommended_tests": ["AI-002"]
            })

        return {
            "story_id": req.story_id,
            "risks": risks
        }
