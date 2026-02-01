"""
Re-Routing Optimisation

This module handles intelligent re-routing and optimization under disruption scenarios.
It implements local search and simulated annealing algorithms to minimize commuter delays
when network segments are disrupted or operating with reduced service.

The optimization model combines:
- Hard constraints: prevent traversal of suspended segments
- Soft constraints: model reduced service frequencies and transfer congestion
- Objective: minimize average commuter delay across multiple origin-destination pairs

Key Features:
- Disruption detection and validation
- Path cost calculation with transfer penalties
- Local search optimization
- Simulated annealing for global optimization
- Performance comparison against baseline conditions
"""

import random
import math


# =====================================================
# DISRUPTIONS
# =====================================================

# Disruption 1: Segment Suspension (Hard Constraint)
# Tanah Merah – Expo closed
DISRUPTED_EDGES_1 = {
    ("Tanah Merah", "Expo"),
    ("Expo", "Tanah Merah")
}

# Disruption 2: Reduced Service (Soft Constraint)
# Expo – Changi Airport reduced frequency
EDGE_PENALTIES = {
    ("Expo", "Changi Airport"): 5,
    ("Changi Airport", "Expo"): 5
}

# Transfer penalty (used in cost function)
TRANSFER_PENALTY = 2


# =====================================================
# CONSTRAINT FUNCTIONS
# =====================================================

def count_transfers(path, station_line):
    """Count number of line transfers in a path"""
    transfers = 0
    for i in range(len(path) - 1):
        if station_line[path[i]] != station_line[path[i + 1]]:
            transfers += 1
    return transfers


def is_path_valid(path, disrupted_edges):
    """Hard constraint: avoid closed segments"""
    for i in range(len(path) - 1):
        if (path[i], path[i + 1]) in disrupted_edges:
            return False
    return True


# =====================================================
# COST FUNCTION
# =====================================================

def path_cost_with_transfer(path, graph, station_line):
    """
    Calculate total path cost including:
    - Edge weights
    - Reduced service penalties
    - Transfer penalties
    """
    cost = 0

    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]

        # Edge cost
        cost += graph[u][v]

        # Reduced service penalty
        if (u, v) in EDGE_PENALTIES:
            cost += EDGE_PENALTIES[(u, v)]

        # Transfer penalty
        if station_line[u] != station_line[v]:
            cost += TRANSFER_PENALTY

    return cost


# =====================================================
# OBJECTIVE FUNCTION
# =====================================================

def total_system_delay(state, baseline_costs, graph, station_line):
    """Calculate total average system delay across all OD pairs"""
    total_delay = 0

    for od, path in state.items():
        disrupted_cost = path_cost_with_transfer(path, graph, station_line)
        total_delay += disrupted_cost - baseline_costs[od]

    return total_delay / len(state)


# =====================================================
# NEIGHBOR GENERATION (LOCAL SEARCH)
# =====================================================

def generate_neighbor(state, od_pair, graph, station_line, astar_func):
    """Generate neighboring solution by re-routing one OD pair"""
    start, goal = od_pair

    # A* with random tie-breaking
    new_path, _ = astar_func(
        graph,
        start,
        goal,
        station_line,
    )

    new_state = state.copy()
    new_state[od_pair] = new_path
    return new_state


# =====================================================
# OPTIMIZATION ALGORITHMS
# =====================================================

def local_search(initial_state, baseline_costs, graph, station_line, astar_func,
                 disrupted_edges, iterations=100):
    """
    Local search optimization to minimize system delay
    
    Args:
        initial_state: Dictionary of OD pairs and their paths
        baseline_costs: Dictionary of baseline costs for each OD pair
        graph: Network graph
        station_line: Station to line mapping
        astar_func: A* algorithm function
        disrupted_edges: Set of disrupted edges
        iterations: Number of iterations
        
    Returns:
        Optimized state and its cost
    """
    current = initial_state.copy()
    current_cost = total_system_delay(
        current,
        baseline_costs,
        graph,
        station_line
    )

    for _ in range(iterations):
        od = random.choice(list(current.keys()))
        neighbor = generate_neighbor(
            current,
            od,
            graph,
            station_line,
            astar_func
        )

        if not is_path_valid(neighbor[od], disrupted_edges):
            continue

        new_cost = total_system_delay(
            neighbor,
            baseline_costs,
            graph,
            station_line
        )

        if new_cost < current_cost:
            current = neighbor
            current_cost = new_cost

    return current, current_cost


def simulated_annealing(initial_state, baseline_costs, graph, station_line, astar_func,
                       disrupted_edges, iterations=200, initial_temp=1.0, cooling_rate=0.95):
    """
    Simulated annealing optimization to escape local optima
    
    Args:
        initial_state: Dictionary of OD pairs and their paths
        baseline_costs: Dictionary of baseline costs for each OD pair
        graph: Network graph
        station_line: Station to line mapping
        astar_func: A* algorithm function
        disrupted_edges: Set of disrupted edges
        iterations: Number of iterations
        initial_temp: Initial temperature
        cooling_rate: Temperature cooling rate (0 < cooling_rate < 1)
        
    Returns:
        Optimized state and its cost
    """
    current = initial_state.copy()
    current_cost = total_system_delay(
        current,
        baseline_costs,
        graph,
        station_line
    )

    T = initial_temp

    for _ in range(iterations):
        od = random.choice(list(current.keys()))
        neighbor = generate_neighbor(
            current,
            od,
            graph,
            station_line,
            astar_func
        )

        if not is_path_valid(neighbor[od], disrupted_edges):
            continue

        new_cost = total_system_delay(
            neighbor,
            baseline_costs,
            graph,
            station_line
        )

        delta = new_cost - current_cost

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = neighbor
            current_cost = new_cost

        T *= cooling_rate

    return current, current_cost


# =====================================================
# OPTIMIZATION ORCHESTRATOR
# =====================================================

def optimize_under_disruption(initial_state, baseline_costs, graph, station_line, astar_func,
                             disrupted_edges, use_local_search=True, use_simulated_annealing=True):
    """
    Perform both local search and simulated annealing optimization
    
    Args:
        initial_state: Initial routing state
        baseline_costs: Baseline costs for each OD pair
        graph: Network graph
        station_line: Station to line mapping
        astar_func: A* algorithm function
        disrupted_edges: Set of disrupted edges
        use_local_search: Whether to run local search
        use_simulated_annealing: Whether to run simulated annealing
        
    Returns:
        Dictionary containing optimization results
    """
    results = {}

    if use_local_search:
        ls_state, ls_cost = local_search(
            initial_state, baseline_costs, graph, station_line,
            astar_func, disrupted_edges
        )
        results['local_search'] = {
            'state': ls_state,
            'cost': ls_cost
        }

    if use_simulated_annealing:
        sa_state, sa_cost = simulated_annealing(
            initial_state, baseline_costs, graph, station_line,
            astar_func, disrupted_edges
        )
        results['simulated_annealing'] = {
            'state': sa_state,
            'cost': sa_cost
        }

    return results


# =====================================================
# RESULT FORMATTING
# =====================================================

def format_optimization_results(results):
    """Format and display optimization results"""
    print("\n" + "="*80)
    print("  RE-ROUTING OPTIMISATION RESULTS")
    print("="*80)

    for method, data in results.items():
        print(f"\n{method.upper().replace('_', ' ')}:")
        print(f"  Average Delay: {data['cost']:.2f} units")
        print(f"  Optimized Routes:")
        for od, path in data['state'].items():
            print(f"    {od[0]} → {od[1]}: {' → '.join(path)}")
