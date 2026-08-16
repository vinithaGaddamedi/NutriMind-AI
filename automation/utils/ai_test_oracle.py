import os
import json
from pydantic import BaseModel, Field
from typing import List, Optional
from google import genai
from google.genai import types

class OracleDecision(BaseModel):
    passed: bool = Field(..., description="Whether the actual output satisfies expected behavior and constraints.")
    reason: str = Field(..., description="Detailed explanation for the pass/fail decision.")
    violations: List[str] = Field(default_factory=list, description="List of specific constraints violated.")
    confidence: float = Field(..., description="Confidence score from 0.0 to 1.0.")

class AITestOracle:
    """
    Evaluates unstructured AI outputs logically without requiring strict exact-match string comparison.
    """
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            # We allow mocking when API key is not present for CI/CD
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name

    def evaluate(self, 
                 actual_output: str, 
                 expected_behavior: str, 
                 constraints: List[str], 
                 context: dict = None) -> OracleDecision:
        
        if not self.client or os.getenv("MOCK_LLM_EVALS") == "true":
            # Mock behavior based on simple heuristics to save API credits in CI
            return self._mock_evaluate(actual_output, expected_behavior, constraints)

        prompt = f"""
        You are an AI Test Oracle. Your job is to determine if the ACTUAL OUTPUT satisfies the EXPECTED BEHAVIOR and adheres to all CONSTRAINTS.

        EXPECTED BEHAVIOR:
        {expected_behavior}

        CONSTRAINTS:
        {json.dumps(constraints, indent=2)}

        CONTEXT:
        {json.dumps(context or {}, indent=2)}

        ACTUAL OUTPUT:
        {actual_output}

        Evaluate critically. Return a JSON object matching the requested schema.
        If a constraint is violated, passed MUST be false and violations MUST be listed.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=OracleDecision,
                    temperature=0.0
                ),
            )
            
            raw_text = response.text
            # Sometimes Gemini returns markdown blocks even with json mime type.
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            
            data = json.loads(raw_text.strip())
            return OracleDecision(**data)
            
        except Exception as e:
            # Fallback for API failure
            return OracleDecision(
                passed=False,
                reason=f"Oracle execution failed: {str(e)}",
                violations=["ORACLE_ERROR"],
                confidence=0.0
            )

    def _mock_evaluate(self, actual_output: str, expected_behavior: str, constraints: List[str]) -> OracleDecision:
        """Naive evaluation for unit testing."""
        actual_lower = actual_output.lower()
        violations = []
        passed = True
        
        # If 'fail' or 'wrong' is explicitly in the mock output, force failure
        if "fail_mock" in actual_lower:
            passed = False
            violations.append("Mock forced failure")
            
        return OracleDecision(
            passed=passed,
            reason="Mock evaluation.",
            violations=violations,
            confidence=1.0
        )
