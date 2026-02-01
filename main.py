"""
ChangiLink AI - Integrated Console Application

This is the main integrated console application that combines three AI components:
1. Route Planning with Search Algorithms (BFS, DFS, Greedy BFS, A*)
2. Logical Inference Engine (Resolution-based reasoning)
3. Bayesian Network (Crowding Risk Prediction)

Usage:
    python main.py                  # Run interactive menu

Author: [Your Name]
Student ID: [Your ID]
"""

import sys
import os

# Add directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'route_planning'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bayesian_network'))

from logical_inference import (
    MRTKnowledgeBase,
    ResolutionEngine,
    NetworkMode,
    Proposition
)
from logical_inference.test_scenarios import (
    run_all_scenarios, 
    run_today_scenarios, 
    run_future_scenarios
)


def display_welcome():
    """Display welcome banner"""
    print("\n" + "="*80)
    print("=" + " "*78 + "=")
    print("=" + "  ✈  CHANGILINK AI - INTEGRATED SYSTEM  ✈".center(78) + "=")
    print("=" + "  Changi Airport Terminal 5 MRT Routing & Advisory System".center(78) + "=")
    print("=" + " "*78 + "=")
    print("="*80)
    print()
    print("  This system integrates three AI components:")
    print("    1. Route Planning with Search Algorithms")
    print("    2. Logical Inference Engine")
    print("    3. Bayesian Network for Crowding Risk Prediction")
    print()
    print("="*80 + "\n")


def display_rules_interactive():
    """Interactive rule display"""
    kb = MRTKnowledgeBase()
    
    while True:
        print("\n" + "="*80)
        print("  LOGICAL INFERENCE - RULE DISPLAY")
        print("="*80)
        print("1. Display all rules")
        print("2. Display TODAY mode rules only")
        print("3. Display FUTURE mode rules only")
        print("4. Display specific rule by ID")
        print("5. Back to main menu")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            kb.display_rules()
        elif choice == "2":
            kb.display_rules(NetworkMode.TODAY)
        elif choice == "3":
            kb.display_rules(NetworkMode.FUTURE)
        elif choice == "4":
            rule_id = input("Enter rule ID (e.g., R1): ").strip()
            rule = kb.get_rule_by_id(rule_id)
            if rule:
                print(f"\n{rule.rule_id}: {rule.description}")
                print(f"Formal: {repr(rule)}")
                print(f"CNF: {rule.to_cnf()[0]}")
            else:
                print(f"Rule {rule_id} not found")
        elif choice == "5":
            break
        else:
            print("Invalid choice")

# ============================================================================
# LOGICAL INFERENCE SUBMENU
# ============================================================================

def logical_inference_menu():
    """Interactive logical inference menu"""
    while True:
        print("\n" + "="*80)
        print("  LOGICAL INFERENCE")
        print("="*80)
        print("1. Display Knowledge Base Rules")
        print("2. Run Test Scenarios")
        print("3. Custom Route Validation")
        print("4. Display Knowledge Base Summary")
        print("5. Back to Main Menu")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            display_rules_interactive()
        elif choice == "2":
            run_test_scenarios_interactive()
        elif choice == "3":
            custom_validation()
        elif choice == "4":
            kb = MRTKnowledgeBase()
            kb.display_summary()
        elif choice == "5":
            break
        else:
            print("Invalid choice")


# ============================================================================
# ROUTE PLANNING MODULE
# ============================================================================

def route_planning_menu():
    """Interactive route planning menu"""
    # Import route planning functions
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "route_planning", 
            os.path.join(os.path.dirname(__file__), "route_planning", "Route Planning with Search Algorithms.py")
        )
        rp = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rp)
    except Exception as e:
        print(f"Error loading route planning module: {e}")
        return
    
    while True:
        print("\n" + "="*80)
        print("  ROUTE PLANNING WITH SEARCH ALGORITHMS")
        print("="*80)
        print("1. Find route using BFS (Breadth-First Search)")
        print("2. Find route using DFS (Depth-First Search)")
        print("3. Find route using Greedy Best-First Search")
        print("4. Find route using A* Algorithm")
        print("5. Compare all algorithms")
        print("6. Compare Today vs Future network modes")
        print("7. View available stations")
        print("8. Back to main menu")
        
        choice = input("\nEnter choice (1-8): ").strip()
        
        if choice == "8":
            break
        elif choice == "7":
            print("\n" + "-"*80)
            print("AVAILABLE STATIONS:")
            print("-"*80)
            for i, station in enumerate(sorted(rp.stations.keys()), 1):
                line = rp.station_line.get(station, "Unknown")
                print(f"{i:2d}. {station:25s} [{line}]")
            continue
        
        if choice in ["1", "2", "3", "4", "5"]:
            start = input("\nEnter start station: ").strip()
            goal = input("Enter destination station: ").strip()
            
            if start not in rp.stations:
                print(f"Error: '{start}' not found in station list")
                continue
            if goal not in rp.stations:
                print(f"Error: '{goal}' not found in station list")
                continue
            
            print(f"\nSearching route from '{start}' to '{goal}'...\n")
            
            if choice == "1":
                path, nodes = rp.bfs(rp.graph_today, start, goal)
                print_route_result("BFS", path, nodes, rp, start, goal)
            
            elif choice == "2":
                path, nodes = rp.dfs(rp.graph_today, start, goal)
                print_route_result("DFS", path, nodes, rp, start, goal)
            
            elif choice == "3":
                path, nodes = rp.greedy_bfs(rp.graph_today, start, goal)
                print_route_result("Greedy Best-First Search", path, nodes, rp, start, goal)
            
            elif choice == "4":
                path, cost = rp.astar(rp.graph_today, start, goal, rp.station_line)
                print("\n" + "="*80)
                print(f"  A* ALGORITHM RESULTS")
                print("="*80)
                if path:
                    print(f"✓ Route found!")
                    print(f"\nPath: {' → '.join(path)}")
                    print(f"Total Cost: {cost:.2f}")
                    print(f"Number of Stations: {len(path)}")
                    transfers = rp.count_transfers(path, rp.station_line)
                    print(f"Number of Transfers: {transfers}")
                else:
                    print("✗ No route found")
            
            elif choice == "5":
                print("\n" + "="*80)
                print(f"  COMPARING ALL ALGORITHMS")
                print("="*80)
                algorithms = [
                    ("BFS", lambda: rp.bfs(rp.graph_today, start, goal)),
                    ("DFS", lambda: rp.dfs(rp.graph_today, start, goal)),
                    ("Greedy BFS", lambda: rp.greedy_bfs(rp.graph_today, start, goal)),
                    ("A*", lambda: rp.astar(rp.graph_today, start, goal, rp.station_line))
                ]
                
                for name, algo_func in algorithms:
                    result = rp.run_algorithm(algo_func, rp.graph_today, start, goal, rp.station_line if name == "A*" else None)
                    print(f"\n{name}:")
                    print(f"  Path: {' → '.join(result['path']) if result['path'] else 'Not found'}")
                    if result['path']:
                        print(f"  Stations: {len(result['path'])}")
                        print(f"  Nodes Explored: {result.get('nodes_explored', 'N/A')}")
                        if 'cost' in result:
                            print(f"  Cost: {result['cost']:.2f}")
        
        elif choice == "6":
            print("\n" + "="*80)
            print("  TODAY vs FUTURE MODE COMPARISON")
            print("="*80)
            print("\nSample origin-destination pairs will be compared...")
            
            od_pairs = [
                ("Changi Airport", "Marina Bay"),
                ("Expo", "City Hall"),
                ("Tampines", "Gardens by the Bay")
            ]
            
            rp.compare_today_future(rp.graph_today, rp.station_line, 
                                   rp.future_graph_today, rp.future_station_line, 
                                   od_pairs)


def print_route_result(algorithm_name, path, nodes_explored, rp, start, goal):
    """Helper function to print route results"""
    print("\n" + "="*80)
    print(f"  {algorithm_name.upper()} RESULTS")
    print("="*80)
    if path:
        print(f"✓ Route found!")
        print(f"\nPath: {' → '.join(path)}")
        print(f"Number of Stations: {len(path)}")
        print(f"Nodes Explored: {nodes_explored}")
        cost = rp.path_cost_with_transfer(path, rp.graph_today, rp.station_line)
        print(f"Estimated Cost: {cost:.2f}")
        transfers = rp.count_transfers(path, rp.station_line)
        print(f"Number of Transfers: {transfers}")
    else:
        print("✗ No route found")


# ============================================================================
# BAYESIAN NETWORK MODULE
# ============================================================================

def bayesian_network_menu():
    """Interactive Bayesian Network menu"""
    try:
        from bayesian_network import CrowdingRiskBN
    except Exception as e:
        print(f"Error loading Bayesian Network module: {e}")
        return
    
    bn = CrowdingRiskBN()
    
    while True:
        print("\n" + "="*80)
        print("  BAYESIAN NETWORK - CROWDING RISK PREDICTION")
        print("="*80)
        print("1. Interactive crowding prediction")
        print("2. Compare Today vs Future mode")
        print("3. Scenario analysis (weather impact)")
        print("4. Scenario analysis (time of day impact)")
        print("5. View network structure")
        print("6. Back to main menu")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "6":
            break
        elif choice == "1":
            interactive_crowding_query(bn)
        elif choice == "2":
            compare_modes_bn(bn)
        elif choice == "3":
            analyze_weather_impact(bn)
        elif choice == "4":
            analyze_time_impact(bn)
        elif choice == "5":
            print("\n" + "-"*80)
            print("BAYESIAN NETWORK STRUCTURE:")
            print("-"*80)
            print("\nVariables:")
            print("  • Weather (W): Clear, Rainy, Thunderstorms")
            print("  • Time of Day (T): Morning, Afternoon, Evening")
            print("  • Day Type (D): Weekday, Weekend")
            print("  • Network Mode (M): Today, Future")
            print("  • Service Status (S): Normal, Reduced, Disrupted")
            print("  • Demand Proxy (P): Low, Medium, High")
            print("  • Crowding Risk (C): Low, Medium, High")
            print("\nDependencies:")
            print("  • Weather → Service Status")
            print("  • Weather → Demand Proxy")
            print("  • Time of Day → Demand Proxy")
            print("  • Day Type → Demand Proxy")
            print("  • Network Mode → Demand Proxy")
            print("  • Network Mode → Crowding Risk")
            print("  • Service Status → Crowding Risk")
            print("  • Demand Proxy → Crowding Risk")


def interactive_crowding_query(bn):
    """Run interactive crowding risk query"""
    print("\n" + "-"*80)
    print("INTERACTIVE CROWDING RISK PREDICTION")
    print("-"*80)
    print("\nEnter conditions (press Enter to skip any field):\n")
    
    weather = input("Weather (Clear/Rainy/Thunderstorms): ").strip()
    if weather and weather not in ['Clear', 'Rainy', 'Thunderstorms']:
        print(f"Invalid weather. Using default.")
        weather = None
    
    time_of_day = input("Time of Day (Morning/Afternoon/Evening): ").strip()
    if time_of_day and time_of_day not in ['Morning', 'Afternoon', 'Evening']:
        print(f"Invalid time. Using default.")
        time_of_day = None
    
    day_type = input("Day Type (Weekday/Weekend): ").strip()
    if day_type and day_type not in ['Weekday', 'Weekend']:
        print(f"Invalid day type. Using default.")
        day_type = None
    
    network_mode = input("Network Mode (Today/Future): ").strip()
    if network_mode and network_mode not in ['Today', 'Future']:
        print(f"Invalid network mode. Using default.")
        network_mode = None
    
    service_status = input("Service Status (Normal/Reduced/Disrupted): ").strip()
    if service_status and service_status not in ['Normal', 'Reduced', 'Disrupted']:
        print(f"Invalid service status. Using default.")
        service_status = None
    
    # Perform prediction
    print("\n" + "-"*80)
    print("PREDICTION RESULTS")
    print("-"*80)
    
    result = bn.predict_crowding(
        weather=weather if weather else None,
        time_of_day=time_of_day if time_of_day else None,
        day_type=day_type if day_type else None,
        network_mode=network_mode if network_mode else None,
        service_status=service_status if service_status else None
    )
    
    # Extract and display probabilities
    values = result.values
    states = result.state_names['Crowding_Risk']
    probs = {state: float(prob) for state, prob in zip(states, values)}
    
    print("\nCrowding Risk Probability Distribution:")
    for state in ['Low', 'Medium', 'High']:
        prob = probs[state]
        bar = '█' * int(prob * 50)
        print(f"  {state:8s}: {prob:6.2%} {bar}")
    
    max_state = max(probs, key=probs.get)
    print(f"\n→ Most Likely Crowding Risk: {max_state} ({probs[max_state]:.2%})")
    
    # Recommendations
    print("\nRecommendations:")
    if probs['High'] > 0.5:
        print("  ⚠ HIGH CROWDING RISK - Consider alternative routes or timing")
        print("    • Use less crowded stations for interchange")
        print("    • Travel during off-peak hours if possible")
    elif probs['Medium'] > 0.5:
        print("  ⚠ MODERATE CROWDING - Plan for potential delays")
        print("    • Allow extra travel time")
        print("    • Stay alert for service announcements")
    else:
        print("  ✓ LOW CROWDING RISK - Normal travel conditions expected")


def compare_modes_bn(bn):
    """Compare Today vs Future mode"""
    print("\n" + "-"*80)
    print("TODAY vs FUTURE MODE COMPARISON")
    print("-"*80)
    print("\nConditions: Morning, Weekday, Clear weather, Normal service\n")
    
    # Today mode
    result_today = bn.predict_crowding(
        weather='Clear',
        time_of_day='Morning',
        day_type='Weekday',
        network_mode='Today',
        service_status='Normal'
    )
    
    # Future mode
    result_future = bn.predict_crowding(
        weather='Clear',
        time_of_day='Morning',
        day_type='Weekday',
        network_mode='Future',
        service_status='Normal'
    )
    
    states = result_today.state_names['Crowding_Risk']
    probs_today = {state: float(prob) for state, prob in zip(states, result_today.values)}
    probs_future = {state: float(prob) for state, prob in zip(states, result_future.values)}
    
    print("TODAY MODE:")
    for state in ['Low', 'Medium', 'High']:
        prob = probs_today[state]
        bar = '█' * int(prob * 40)
        print(f"  {state:8s}: {prob:6.2%} {bar}")
    
    print("\nFUTURE MODE (with TELe/CRL):")
    for state in ['Low', 'Medium', 'High']:
        prob = probs_future[state]
        bar = '█' * int(prob * 40)
        print(f"  {state:8s}: {prob:6.2%} {bar}")
    
    print("\nIMPROVEMENT:")
    print(f"  High Risk: {probs_today['High']:.2%} → {probs_future['High']:.2%} "
          f"({probs_future['High'] - probs_today['High']:+.2%})")


def analyze_weather_impact(bn):
    """Analyze weather impact on crowding"""
    print("\n" + "-"*80)
    print("WEATHER IMPACT ANALYSIS")
    print("-"*80)
    print("\nConditions: Morning, Weekday, Today mode, Normal service\n")
    
    weather_conditions = ['Clear', 'Rainy', 'Thunderstorms']
    
    for weather in weather_conditions:
        result = bn.predict_crowding(
            weather=weather,
            time_of_day='Morning',
            day_type='Weekday',
            network_mode='Today',
            service_status='Normal'
        )
        
        states = result.state_names['Crowding_Risk']
        probs = {state: float(prob) for state, prob in zip(states, result.values)}
        
        print(f"{weather.upper()}:")
        for state in ['Low', 'Medium', 'High']:
            prob = probs[state]
            bar = '█' * int(prob * 40)
            print(f"  {state:8s}: {prob:6.2%} {bar}")
        print()


def analyze_time_impact(bn):
    """Analyze time of day impact"""
    print("\n" + "-"*80)
    print("TIME OF DAY IMPACT ANALYSIS")
    print("-"*80)
    print("\nConditions: Clear weather, Weekday, Today mode, Normal service\n")
    
    times = ['Morning', 'Afternoon', 'Evening']
    
    for time_of_day in times:
        result = bn.predict_crowding(
            weather='Clear',
            time_of_day=time_of_day,
            day_type='Weekday',
            network_mode='Today',
            service_status='Normal'
        )
        
        states = result.state_names['Crowding_Risk']
        probs = {state: float(prob) for state, prob in zip(states, result.values)}
        
        print(f"{time_of_day.upper()}:")
        for state in ['Low', 'Medium', 'High']:
            prob = probs[state]
            bar = '█' * int(prob * 40)
            print(f"  {state:8s}: {prob:6.2%} {bar}")
        print()


# ============================================================================
# LOGICAL INFERENCE MODULE (continued)
# ============================================================================

def display_rules_interactive():
    """Interactive rule display"""
    kb = MRTKnowledgeBase()
    
    while True:
        print("\n" + "="*70)
        print("RULE DISPLAY OPTIONS")
        print("="*70)
        print("1. Display all rules")
        print("2. Display TODAY mode rules only")
        print("3. Display FUTURE mode rules only")
        print("4. Display specific rule by ID")
        print("5. Back to main menu")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            kb.display_rules()
        elif choice == "2":
            kb.display_rules(NetworkMode.TODAY)
        elif choice == "3":
            kb.display_rules(NetworkMode.FUTURE)
        elif choice == "4":
            rule_id = input("Enter rule ID (e.g., R1): ").strip()
            rule = kb.get_rule_by_id(rule_id)
            if rule:
                print(f"\n{rule.rule_id}: {rule.description}")
                print(f"Formal: {repr(rule)}")
                print(f"CNF: {rule.to_cnf()[0]}")
            else:
                print(f"Rule {rule_id} not found")
        elif choice == "5":
            break
        else:
            print("Invalid choice")


def run_test_scenarios_interactive():
    """Interactive test scenario runner with submenu"""
    while True:
        print("\n" + "="*80)
        print("  LOGICAL INFERENCE - TEST SCENARIOS")
        print("="*80)
        print("1. Run all test scenarios")
        print("2. Run TODAY mode scenarios only")
        print("3. Run FUTURE mode scenarios only")
        print("4. Back to main menu")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            run_all_scenarios()
        elif choice == "2":
            run_today_scenarios()
        elif choice == "3":
            run_future_scenarios()
        elif choice == "4":
            break
        else:
            print("Invalid choice")


def custom_validation():
    """Interactive custom validation"""
    kb = MRTKnowledgeBase()
    engine = ResolutionEngine(kb)
    
    print("\n" + "="*80)
    print("  LOGICAL INFERENCE - CUSTOM VALIDATION")
    print("="*80)
    
    # Select mode
    print("\nSelect Network Mode:")
    print("1. TODAY (Current EWL airport branch)")
    print("2. FUTURE (TELe/CRL extensions)")
    mode_choice = input("Enter choice (1-2): ").strip()
    
    if mode_choice == "1":
        mode = NetworkMode.TODAY
    elif mode_choice == "2":
        mode = NetworkMode.FUTURE
    else:
        print("Invalid choice")
        return
    
    print(f"\nMode selected: {mode.value.upper()}")
    
    # Enter facts
    print("\nEnter facts (proposition_name=true/false)")
    print("Example: Station_Open_Expo=true")
    print("Enter 'done' when finished")
    
    facts = {}
    while True:
        fact_input = input("Fact: ").strip()
        
        if fact_input.lower() == "done":
            break
        
        try:
            prop_name, value_str = fact_input.split("=")
            value = value_str.lower() == "true"
            facts[prop_name.strip()] = value
            print(f"  Added: {prop_name.strip()} = {value}")
        except:
            print("  Invalid format. Use: proposition_name=true/false")
    
    # Validate
    print("\nValidating...")
    result = engine.validate_route(facts, mode)
    
    print("\n" + "="*80)
    print("  VALIDATION RESULT")
    print("="*80)
    print(f"\nMode: {result['mode'].upper()}")
    print(f"\nFacts:")
    for fact, value in result['facts'].items():
        print(f"  • {fact}: {value}")
    
    if result['is_consistent']:
        print(f"\n✓ VALID - Route is consistent with all rules")
    else:
        print(f"\n✗ INVALID - Contradictions detected")
    
    print(f"\nDetails: {result['consistency_message']}")
    
    if result['violated_rules']:
        print(f"\nViolated Rules:")
        for violation in result['violated_rules']:
            print(f"  • {violation}")


def main_menu():
    """Main interactive menu"""
    while True:
        print("\n" + "="*80)
        print("  CHANGILINK AI - MAIN MENU")
        print("="*80)
        print()
        print("  1. Route Planning")
        print("  2. Logical Inference")
        print("  3. Bayesian Network")
        print("  4. Exit")
        print()
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            route_planning_menu()
        elif choice == "2":
            logical_inference_menu()
        elif choice == "3":
            bayesian_network_menu()
        elif choice == "4":
            print("\n" + "="*80)
            print("  Thank you for using ChangiLink AI Integrated System!")
            print("="*80 + "\n")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1-4.")


def display_about():
    """Display information about the system"""
    print("\n" + "="*80)
    print("  ABOUT CHANGILINK AI INTEGRATED SYSTEM")
    print("="*80)
    print()
    print("This integrated system combines three AI components for the Changi Airport")
    print("Terminal 5 MRT routing and advisory system:")
    print()
    print("1. ROUTE PLANNING WITH SEARCH ALGORITHMS")
    print("   • Implements BFS, DFS, Greedy Best-First Search, and A* algorithms")
    print("   • Finds optimal paths between MRT stations")
    print("   • Compares Today vs Future network modes")
    print("   • Considers transfer penalties and line changes")
    print()
    print("2. LOGICAL INFERENCE ENGINE")
    print("   • Resolution-based theorem proving")
    print("   • Validates service advisory consistency")
    print("   • Checks route validity against operational rules")
    print("   • Identifies rule violations")
    print()
    print("3. BAYESIAN NETWORK FOR CROWDING RISK PREDICTION")
    print("   • Predicts crowding risk at MRT stations")
    print("   • Considers weather, time, service status, and network mode")
    print("   • Provides probability distributions and recommendations")
    print("   • Compares Today vs Future mode scenarios")
    print()
    print("Developed for: AICT Assignment")
    print("System Version: 1.0")
    print("Date: February 2026")
    print("="*80)


def main():
    """Main entry point"""
    display_welcome()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg == "--help" or arg == "-h":
            print("Usage:")
            print("  python main.py                  # Interactive menu")
            print("  python main.py --test           # Run all test scenarios")
            print("  python main.py --test-today     # Run TODAY mode scenarios")
            print("  python main.py --test-future    # Run FUTURE mode scenarios")
            print("  python main.py --display-rules  # Display all rules")
            print("  python main.py --custom         # Custom validation")
            sys.exit(0)
        
        elif arg == "--test":
            run_all_scenarios()
            sys.exit(0)
        
        elif arg == "--test-today":
            run_today_scenarios()
            sys.exit(0)
        
        elif arg == "--test-future":
            run_future_scenarios()
            sys.exit(0)
        
        elif arg == "--display-rules":
            kb = MRTKnowledgeBase()
            kb.display_rules()
            sys.exit(0)
        
        elif arg == "--custom":
            custom_validation()
            sys.exit(0)
        
        else:
            print(f"Unknown argument: {arg}")
            print("Use --help for usage information")
            sys.exit(1)
    
    # No arguments - run interactive menu
    main_menu()


if __name__ == "__main__":
    main()
