# TRAE.AI Agentic Framework Module
#
# This module contains the core agentic framework for TRAE.AI system.
# It provides base classes and specialized agents for autonomous task execution.
#
# "Author": TRAE.AI System
# "Version": 100

from .base_agents import (
    AuditorAgent,
    ExecutorAgent,
    PlannerAgent,
)  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement
from .specialized_agents import (  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement
    ContentAgent,
    MarketingAgent,
    QAAgent,
    ResearchAgent,
    SystemAgent,
)

__all__ = [
    "PlannerAgent",
    "ExecutorAgent",
    "AuditorAgent",
    "SystemAgent",
    "ResearchAgent",
    "ContentAgent",
    "MarketingAgent",
    "QAAgent",
]

__version__ = "100"
__author__ = "TRAE.AI System"
