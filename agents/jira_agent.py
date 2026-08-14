import logging
from typing import Dict, Any

logger = logging.getLogger("JiraAgent")

class JiraAgent:
    """
    Automates Jira defect creation formatting failure evidence, logs, traces, and AI RCA.
    """

    def format_defect_payload(
        self,
        story_id: str,
        test_case_id: str,
        environment: str,
        steps: str,
        expected: str,
        actual: str,
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        logger.info("Formatting Jira defect payload for %s / %s...", story_id, test_case_id)

        defect = {
            "project": "MEAL",
            "issue_type": "Bug",
            "summary": f"[AI Auto-Defect] [{analysis.get('failure_type', 'DEFECT')}] {test_case_id}: {actual[:80]}",
            "story_id": story_id,
            "test_case_id": test_case_id,
            "environment": environment,
            "description": f"""h2. Issue Description
*Story ID:* {story_id}
*Test Case:* {test_case_id}
*Environment:* {environment}

h3. Reproduction Steps
{steps}

h3. Expected Result
{expected}

h3. Actual Result
{actual}

h3. 🤖 AI Root Cause Analysis (RCA)
*Failure Classification:* {analysis.get('failure_type', 'UNKNOWN')}
*Root Cause:* {analysis.get('root_cause', 'N/A')}
*AI Confidence Score:* {analysis.get('confidence', 0.90):.2f}
*Recommended Action:* {analysis.get('recommended_action', 'Investigate')}
""",
            "priority": "High" if analysis.get('failure_type') == "APPLICATION_DEFECT" else "Medium",
            "labels": ["automated-test-failure", "ai-rca", analysis.get("failure_type", "bug").lower()]
        }

        logger.info("Created Jira defect payload for summary: '%s'", defect["summary"])
        return defect
