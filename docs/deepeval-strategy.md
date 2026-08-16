# DeepEval Evaluation Strategy

DeepEval represents our "Semantic Tier". It is an LLM-as-a-Judge framework used strictly where deterministic testing falls short.

## Core Metrics
1. **Faithfulness**: Does the AI's response contradict the provided context?
2. **Relevance**: Did the AI actually answer the user's question, or did it deflect?
3. **Hallucination**: Did the AI invent facts not present in its grounding data?

## Why DeepEval is Required
A traditional Playwright test can confirm that a chatbot UI rendered and returned a `200 OK` status with a text payload. However, a traditional test cannot confirm if the text payload is *good advice*. DeepEval provides the mathematical scoring to measure the *quality* of the generative output.

## The Limitation Rule
DeepEval is **NOT** used for hard business rules.
If a user has a Peanut Allergy, we do not ask DeepEval if the recipe is safe. LLMs are probabilistic and might fail to recognize an obscure peanut derivative. We use deterministic Python string/array matching for life-safety constraints, and leave DeepEval to judge the conversational quality of the response.
