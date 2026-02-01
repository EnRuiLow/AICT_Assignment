"""
Re-Routing Optimisation Module

This module handles intelligent re-routing and optimization under disruption scenarios.
It implements local search and simulated annealing algorithms to minimize commuter delays
when network segments are disrupted or operating with reduced service.
"""

# Import key functions
import importlib.util
import sys
import os

# Load the module with spaces in its name
spec = importlib.util.spec_from_file_location(
    "rerouting_optimisation",
    os.path.join(os.path.dirname(__file__), "Re-Routing Optimisation.py")
)
rerouting_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rerouting_module)

# Export key functions
from_module = rerouting_module

__all__ = [
    'local_search',
    'simulated_annealing', 
    'optimize_under_disruption',
    'format_optimization_results',
    'is_path_valid',
    'path_cost_with_transfer',
    'count_transfers',
    'total_system_delay'
]

