import os
import uuid
import json
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from google import genai
from google.genai import types

class SelfHealingProposal(BaseModel):
    original_locator: str = Field(..., description="The locator that failed")
    candidate_locator: str = Field(..., description="The suggested stable replacement locator")
    reason: str = Field(..., description="Why this candidate is robust and correct")
    confidence: float = Field(..., description="Confidence score 0.0-1.0")
    patch_content: str = Field(..., description="The unified diff patch content to fix the file")

class SelfHealingService:
    """
    Analyzes DOM snapshots to propose self-healing locator patches for Playwright tests.
    Strictly follows the proposal workflow: generates patches instead of silently mutating code.
    """
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name

    def generate_healing_proposal(
        self, 
        failed_locator: str, 
        dom_snippet: str, 
        file_path: str
    ) -> SelfHealingProposal:
        
        if not self.client or os.getenv("MOCK_LLM_EVALS") == "true":
            # Mock behavior
            mock_patch = f"""--- {file_path}
+++ {file_path}
@@ -10,3 +10,3 @@
-    page.click("{failed_locator}")
+    page.click("button:has-text('Submit')")
"""
            return SelfHealingProposal(
                original_locator=failed_locator,
                candidate_locator="button:has-text('Submit')",
                reason="Mock reasoning: 'Submit' text is more robust than CSS class.",
                confidence=0.9,
                patch_content=mock_patch
            )

        prompt = f"""
        You are a Self-Healing QA Agent. A Playwright test failed because the locator could not be found.
        
        FAILED LOCATOR: {failed_locator}
        FILE PATH: {file_path}
        
        CURRENT DOM SNIPPET:
        ```html
        {dom_snippet}
        ```
        
        Identify the correct element in the DOM. Generate a stable, robust Playwright candidate locator (prefer ARIA roles, test-ids, or text over brittle CSS).
        Generate a Unified Diff patch that replaces the old locator with the new locator.
        Return a JSON object conforming to the schema.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=SelfHealingProposal,
                    temperature=0.0
                ),
            )
            raw_text = response.text
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            
            data = json.loads(raw_text.strip())
            return SelfHealingProposal(**data)
            
        except Exception as e:
            raise RuntimeError(f"Self-healing generation failed: {str(e)}")

    def write_patch(self, proposal: SelfHealingProposal, output_dir: str) -> str:
        """Writes the patch to a file for human review, adhering to 'Safe Self-Healing' rules."""
        if proposal.confidence < 0.7:
            raise ValueError(f"Rejecting low-confidence fix: {proposal.confidence}")
            
        patch_id = uuid.uuid4().hex[:6]
        patch_path = os.path.join(output_dir, f"self_heal_{patch_id}.patch")
        
        with open(patch_path, "w") as f:
            f.write(proposal.patch_content)
            
        return patch_path
