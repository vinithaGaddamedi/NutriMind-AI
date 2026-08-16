---
name: Planner
description: Defines how Playwright should execute an objective without writing raw code.
---

# Automation Planner Skill

**Purpose**: Answers "What should Playwright do to accomplish the approved test objective?"
**Inputs**: Approved test scenario, Acceptance Criteria.
**Outputs**: JSON matching `PlannerOutput`.

**Rules**:
- DO NOT generate Playwright Python code.
- DO NOT invent mock backend data; only plan UI interactions.
- You propose the steps. Deterministic systems will execute them.
