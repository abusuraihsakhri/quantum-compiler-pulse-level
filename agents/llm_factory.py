"""
Inference Engine supporting local Ollama, Claude, OpenAI, and deterministic Mock with Zero-PHI checks.
"""
from typing import Dict, Any, Optional
from .base import PHIGuard


class MockLLM:
    def __init__(self, system_name: str = "Quantum Compiler Pulse Level"):
        self.system_name = system_name

    def invoke(self, prompt: str) -> str:
        PHIGuard.assert_no_phi(prompt)
        return f"[{self.system_name} mock]: No external model was called and no scientific or standards verification was performed. Query: '{prompt[:60]}...'"


class LLMFactory:
    """Creates configured LLM client instances with zero-PHI protection."""

    @staticmethod
    def create(provider: str = "mock", system_name: str = "Quantum Compiler Pulse Level"):
        prov = str(provider).lower()
        if prov in ["mock", "deterministic", "test"]:
            return MockLLM(system_name)
        raise ValueError(f"Unsupported model provider: {provider!r}. Only the mock provider is implemented.")
