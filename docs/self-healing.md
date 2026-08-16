# Self-Healing Governance

The NutriMind AI Framework features autonomous self-healing, but it operates under a strict, enterprise-grade governance model. 

## The Healing Loop
1. Playwright throws a `TimeoutError` because a UI button was renamed.
2. The `FailureAgent` classifies the failure as a `LOCATOR_FAILURE`.
3. The `SelfHealingService` retrieves the DOM snapshot at the time of failure, locates the new semantic match for the button, and generates a Unified Diff `.patch` file.

## Human-in-the-Loop Governance
The framework **never silently modifies and merges production code**. 
While the AI generates the exact Git patch required to fix the repository, it halts execution and requests human approval (`Y/N`). 

### Why?
1. **Security**: An AI should never unilaterally rewrite API logic or frontend behavior without a human auditor.
2. **Quality Control**: The AI might find a "workaround" that technically passes the test but breaks a UX pattern. 
3. **Traceability**: Changes to the codebase must be traceable back to a specific intent, not just a black-box autonomous action.
