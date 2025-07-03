"""
AGI System - An Educational Artificial General Intelligence Implementation

This package demonstrates key concepts of AGI including:
- Reasoning and problem-solving
- Learning from experience
- Goal-setting and planning
- Multi-domain capability
- Self-improvement mechanisms
"""

from .core.agi import AGI
from .agents.reasoning_agent import ReasoningAgent
from .environments.task_environment import TaskEnvironment

__version__ = "0.1.0"
__all__ = ["AGI", "ReasoningAgent", "TaskEnvironment"]
