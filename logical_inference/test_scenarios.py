"""
TELe-Specific Test Scenarios

This module demonstrates test cases that validate the TELe (Thomson-East Coast Line Extension)
rules in the updated knowledge base.

Author: [Your Name]
Student ID: [Your ID]
"""

from logical_inference.models import NetworkMode
from logical_inference.knowledge_base import MRTKnowledgeBase
from logical_inference.inference_engine import ResolutionEngine


def get_tele_test_scenarios():
    """
    Returns a list of test scenarios specifically for TELe rules.
    
    These scenarios test:
    - R13: Station conversion completion
    - R14: Systems integration impacts
    - R15: Future mode airport access
    - R16: Direct city-airport connection
    - R17: Signalling conversion disruptions
    - R18: Sungei Bedok to T5 routing
    - R19: Platform door modifications
    - R20: Power supply conversion
    """
    
    scenarios = []
    
    # ========================================================================
    # SCENARIO 1: TELe Conversion Complete - Valid Future Mode
    # ========================================================================
    scenarios.append({
        "id": "TELe_1",
        "description": "VALID - TELe Conversion Complete in Future Mode",
        "mode": NetworkMode.FUTURE,
        "facts": {
            "Network_Mode_Future": True,
            "TELe_Conversion_Complete": True,
            "Network_Operational": True,
            "Line_Active_TEL": True,
            "Station_Open_Changi_Airport": True,
        },
        "expected_outcome": "VALID",
        "expected_inferences": [
            "Stations_TanahMerah_Expo_Changi_TEL",  # via R13
            "Line_Active_TEL_T5",  # via R4
            "Changi_Airport_Accessible_Via_TEL_Only",  # via R15
            "Direct_TEL_City_Airport_Connection",  # via R16
        ],
        "explanation": "After TELe conversion, the three stations operate as TEL stations, "
                      "providing direct city-airport connectivity via TEL."
    })
    
    # ========================================================================
    # SCENARIO 2: Invalid EWL Airport Branch in Future Mode
    # ========================================================================
    scenarios.append({
        "id": "TELe_2",
        "description": "INVALID - Old EWL Airport Branch Active in Future Mode",
        "mode": NetworkMode.FUTURE,
        "facts": {
            "Network_Mode_Future": True,
            "Line_Active_EWL_Airport": True,  # CONTRADICTION!
            "Destination_Changi_Airport": True,
        },
        "expected_outcome": "INVALID",
        "violated_rules": ["R3", "R15"],
        "explanation": "The old EWL airport branch should NOT be active in Future Mode. "
                      "R3 states that in Future Mode, the old EWL branch is inactive. "
                      "This creates a contradiction."
    })
    
    # ========================================================================
    # SCENARIO 3: Systems Integration Work Ongoing
    # ========================================================================
    scenarios.append({
        "id": "TELe_3",
        "description": "VALID - Systems Integration Work Requiring Adjustments",
        "mode": NetworkMode.TODAY,
        "facts": {
            "Network_Mode_Today": True,
            "Systems_Integration_Active": True,
            "Station_Signalling_Conversion_Active": True,
            "Platform_Doors_Modification_Active": True,
        },
        "expected_outcome": "VALID",
        "expected_inferences": [
            "Service_Adjustments_Required",  # via R14, R17
            "Station_Reduced_Capacity",  # via R19
        ],
        "explanation": "During systems integration (signalling, PSDs), service adjustments "
                      "and reduced capacity are expected. System correctly identifies this."
    })
    
    # ========================================================================
    # SCENARIO 4: Route from Sungei Bedok to T5 (Future Mode)
    # ========================================================================
    scenarios.append({
        "id": "TELe_4",
        "description": "VALID - Direct Route from Sungei Bedok to T5",
        "mode": NetworkMode.FUTURE,
        "facts": {
            "Network_Mode_Future": True,
            "Origin_Sungei_Bedok": True,
            "Destination_T5": True,
            "TELe_Conversion_Complete": True,
            "Line_Active_TEL": True,
        },
        "expected_outcome": "VALID",
        "expected_inferences": [
            "Route_Uses_TEL_Extension",  # via R18
            "Line_Active_TEL_T5",  # via R4 (if Network_Operational)
        ],
        "explanation": "TELe creates a direct extension from Sungei Bedok to T5, "
                      "so this route should use the TEL extension without transfers."
    })
    
    # ========================================================================
    # SCENARIO 5: T5 Access Attempted in TODAY Mode
    # ========================================================================
    scenarios.append({
        "id": "TELe_5",
        "description": "INVALID - Attempting to Access T5 in TODAY Mode",
        "mode": NetworkMode.TODAY,
        "facts": {
            "Network_Mode_Today": True,
            "Route_Uses_T5": True,
            "Station_Open_T5": True,
        },
        "expected_outcome": "INVALID",
        "violated_rules": ["R12"],
        "explanation": "T5 station doesn't exist yet in TODAY mode. R12 states that "
                      "if route uses T5, network must be in Future Mode. Contradiction."
    })
    
    # ========================================================================
    # SCENARIO 6: Power Supply Conversion Impact
    # ========================================================================
    scenarios.append({
        "id": "TELe_6",
        "description": "VALID - Power Supply Conversion Requiring Alternative Routes",
        "mode": NetworkMode.TODAY,
        "facts": {
            "Network_Mode_Today": True,
            "Power_Supply_Conversion_Active": True,
            "Systems_Integration_Active": True,
        },
        "expected_outcome": "VALID",
        "expected_inferences": [
            "Alternative_Routing_Required",  # via R20
            "Service_Adjustments_Required",  # via R14
        ],
        "explanation": "Power supply conversion requires alternative routing and "
                      "service adjustments during transition period."
    })
    
    # ========================================================================
    # SCENARIO 7: Comparison - Airport Access (TODAY vs FUTURE)
    # ========================================================================
    scenarios.append({
        "id": "TELe_7a",
        "description": "COMPARISON A - Airport Access in TODAY Mode (via EWL)",
        "mode": NetworkMode.TODAY,
        "facts": {
            "Network_Mode_Today": True,
            "Destination_Changi_Airport": True,
            "Line_Active_EWL_Airport": True,
            "Station_Open_TanahMerah": True,
            "Station_Open_Expo": True,
            "Station_Open_Changi_Airport": True,
        },
        "expected_outcome": "VALID",
        "explanation": "In TODAY mode, Changi Airport is accessible via the EWL branch "
                      "(Tanah Merah → Expo → Changi Airport)."
    })
    
    scenarios.append({
        "id": "TELe_7b",
        "description": "COMPARISON B - Airport Access in FUTURE Mode (via TEL)",
        "mode": NetworkMode.FUTURE,
        "facts": {
            "Network_Mode_Future": True,
            "Destination_Changi_Airport": True,
            "TELe_Conversion_Complete": True,
            "Line_Active_TEL": True,
            "Station_Open_Changi_Airport": True,
        },
        "expected_outcome": "VALID",
        "expected_inferences": [
            "Route_Uses_TEL",  # via R11
            "Changi_Airport_Accessible_Via_TEL_Only",  # via R15
            "Direct_TEL_City_Airport_Connection",  # via R16
        ],
        "explanation": "In FUTURE mode, Changi Airport is accessible ONLY via TEL "
                      "(converted stations), providing faster direct connection."
    })
    
    # ========================================================================
    # SCENARIO 8: TEL-CRL Interchange at T5
    # ========================================================================
    scenarios.append({
        "id": "TELe_8",
        "description": "VALID - TEL-CRL Interchange at T5 (Future Mode)",
        "mode": NetworkMode.FUTURE,
        "facts": {
            "Network_Mode_Future": True,
            "Line_Active_TEL": True,
            "Line_Active_CRL": True,
            "Line_Active_CRL_T5": True,
            "Station_Open_T5": True,
            "TELe_Conversion_Complete": True,
        },
        "expected_outcome": "VALID",
        "expected_inferences": [
            "Transfer_Available_TEL_CRL",  # via R9
            "Network_Mode_Future",  # via R7 (reinforced)
        ],
        "explanation": "T5 will be a major interchange between TEL and CRL, enabling "
                      "seamless transfers between the two lines."
    })
    
    # ========================================================================
    # SCENARIO 9: Incomplete TELe in Future Mode
    # ========================================================================
    scenarios.append({
        "id": "TELe_9",
        "description": "EDGE CASE - Future Mode Declared but TELe Not Complete",
        "mode": NetworkMode.FUTURE,
        "facts": {
            "Network_Mode_Future": True,
            "TELe_Conversion_Complete": False,
            "Line_Active_TEL": True,
            "Destination_Changi_Airport": True,
        },
        "expected_outcome": "INDETERMINATE",
        "explanation": "This represents a transition state where Future Mode is active "
                      "but TELe conversion isn't complete. System behavior depends on "
                      "how transition phases are modeled."
    })
    
    # ========================================================================
    # SCENARIO 10: Multi-System Integration Work
    # ========================================================================
    scenarios.append({
        "id": "TELe_10",
        "description": "VALID - Multiple Systems Under Integration Simultaneously",
        "mode": NetworkMode.TODAY,
        "facts": {
            "Network_Mode_Today": True,
            "Systems_Integration_Active": True,
            "Station_Signalling_Conversion_Active": True,
            "Platform_Doors_Modification_Active": True,
            "Power_Supply_Conversion_Active": True,
            "Integration_Work_Active": True,
        },
        "expected_outcome": "VALID",
        "expected_inferences": [
            "Service_Adjustments_Required",  # via R10, R14, R17
            "Station_Reduced_Capacity",  # via R19
            "Alternative_Routing_Required",  # via R20
        ],
        "explanation": "During major integration work, multiple systems are affected "
                      "simultaneously, requiring comprehensive service adjustments."
    })
    
    return scenarios


def run_all_scenarios():
    """
    Run all TELe test scenarios and display results.
    
    This function:
    1. Initializes the knowledge base and inference engine
    2. Retrieves all test scenarios
    3. Executes each scenario through the engine
    4. Displays formatted results with validation status
    """
    print("\n" + "="*70)
    print("RUNNING ALL TEST SCENARIOS")
    print("="*70 + "\n")
    
    # Initialize
    kb = MRTKnowledgeBase()
    engine = ResolutionEngine(kb)
    scenarios = get_tele_test_scenarios()
    
    passed = 0
    failed = 0
    
    for scenario in scenarios:
        print(f"\n{'─'*70}")
        print(f"[{scenario['id']}] {scenario['description']}")
        print(f"Mode: {scenario['mode'].value.upper()}")
        print(f"{'─'*70}")
        
        # Display input facts
        print("\nInput Facts:")
        for fact, value in scenario['facts'].items():
            print(f"  • {fact}: {value}")
        
        # Run validation
        result = engine.validate_route(scenario['facts'], scenario['mode'])
        
        # Check result
        is_valid = result['is_consistent']
        expected = scenario['expected_outcome'] == "VALID"
        test_passed = (is_valid == expected)
        
        if test_passed:
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1
        
        print(f"\nResult: {status}")
        print(f"  Consistency: {result['is_consistent']}")
        print(f"  Expected: {scenario['expected_outcome']}")
        
        if result['consistency_message']:
            print(f"  Message: {result['consistency_message']}")
        
        if result['violated_rules']:
            print(f"  Violated Rules: {', '.join(result['violated_rules'])}")
        
        print(f"\nExplanation: {scenario['explanation']}")
    
    # Summary
    print(f"\n\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}")
    print(f"Total Scenarios: {len(scenarios)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED!")
    else:
        print(f"\n✗ {failed} TEST(S) FAILED")
    
    print(f"{'='*70}\n")


def print_tele_scenario_summary():
    """Print a summary of all TELe test scenarios"""
    scenarios = get_tele_test_scenarios()
    
    print("\n" + "="*70)
    print("TELe TEST SCENARIOS SUMMARY")
    print("="*70 + "\n")
    
    print(f"Total TELe-specific scenarios: {len(scenarios)}\n")
    
    for scenario in scenarios:
        print(f"[{scenario['id']}] {scenario['description']}")
        print(f"   Mode: {scenario['mode'].value.upper()}")
        print(f"   Expected: {scenario['expected_outcome']}")
        if 'violated_rules' in scenario:
            print(f"   Violates: {', '.join(scenario['violated_rules'])}")
        print(f"   {scenario['explanation'][:70]}...")
        print()
    
    print("="*70 + "\n")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print_tele_scenario_summary()
    
    print("\n" + "="*70)
    print("DETAILED SCENARIO EXAMPLE")
    print("="*70 + "\n")
    
    scenarios = get_tele_test_scenarios()
    example = scenarios[0]  # TELe_1
    
    print(f"Scenario ID: {example['id']}")
    print(f"Description: {example['description']}")
    print(f"Mode: {example['mode'].value}")
    print(f"\nInput Facts:")
    for fact, value in example['facts'].items():
        print(f"   • {fact}: {value}")
    
    print(f"\nExpected Outcome: {example['expected_outcome']}")
    
    if 'expected_inferences' in example:
        print(f"\nExpected Inferences:")
        for inference in example['expected_inferences']:
            print(f"   • {inference}")
    
    print(f"\nExplanation:")
    print(f"   {example['explanation']}")
    
    print("\n" + "="*70)
    print("To run these scenarios with the inference engine:")
    print("="*70)
    print("""
from knowledge_base_updated import MRTKnowledgeBase
from logical_inference import ResolutionEngine
from tele_test_scenarios import get_tele_test_scenarios

# Initialize
kb = MRTKnowledgeBase()
engine = ResolutionEngine(kb)

# Get scenarios
scenarios = get_tele_test_scenarios()

# Run each scenario
for scenario in scenarios:
    result = engine.validate_route(scenario['facts'], scenario['mode'])
    print(f"{scenario['id']}: {result['is_consistent']}")
    """)
    print("="*70 + "\n")
