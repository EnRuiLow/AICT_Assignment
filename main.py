"""
Main Entry Point for Logical Inference System

This is the main script to run the MRT Logical Inference component.
It demonstrates all features including rule display, inference, and testing.

Usage:
    python main.py                  # Run interactive menu
    python main.py --test           # Run all test scenarios
    python main.py --display-rules  # Display all rules
    python main.py --custom         # Run custom validation

Author: [Your Name]
Student ID: [Your ID]
"""

import sys
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
    print("\n" + "#"*70)
    print("#" + " "*68 + "#")
    print("#" + "  ChangiLink AI - Logical Inference Component".center(68) + "#")
    print("#" + "  MRT Service Advisory Consistency Validation".center(68) + "#")
    print("#" + " "*68 + "#")
    print("#"*70 + "\n")


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
        print("\n" + "="*70)
        print("TEST SCENARIOS OPTIONS")
        print("="*70)
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
    
    print("\n" + "="*70)
    print("CUSTOM VALIDATION")
    print("="*70)
    
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
    
    print("\n" + "="*70)
    print("VALIDATION RESULT")
    print("="*70)
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
        print("\n" + "="*70)
        print("MAIN MENU")
        print("="*70)
        print("1. Run test scenarios")
        print("2. Display rules")
        print("3. Custom validation")
        print("4. Display knowledge base summary")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            run_test_scenarios_interactive()
        elif choice == "2":
            display_rules_interactive()
        elif choice == "3":
            custom_validation()
        elif choice == "4":
            kb = MRTKnowledgeBase()
            kb.display_summary()
            kb.display_rules()
        elif choice == "5":
            print("\nThank you for using ChangiLink AI Logical Inference!")
            print("="*70 + "\n")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1-5.")


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
