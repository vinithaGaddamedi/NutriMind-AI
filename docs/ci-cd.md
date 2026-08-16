# CI/CD and AI Quality Gates

The NutriMind architecture natively embeds the Agentic QA framework into GitHub Actions, ensuring zero-touch deployments backed by AI rigorous validation.

## Pipeline Architecture
1. **PR Pipeline (`pr_pipeline.yml`)**: Fast, heavily parallelized. Runs deterministic unit/API/UI testing. It blocks bad code from merging into `main`.
2. **Nightly Pipeline (`nightly_pipeline.yml`)**: Runs deeper, token-heavy semantic evaluation via DeepEval and complex Security Prompt Injection suites. 
3. **Release Pipeline (`release_pipeline.yml`)**: The exhaustive suite orchestrator. Generates the final Executive Enterprise Report.

## The AI Quality Gate
At the end of every pipeline sits the **AI Quality Gate**.

This gate operates on strict, JSON-configured rules (`quality_gate_thresholds.json`). It guarantees that AI evaluations don't become subjective. 

If the aggregate test payload reveals that the AI Chatbot's **Hallucination Rate** exceeded 5%, the gate `FAIL`s the GitHub Action, hard-blocking the release. It removes the need for a human QA manager to comb through logs to determine if an AI model degradation occurred.
