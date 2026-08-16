# Cognizant Lead QA - 10-Minute Demo Script

*Use this script when demonstrating the NutriMind AI QA Framework to stakeholders or interviewing for a Lead QA / SDET position.*

## Preparation
- Open a terminal at the root of the project.
- Open VS Code to the `reports/` folder.
- Have this script handy.

---

## 0:00 - 2:00 | Introduction & Architecture
**Speaker Track**: 
"Hello everyone, I'm here to demonstrate the NutriMind Agentic QA Framework. Traditional automation frameworks break when buttons move, and they struggle to test generative AI outputs. We solved this by building a constellation of 10 specialized AI agents that handle the entire SDLC—from reading Jira stories to writing code, evaluating semantics, and even self-healing failures."

**Action**: Share the screen showing the `docs/architecture.md` Mermaid diagram.

**Speaker Track**: 
"Our core philosophy is simple: **We do not trust the AI.** We use AI for generative test design and DeepEval semantics, but we *never* use AI for hard business rules. If a user has a peanut allergy, we enforce that constraint using deterministic Python. If it fails, it fails hard."

---

## 2:00 - 5:00 | The E2E Demo Execution
**Speaker Track**: 
"Rather than show you slides, I'm going to run a live simulation. We're going to feed the framework a raw Jira story about a user with a Peanut Allergy. We're going to let the agents design the tests and run them. Then, we are going to programmatically inject a defect into the backend API to break the allergy logic, and watch how the system reacts."

**Action**: In the terminal, execute:
```bash
./scripts/run_demo.sh
```

**Speaker Track** (while it runs):
- "Here you can see the `RequirementAgent` and `RiskAgent` pulling the constraints out of the text."
- "Now the `AutomationAgent` generated the Playwright script. The first run passes."
- "Look here—the script just monkey-patched the API code to ignore the peanut allergy. This simulates a bad developer commit."
- "The framework caught it! The Deterministic Validator just threw an error because it found 'peanut' in the response."

---

## 5:00 - 8:00 | Self-Healing Governance
**Speaker Track**:
"Because the pipeline failed, the `FailureAgent` took over. It grabbed the stack trace, ran a Root Cause Analysis, and figured out the API logic was broken. Now, it has handed off to the `SelfHealingService`."

**Action**: Wait for the script to pause at `[Human Gate] Approve this patch? (Y/N): `

**Speaker Track**:
"This is our strict **Human-in-the-loop Governance**. The AI has generated the exact Git `.patch` file required to fix the developer's mistake. But we never allow AI to silently modify and merge production code. As the QA Lead, I review the patch. It looks correct, so I will approve it."

**Action**: Press `Y` and Enter.

**Speaker Track**: 
"The system applied the fix, re-ran the test, and verified it passed. It also saved that execution path into our **Golden Dataset** so we can never regress on this specific failure again."

---

## 8:00 - 10:00 | The Executive Quality Gate
**Action**: Open `reports/enterprise_report.html` in the browser.

**Speaker Track**:
"Finally, the `EnterpriseReporter` aggregates the traceability, coverage, and DeepEval scores into this HTML dashboard. Our CI/CD pipeline reads from a JSON config file. If the AI Quality Score drops below 85%, or if we find 1 critical security injection failure, the **AI Quality Gate** fails the GitHub Action and blocks the deployment."

"What you just saw was an autonomous system shifting quality left to the requirements phase, catching a defect in execution, writing the code to fix the defect, asking for human permission, and then passing the release gate. Thank you."
