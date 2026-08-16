# Architecture Gap Analysis

## 1. Current Architecture
The NutriMind AI Framework currently features a flat, 20-agent architecture located inside the root `agents/` directory. It utilizes an `orchestrator.py` to pass Jira stories through Requirement, Risk, and Test Design phases, eventually handing off to an `automation_agent.py` which generates Playwright strings. We utilize DeepEval for semantic checks and have built a self-healing patch service.

## 2. Current Agents vs Proposed Architecture

**Current Flat Directory:**
`jira_agent.py`, `requirement_agent.py`, `risk_agent.py`, `test_design_agent.py`, `manual_test_agent.py`, `automation_agent.py`, `failure_agent.py`, `self_healing_agent.py`, `reporting_agent.py`, `mcp_server.py`, `orchestrator.py` (and others).

**Proposed Layered Directory:**
- `agents/orchestration/`
- `agents/shift_left/`
- `agents/automation/`
- `agents/intelligence/`
- `agents/infrastructure/`

## 3. Duplicate/Overlapping Responsibilities
- **Automation Generation:** Currently, `automation_agent.py` takes test scenarios and directly spits out Python code. It is acting as both the Planner ("What should we click?") and the Generator ("Write the page.locator syntax"). It lacks a Validator step.
- **Healing:** We have a `self_healing_agent.py` and a `automation/utils/self_healing_service.py` which duplicate execution paths. This must be merged into a single `healer_agent.py`.

## 4. Current Gaps
1. **Automation Strategy:** We are missing the strict `Planner -> Generator -> Validator` pipeline for automation scripts.
2. **Real vs Mock Execution:** While our CI/CD runs Playwright tests, the internal agent feedback loop sometimes relies on hardcoded string injection (e.g. simulating a failure in the demo script via text replacement rather than a real DOM mismatch).
3. **DeepEval:** Some early unit tests may use simulated `0.94` scores to test logic gates instead of invoking the real LLM-as-a-judge metric.
4. **Chatbot Tools:** The chatbot needs stricter capability definitions for fetching real user preferences and allergy states rather than hallucinating them.

## 5. Files That Will Change
- `agents/*`: Almost all agent files will be moved into subdirectories, requiring massive import refactoring across the entire repository (`automation/`, `backend/`, `tests/`).
- `automation/demo_e2e_lifecycle.py`: Will be rewritten to consume the new `AutomationOrchestrator`.
- `docs/*`: Architecture docs will be updated to reflect the Planner/Generator/Validator paradigm.

## 6. Files That Will NOT Change
- `backend/routes/` and `web-app/` core business logic (excluding the Chatbot API upgrades).
- `automation/api_tests/` and legacy `ui_tests/` (these just need to continue passing).
- `automation/config/quality_gate_thresholds.json` (the rules remain the same).

## 7. Risks of Refactoring
Moving `agents/` into subdirectories will break hundreds of import paths across 100+ files. We must approach Phase 1 very carefully, utilizing `sys.path` or modifying the package `__init__.py` files to ensure module resolution does not catastrophically fail. Re-wiring the `AutomationAgent` into three separate agents (Planner/Gen/Val) risks breaking the seamless E2E demo we just built if the prompt schemas do not perfectly align.
