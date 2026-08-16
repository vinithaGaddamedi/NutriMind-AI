import logging
import os
from typing import Dict, Any

from agents.base_agent import BaseAgent
from agents.schemas.base_agent_schema import AgentMetadata, AgentOutput
from agents.schemas.execution_schemas import HealingProposal

logger = logging.getLogger("SelfHealingPatchAgent")

class SelfHealingPatchAgent(BaseAgent[HealingProposal]):
    """
    Generates Git Diff patch proposals for failed locators or broken assertions.
    Ensures safe Human-In-The-Loop approval workflow before merging.
    """
    
    def __init__(self, provider_name: str = None):
        super().__init__("SelfHealingPatchAgent", provider_name)

    def propose_patch(self, file_path: str, old_selector: str, new_selector: str) -> AgentOutput[HealingProposal]:
        logger.info("Generating Git diff patch for %s...", file_path)
        
        diff_patch = f"""--- a/{file_path}
+++ b/{file_path}
@@ -12,3 +12,3 @@
-    BUTTON_LOCATOR = "{old_selector}"
+    BUTTON_LOCATOR = "{new_selector}"
"""
        
        patch_dir = "automation/reports/patches"
        os.makedirs(patch_dir, exist_ok=True)
        patch_file = os.path.join(patch_dir, "self_healing.patch")
        
        with open(patch_file, "w") as f:
            f.write(diff_patch)
            
        logger.info("Patch file generated at %s", patch_file)

        proposal = HealingProposal(
            test_case_id="NEEDS_CLARIFICATION", # Can be passed in later if available
            patch_file_path=patch_file,
            git_diff=diff_patch,
            status="PROPOSED_PATCH_WAITING_HUMAN_APPROVAL"
        )
        
        metadata = AgentMetadata(
            agent_name=self.agent_name,
            correlation_id="local-patch-gen",
            latency_ms=0
        )
        
        return AgentOutput[HealingProposal](data=proposal, metadata=metadata)
