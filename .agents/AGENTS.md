# NutriMind-AI Enterprise Quality Engineering Rules

These rules dictate how this repository should be evolved into an enterprise-grade AI-powered Quality Engineering / Agentic QA framework.

1. Inspect the existing repository before changing anything.
2. Reuse existing functionality whenever possible.
3. Do not create duplicate frameworks, utilities, fixtures, page objects, API clients, or AI services.
4. Do not invent files, APIs, selectors, business rules, requirements, acceptance criteria, or test data.
5. If information is unavailable, explicitly report: NEEDS_CLARIFICATION
6. Do not hardcode secrets.
7. Use environment variables for credentials.
8. Do not expose API keys in logs.
9. Use Gemini through a reusable LLM provider abstraction.
10. Agents must return structured outputs.
11. Validate agent outputs using Pydantic/schema validation.
12. Do not allow one agent's unvalidated output to become another agent's source of truth.
13. Deterministic business rules must remain deterministic.
14. DeepEval should be used for semantic/LLM evaluation.
15. AI-generated code must be validated by execution.
16. Self-healing must generate a patch proposal, not silently modify and merge production code.
17. High-risk changes require human approval.
18. Every generated test must maintain requirement traceability.
19. Every AI evaluation must have reproducible input/golden data.
20. Prefer small, testable components over a giant agent.
21. Do not change unrelated functionality.
22. After every implementation, provide:
    - files changed
    - files created
    - files deleted
    - architecture changes
    - tests executed
    - test results
    - known limitations

## Development process:

INSPECT → DESIGN → IMPLEMENT → TEST → REVIEW

Do not implement anything until explicitly requested in each phase.
