"""
Test Scenarios for Logical Inference

This module contains 9 test scenarios covering:
- Valid routes (both modes)
- Invalid routes (rule violations)
- Contradictory advisories

Author: [Your Name]
Student ID: [Your ID]
"""

from .models import NetworkMode
from .knowledge_base import MRTKnowledgeBase
from .inference_engine import ResolutionEngine


def print_scenario_header(scenario_num: int, title: str):
    """Print formatted scenario header"""
    print("\n" + "="*70)
    print(f"SCENARIO {scenario_num}: {title}")
    print("="*70)


def print_result(result: dict):
    """Print validation result in formatted way"""
    print(f"\nMode: {result['mode'].upper()}")
    print(f"\nInput Facts:")
    for fact, value in result['facts'].items():
        print(f"  • {fact}: {value}")
    
    print(f"\nValidation Result:")
    if result['is_consistent']:
        print("  ✓ VALID - No contradictions detected")
    else:
        print("  ✗ INVALID - Contradictions detected")
    
    print(f"\nDetails:")
    print(f"  {result['consistency_message']}")
    
    if result['violated_rules']:
        print(f"\nViolated Rules:")
        for violation in result['violated_rules']:
            print(f"  • {violation}")


# ============================================================================
# SCENARIO 1: VALID - Normal Operations in TODAY Mode
# ============================================================================

def scenario_1_valid_today():
    """
    Scenario 1: Valid route in TODAY Mode
    
    Context: Normal weekday operations, all stations open, standard service
    Expected: All rules satisfied, no contradictions
    """
    print_scenario_header(1, "VALID - Normal Operations (TODAY Mode)")
    
    kb = MRTKnowledgeBase()
    engine = ResolutionEngine(kb)
    
    facts = {
        "Network_Mode_Today": True,
        "Station_Open_TanahMerah": True,
        "Station_Open_Expo": True,
        "Station_Open_Changi_Airport": True,
        "Line_Active_TEL": True,
        "Line_Active_EWL_Airport": True,
        "Service_Status_Normal_TEL": True,
        "Network_Operational": True,
    }
    
    result = engine.validate_route(facts, NetworkMode.TODAY)
    print_result(result)
    
    return result


# ============================================================================
# SCENARIO 2: INVALID - Using Old EWL Branch in FUTURE Mode
# ============================================================================

def scenario_2_invalid_future_ewl():
    """
    Scenario 2: Invalid route - Using old EWL airport branch in FUTURE Mode
    
    Context: Future network with TELe/CRL, but trying to use old EWL to airport
    Expected: Violation of R3 (old EWL branch not active in Future Mode)
    """
    print_scenario_header(2, "INVALID - Old EWL Airport Branch in FUTURE Mode")
    
    kb = MRTKnowledgeBase()
    engine = ResolutionEngine(kb)
    
    facts = {
        "Network_Mode_Future": True,
        "Line_Inactive_EWL_Airport": False,  # Trying to say it IS active (violates R3)
        "Line_Active_TEL": True,
        "Destination_Changi_Airport": True,
        "Network_Operational": True,
    }
    
    result = engine.validate_route(facts, NetworkMode.FUTURE)
    print_result(result)
    
    return result


# ============================================================================
# SCENARIO 3: CONTRADICTION - Station Open AND Under Integration
# ============================================================================

def scenario_3_contradiction_integration():
    """
    Scenario 3: Contradictory advisories
    
    Context: Advisory states Expo is open, but also undergoing integration work
    Expected: Contradiction detected (R2: Integration work → Station closed)
    """
    print_scenario_header(3, "CONTRADICTION - Station Open AND Integration Work")
    
    kb = MRTKnowledgeBase()
    engine = ResolutionEngine(kb)
    
    facts = {
        "Network_Mode_Today": True,
        "Integration_Work_Expo": True,  # Expo undergoing integration
        "Station_Closed_Expo": False,  # But advisory says it's NOT closed (contradiction)
    }
    
    result = engine.validate_route(facts, NetworkMode.TODAY)
    print_result(result)
    
    return result


# ============================================================================
# SCENARIO 4: VALID - FUTURE Mode with TEL to T5
# ============================================================================

def scenario_4_valid_future_t5():
    """
    Scenario 4: Valid route in FUTURE Mode to T5
    
    Context: Future network operational, routing to new T5 station via TEL
    Expected: All rules satisfied (R4, R12 validated)
    """
    print_scenario_header(4, "VALID - FUTURE Mode Route to T5")
    
    kb = MRTKnowledgeBase()
    engine = ResolutionEngine(kb)
    
    facts = {
        "Network_Mode_Future": True,
        "Network_Operational": True,
        "Line_Active_TEL_T5": True,  # TEL extension to T5
        "Line_Active_CRL_T5": True,  # CRL extension to T5
        "Station_Open_T5": True,
        "Route_Uses_T5": True,
        "Line_Active_TEL": True,
        "Line_Active_CRL": True,
        "Transfer_Available_TEL_CRL": True,  # R9 should be satisfied
    }
    
    result = engine.validate_route(facts, NetworkMode.FUTURE)
    print_result(result)
    
    return result


# ============================================================================
# SCENARIO 5: INVALID - Using T5 in TODAY Mode (FIXED)
# ============================================================================

def scenario_5_invalid_t5_today():
    """
    Scenario 5: Invalid - Trying to route to T5 in TODAY Mode
    
    Context: TODAY mode but route uses T5 (which doesn't exist yet)
    Expected: Violation of R12 and R13 (T5 requires Future Mode, but we're in Today Mode)
    """
    print_scenario_header(5, "INVALID - Using T5 Station in TODAY Mode")
    
    kb = MRTKnowledgeBase()
    engine = ResolutionEngine(kb)
    
    facts = {
        "Network_Mode_Today": True,
        "Route_Uses_T5": True,  # This triggers R12: Route_Uses_T5 → Network_Mode_Future
        "Network_Mode_Not_Future": True,  # R13 consequence: Today → Not Future
        # R12 infers Network_Mode_Future
        # R13 infers Network_Mode_Not_Future  
        # These contradict!
    }
    
    result = engine.validate_route(facts, NetworkMode.TODAY)
    print_result(result)
    
    return result


# ============================================================================
# SCENARIO 6: VALID - Reduced Service with Crowding Risk
# ============================================================================

def scenario_6_valid_crowding():
    """
    Scenario 6: Valid but crowded - Reduced service during peak hour
    
    Context: TEL has reduced service during peak hour
    Expected: Valid route but high crowding risk (R8)
    """
    print_scenario_header(6, "VALID - Reduced Service with High Crowding Risk")
    
    kb = MRTKnowledgeBase()
    engine = ResolutionEngine(kb)
    
    facts = {
        "Network_Mode_Today": True,
        "Service_Status_Reduced_TEL": True,
        "Time_Peak": True,
        "Crowding_Risk_High": True,  # R8 consequence
        "Integration_Work_Active": True,
        "Service_Adjustments_Required": True,  # R10 consequence
    }
    
    result = engine.validate_route(facts, NetworkMode.TODAY)
    print_result(result)
    
    return result


# ============================================================================
# SCENARIO 7: VALID - Multiple Station Closures
# ============================================================================

def scenario_7_multiple_closures():
    """
    Scenario 7: Multiple simultaneous station closures
    
    Context: Both Expo and Tanah Merah closed due to maintenance
    Expected: Valid scenario, but no TEL-EWL transfer available
    Tests: Cascading effects of multiple closures
    """
    print_scenario_header(7, "VALID - Multiple Station Closures")
    
    kb = MRTKnowledgeBase()
    engine = ResolutionEngine(kb)
    
    facts = {
        "Network_Mode_Today": True,
        "Station_Closed_Expo": True,
        "Station_Closed_TanahMerah": True,  # Both major interchange stations closed
        "Integration_Work_Expo": True,      # Reason for Expo closure
        "Line_Active_TEL": True,
        "Line_Active_EWL_Airport": True,
        "Transfer_Unavailable_Expo": True,  # R6 consequence
        "Transfer_Unavailable_TEL_EWL": True,  # R15 consequence
    }
    
    result = engine.validate_route(facts, NetworkMode.TODAY)
    print_result(result)
    
    return result


# ============================================================================
# SCENARIO 8: VALID - Complete Future Mode Setup
# ============================================================================

def scenario_8_future_mode_complete():
    """
    Scenario 8: Complete Future Mode network configuration
    
    Context: Future network fully operational with all extensions
    Expected: Valid - all Future Mode requirements met
    Tests: Comprehensive Future Mode validation
    """
    print_scenario_header(8, "VALID - Complete FUTURE Mode Configuration")
    
    kb = MRTKnowledgeBase()
    engine = ResolutionEngine(kb)
    
    facts = {
        "Network_Mode_Future": True,
        "Network_Mode_Not_Today": True,  # R14 consequence
        "Network_Operational": True,
        "Line_Active_TEL_T5": True,  # R4 consequence
        "Line_Active_CRL_T5": True,
        "Line_Inactive_EWL_Airport": True,  # R3 consequence
        "Station_Open_T5": True,
        "Line_Active_TEL": True,
        "Line_Active_CRL": True,
        "Transfer_Available_TEL_CRL": True,  # R9 consequence
        "Destination_Changi_Airport": True,
        "Route_Uses_TEL": True,  # R11 consequence
    }
    
    result = engine.validate_route(facts, NetworkMode.FUTURE)
    print_result(result)
    
    return result


# ============================================================================
# SCENARIO 9: VALID - Peak Hour Complex Scenario
# ============================================================================

def scenario_9_peak_hour_complex():
    """
    Scenario 9: Peak hour with multiple concurrent issues
    
    Context: Peak hour + reduced service + integration work
    Expected: Valid but with high crowding risk
    Tests: Multiple rules triggering simultaneously
    """
    print_scenario_header(9, "VALID - Peak Hour Multiple Service Issues")
    
    kb = MRTKnowledgeBase()
    engine = ResolutionEngine(kb)
    
    facts = {
        "Network_Mode_Today": True,
        "Time_Peak": True,
        "Service_Status_Reduced_TEL": True,
        "Integration_Work_Active": True,
        "Crowding_Risk_High": True,  # R8 consequence
        "Service_Adjustments_Required": True,  # R10 consequence
        "Network_Operational": True,
    }
    
    result = engine.validate_route(facts, NetworkMode.TODAY)
    print_result(result)
    
    return result


# ============================================================================
# COMPARISON SCENARIOS: TODAY vs FUTURE Mode
# ============================================================================

def comparison_scenario_changi_airport():
    """
    Comparison: Routing to Changi Airport in TODAY vs FUTURE Mode
    
    Tests how the same destination works differently in different modes
    """
    print("\n" + "="*70)
    print("COMPARISON: Changi Airport Route - TODAY vs FUTURE Mode")
    print("="*70)
    
    kb = MRTKnowledgeBase()
    
    # TODAY Mode
    print("\n--- TODAY MODE ---")
    engine_today = ResolutionEngine(kb)
    facts_today = {
        "Network_Mode_Today": True,
        "Destination_Changi_Airport": True,
        "Line_Active_EWL_Airport": True,  # Use old EWL branch
        "Station_Open_Changi_Airport": True,
    }
    result_today = engine_today.validate_route(facts_today, NetworkMode.TODAY)
    print(f"Result: {'✓ VALID' if result_today['is_consistent'] else '✗ INVALID'}")
    
    # FUTURE Mode
    print("\n--- FUTURE MODE ---")
    engine_future = ResolutionEngine(kb)
    facts_future = {
        "Network_Mode_Future": True,
        "Destination_Changi_Airport": True,
        "Route_Uses_TEL": True,  # Must use TEL (R11)
        "Line_Inactive_EWL_Airport": True,  # Old EWL not active (R3)
        "Station_Open_Changi_Airport": True,
    }
    result_future = engine_future.validate_route(facts_future, NetworkMode.FUTURE)
    print(f"Result: {'✓ VALID' if result_future['is_consistent'] else '✗ INVALID'}")
    
    print("\nAnalysis:")
    print("  • TODAY Mode: Uses EWL airport branch")
    print("  • FUTURE Mode: Must use TEL (old EWL branch converted)")
    print("  • This demonstrates the network transformation impact")


# ============================================================================
# HELPER FUNCTIONS FOR SCENARIO FILTERING
# ============================================================================

def run_today_scenarios():
    """Run only TODAY mode scenarios"""
    print("\n" + "#"*70)
    print("# TODAY MODE TEST SCENARIOS")
    print("#"*70)
    
    results = []
    results.append(scenario_1_valid_today())
    results.append(scenario_3_contradiction_integration())
    results.append(scenario_5_invalid_t5_today())
    results.append(scenario_6_valid_crowding())
    results.append(scenario_7_multiple_closures())
    results.append(scenario_9_peak_hour_complex())
    
    print("\n" + "="*70)
    print(f"TODAY MODE SCENARIOS COMPLETED: {len(results)} scenarios")
    print("="*70)
    
    return results


def run_future_scenarios():
    """Run only FUTURE mode scenarios"""
    print("\n" + "#"*70)
    print("# FUTURE MODE TEST SCENARIOS")
    print("#"*70)
    
    results = []
    results.append(scenario_2_invalid_future_ewl())
    results.append(scenario_4_valid_future_t5())
    results.append(scenario_8_future_mode_complete())
    
    print("\n" + "="*70)
    print(f"FUTURE MODE SCENARIOS COMPLETED: {len(results)} scenarios")
    print("="*70)
    
    return results


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def run_all_scenarios():
    """Run all test scenarios"""
    
    print("\n" + "#"*70)
    print("# LOGICAL INFERENCE TEST SCENARIOS")
    print("# ChangiLink AI - MRT Advisory Consistency Validation")
    print("#"*70)
    
    # Display knowledge base
    print("\n" + "="*70)
    print("KNOWLEDGE BASE OVERVIEW")
    print("="*70)
    kb = MRTKnowledgeBase()
    kb.display_summary()
    
    # Run individual scenarios
    results = []
    results.append(scenario_1_valid_today())
    results.append(scenario_2_invalid_future_ewl())
    results.append(scenario_3_contradiction_integration())
    results.append(scenario_4_valid_future_t5())
    results.append(scenario_5_invalid_t5_today())
    results.append(scenario_6_valid_crowding())
    results.append(scenario_7_multiple_closures())
    results.append(scenario_8_future_mode_complete())
    results.append(scenario_9_peak_hour_complex())
    
    # Run comparison
    comparison_scenario_changi_airport()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    valid_count = sum(1 for r in results if r['is_consistent'])
    invalid_count = len(results) - valid_count
    
    print(f"\nTotal Scenarios: {len(results)}")
    print(f"Valid Scenarios: {valid_count}")
    print(f"Invalid/Contradictory: {invalid_count}")
    
    print("\nScenario Breakdown:")
    for i, result in enumerate(results, 1):
        status = "✓ VALID" if result['is_consistent'] else "✗ INVALID"
        print(f"  Scenario {i} ({result['mode']}): {status}")
    
    print("\n" + "="*70)
    print("ALL SCENARIOS COMPLETED ✓")
    print("="*70)


if __name__ == "__main__":
    run_all_scenarios()
