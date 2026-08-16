# Golden Dataset Strategy

Our framework learns continuously through the **Golden Dataset Strategy**. A golden dataset is a collection of perfect `Input -> Expected State` mappings.

## Hallucination Prevention & Prompt Regressions
Whenever we update our AI System Prompts, there is a risk of degrading the agent's intelligence. To prevent this, we maintain a vast library of Goldens representing complex test scenarios (e.g., contradictory allergies, malicious prompt injections). 

Before a new System Prompt is promoted to production, the `prompt_regression_runner` tests the new prompt against the entire Golden dataset. If the DeepEval Hallucination score spikes, or if the Constraint Compliance drops below a hardcoded boundary, the prompt update is automatically rejected.

## Closing the Loop
Whenever a true defect is found in the application (and fixed via Self-Healing), the execution path is automatically serialized and appended to the Golden Dataset. This ensures the framework never forgets a previous failure, building a permanent, ever-growing regression suite.
