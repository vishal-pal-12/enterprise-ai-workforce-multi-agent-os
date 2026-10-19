from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseEnterpriseAgent(ABC):
    """
    Standard modular interface for all enterprise agents:
    - Sales Intelligence Agent
    - CEO Orchestrator Agent
    - HR Agent
    - Finance Agent
    """
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    @abstractmethod
    def execute(self, objective: str, max_steps: int = 8) -> Dict[str, Any]:
        """
        Executes a business objective through the bounded agentic loop:
        PLAN -> SELECT TOOL -> EXECUTE -> OBSERVE -> EVALUATE -> FINISH
        """
        pass
