import sys
import os
import json
import logging
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.base_agent import BaseAgent
from agents.schemas.base_agent_schema import AgentInput, AgentOutput
from agents.schemas.optimization_schemas import OptimizationInput, OptimizationReport

logger = logging.getLogger("TestOptimizationAgent")

class TestOptimizationAgent(BaseAgent[OptimizationReport]):
    """
    Intelligent test suite orchestrator.
    Filters the available testing pool into PR, Nightly, and Release suites 
    based on risk, historical failure rates, changed code, and flakiness.
    """
    def __init__(self, provider_name: str = None):
        super().__init__("TestOptimizationAgent", provider_name)

    def optimize_suites(self, payload: OptimizationInput) -> AgentOutput[OptimizationReport]:
        logger.info("Optimizing suites for %d available tests with %d changed files...", 
                    len(payload.available_tests), len(payload.changed_code))
        
        system_prompt = (
            "You are an expert AI Test Optimization Agent. "
            "You receive a pool of available tests, recent code changes, and test metadata (risk, duration, flakiness). "
            "Your objective is to allocate these tests into three suites: PR, Nightly, and Release. "
            "CRITICAL RULES: "
            "1. Do not delete tests. Every test MUST appear in the 'release_suite'. "
            "2. 'pr_suite' should be lean. Only include tests that map to the 'changed_code', are 'Critical/High' risk, "
            "or have high historical failure rates. DO NOT include known flaky tests or highly long-running tests in the PR suite. "
            "3. 'nightly_suite' includes everything in the PR suite plus long-running, medium-risk, or flaky tests. "
            "4. You must provide a specific 'reasoning' string for EVERY test you select in each suite."
        )

        prompt = f"""
        Optimization Input:
        {payload.model_dump_json(indent=2)}
        """
        
        input_data = AgentInput(
            prompt=prompt,
            system_instruction=system_prompt
        )
        return self.execute(input_data, OptimizationReport)
