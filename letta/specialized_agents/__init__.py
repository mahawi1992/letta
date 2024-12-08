"""
This module contains specialized agents that extend the base Letta agent functionality.
These agents are designed for specific tasks like research, coding, and orchestration.
"""

from .research_agent import ResearchAgent
from .coding_agent import CodingAgent
from .orchestrator import EnhancedOrchestratorAgent
from .memory_optimizer import MemoryOptimizer

__all__ = ['ResearchAgent', 'CodingAgent', 'EnhancedOrchestratorAgent', 'MemoryOptimizer']
