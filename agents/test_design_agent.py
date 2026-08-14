import logging
from typing import Dict, Any, List
from agents.schemas.requirement_schema import RequirementModel

logger = logging.getLogger("TestDesignAgent")

class TestDesignAgent:
    """
    Generates multi-dimensional test scenarios (Positive, Negative, Boundary, Security, API, AI behavior).
    """

    def generate_scenarios(self, req: RequirementModel) -> List[Dict[str, Any]]:
        logger.info("Generating test scenarios for story %s...", req.story_id)
        scenarios = []

        # 1. Positive Scenario
        scenarios.append({
            "scenario_id": f"TS-{req.story_id}-001",
            "requirement_id": req.story_id,
            "type": "positive",
            "priority": "High",
            "description": f"Verify successful meal plan generation for story {req.story_id} with valid parameters.",
            "automation_candidate": True
        })

        # 2. Negative Scenario
        scenarios.append({
            "scenario_id": f"TS-{req.story_id}-002",
            "requirement_id": req.story_id,
            "type": "negative",
            "priority": "High",
            "description": "Verify error validation when submitting invalid caloric or empty profile fields.",
            "automation_candidate": True
        })

        # 3. AI Behavior / Constraint Scenario
        scenarios.append({
            "scenario_id": f"TS-{req.story_id}-003",
            "requirement_id": req.story_id,
            "type": "ai_behavior",
            "priority": "Critical",
            "description": "Verify AI compliance with peanut allergy constraint in meal output.",
            "automation_candidate": True
        })

        # 4. API Scenario
        scenarios.append({
            "scenario_id": f"TS-{req.story_id}-004",
            "requirement_id": req.story_id,
            "type": "api",
            "priority": "Medium",
            "description": "Verify POST /api/meal/meal-plan/single schema validation and HTTP status code.",
            "automation_candidate": True
        })

        return scenarios
