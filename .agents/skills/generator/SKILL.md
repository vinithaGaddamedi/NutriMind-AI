---
name: Generator
description: Translates a JSON plan into executable Pytest Playwright code.
---

# Automation Generator Skill

**Purpose**: Answers "How do we implement the plan as Playwright automation?"
**Inputs**: `PlannerOutput` JSON, available Page Objects.
**Outputs**: Pytest/Playwright source code.

**Rules**:
- MUST use existing page objects if available.
- DO NOT invent duplicate utilities.
- Assume deterministic validators will check your output.
