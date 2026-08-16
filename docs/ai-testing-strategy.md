# AI Testing Strategy

The NutriMind architecture does not rely on a single monolith to test AI. It uses a cascading multi-tier strategy.

## Multi-Tiered Pipeline

1. **Unit Tier (Python/Pytest)**
   - Tests basic schema validation.
   - Proves that the endpoints are alive and JSON parsing works.
2. **API Tier (Deterministic Validators)**
   - Validates that the AI models do not violate hard business rules.
   - If an AI meal planner returns a "peanut" string for a user with a peanut allergy, it fails *deterministically* via Python `assert`, bypassing any LLM logic.
3. **Semantic Tier (DeepEval)**
   - Used *only* for non-deterministic evaluations.
   - Checks conversational AI tone, context retention across multi-turn chats, and hallucination bounds.
4. **Agent Tier**
   - Tests the QA agents themselves.
   - Evaluates if the `TestDesignAgent` hallucinated an API endpoint that doesn't exist.

## The AI Oracle
We use an **AI Test Oracle** to evaluate generative outputs where exact string matching is impossible (e.g. "Create a welcoming greeting"). The Oracle provides a `PASS/FAIL` confidence score. However, *the Oracle is strictly forbidden from overriding deterministic validators*. If the determinist validator flags an allergy violation, the Oracle cannot "save" the test run, even if it thinks the recipe looks tasty.
