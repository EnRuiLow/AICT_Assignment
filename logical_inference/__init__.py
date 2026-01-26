"""
Logical Inference Package for MRT Advisory Consistency
ChangiLink AI - Assignment Component

This package implements resolution-based inference for validating
MRT routing decisions and detecting contradictions in service advisories.

Author: [Your Name]
Student ID: [Your ID]
Module: AICT
"""

from .models import Proposition, Clause, NetworkMode, ServiceStatus
from .rules import LogicRule
from .knowledge_base import MRTKnowledgeBase
from .inference_engine import ResolutionEngine

__version__ = "1.0.0"
__all__ = [
    "Proposition",
    "Clause",
    "NetworkMode",
    "ServiceStatus",
    "LogicRule",
    "MRTKnowledgeBase",
    "ResolutionEngine",
]