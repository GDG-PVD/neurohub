"""Core A2A functionality for the multi-agent system.

This module provides the base classes and utilities for building
A2A-compliant agents.
"""

# Export wrapper classes for workshop
from .a2a_wrappers import A2AAgent, A2ATask, A2AOrchestrator

# Also export original client classes if available
try:
    from .a2a_client import (
        A2AAgent as OriginalA2AAgent,
        A2AOrchestrator as OriginalA2AOrchestrator,
        AgentCapability,
        InteractionMode,
    )
    __all__ = [
        "A2AAgent",
        "A2ATask",
        "A2AOrchestrator",
        "OriginalA2AAgent",
        "OriginalA2AOrchestrator",
        "AgentCapability",
        "InteractionMode",
    ]
except ImportError:
    # Original client not available, use wrappers only
    __all__ = [
        "A2AAgent",
        "A2ATask",
        "A2AOrchestrator",
    ]