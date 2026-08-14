from abc import ABC, abstractmethod
from typing import Optional

class AIProvider(ABC):
    """
    Abstract Base Class defining the contract for AI providers in the Quality Engineering Framework.
    """

    @abstractmethod
    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """
        Generate text response for a given prompt with optional system instruction.
        """
        pass

    @abstractmethod
    def analyze_failure(self, error_message: str, stack_trace: str, page_dom: Optional[str] = None) -> str:
        """
        Analyze E2E test failure logs and return a detailed markdown diagnostic report.
        """
        pass

    @abstractmethod
    def generate_test_code(self, source_code: str, requirements: Optional[str] = None) -> str:
        """
        Generate automated test script code from component source code or feature specification.
        """
        pass
