"""Core A2A functionality for the multi-agent system.

This module provides the base classes and utilities for building
A2A-compliant agents.
"""

from .a2a_client import (
    A2AAgent,
    A2AOrchestrator,
    AgentCapability,
    InteractionMode,
)

__all__ = [
    "A2AAgent",
    "A2AOrchestrator",
    "AgentCapability",
    "InteractionMode",
]