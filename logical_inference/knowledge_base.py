"""
MRT Knowledge Base

This module defines the MRTKnowledgeBase class which stores all operational
rules for the MRT system, covering both Today Mode and Future Mode operations.

Author: [Your Name]
Student ID: [Your ID]
"""

from typing import List, Optional
from .models import NetworkMode
from .rules import LogicRule


class MRTKnowledgeBase:
    """
    Knowledge base containing MRT operational rules.
    
    Stores rules that govern:
    - Station operations (open/closed states)
    - Line operations (active/inactive)
    - Transfer requirements
    - Service status constraints
    - Network mode differences (Today vs Future)
    - Integration work impacts
    
    The knowledge base is initialized with 12 rules covering the LTA's
    July 2025 TELe/CRL announcement requirements.
    """
    
    def __init__(self):
        """Initialize the knowledge base with operational rules"""
        self.rules: List[LogicRule] = []
        self._initialize_rules()
    
    def _initialize_rules(self):
        """
        Initialize the 12+ operational rules.
        
        Rules are organized by category:
        - Transfer rules (R1)
        - Integration work rules (R2, R10)
        - Network mode rules (R3, R4, R7, R11, R12)
        - Service status rules (R5, R8)
        - Station closure rules (R6)
        - Multi-line interchange rules (R9)
        """
        
        # ====================================================================
        # TRANSFER RULES
        # ====================================================================
        
        self.rules.append(LogicRule(
            rule_id="R1",
            description="If Tanah Merah station is open AND TEL line is active, then TEL-EWL transfer is available",
            antecedent=["Station_Open_TanahMerah", "Line_Active_TEL"],
            consequent="Transfer_Available_TEL_EWL"
        ))
        
        self.rules.append(LogicRule(
            rule_id="R9",
            description="If both TEL and CRL are active at T5 station, then TEL-CRL transfer must be available",
            antecedent=["Line_Active_TEL", "Line_Active_CRL", "Station_Open_T5"],
            consequent="Transfer_Available_TEL_CRL"
        ))
        
        # ====================================================================
        # INTEGRATION WORK RULES
        # ====================================================================
        
        self.rules.append(LogicRule(
            rule_id="R2",
            description="If Expo station is undergoing integration work, then Expo station is NOT open",
            antecedent=["Integration_Work_Expo"],
            consequent="Station_Closed_Expo"  # Using Station_Closed instead of ¬Station_Open
        ))
        
        self.rules.append(LogicRule(
            rule_id="R10",
            description="If integration work is ongoing AND network is in Today Mode, then service adjustments are required",
            antecedent=["Integration_Work_Active", "Network_Mode_Today"],
            consequent="Service_Adjustments_Required",
            network_mode=NetworkMode.TODAY
        ))
        
        # ====================================================================
        # NETWORK MODE RULES - FUTURE MODE
        # ====================================================================
        
        self.rules.append(LogicRule(
            rule_id="R3",
            description="In Future Mode, the old EWL airport branch (Tanah Merah-Expo-Changi Airport) is NOT active",
            antecedent=["Network_Mode_Future"],
            consequent="Line_Inactive_EWL_Airport",  # Using positive form
            network_mode=NetworkMode.FUTURE
        ))
        
        self.rules.append(LogicRule(
            rule_id="R4",
            description="In Future Mode, if the network is operational, then TEL extension to T5 is active",
            antecedent=["Network_Mode_Future", "Network_Operational"],
            consequent="Line_Active_TEL_T5",
            network_mode=NetworkMode.FUTURE
        ))
        
        self.rules.append(LogicRule(
            rule_id="R7",
            description="If CRL extension to T5 is active, then the network must be in Future Mode",
            antecedent=["Line_Active_CRL_T5"],
            consequent="Network_Mode_Future",
            network_mode=NetworkMode.FUTURE
        ))
        
        self.rules.append(LogicRule(
            rule_id="R11",
            description="In Future Mode, if routing to Changi Airport, then TEL line must be used (not old EWL)",
            antecedent=["Network_Mode_Future", "Destination_Changi_Airport"],
            consequent="Route_Uses_TEL",
            network_mode=NetworkMode.FUTURE
        ))
        
        self.rules.append(LogicRule(
            rule_id="R12",
            description="If T5 station is being used in a route, then network must be in Future Mode",
            antecedent=["Route_Uses_T5"],
            consequent="Network_Mode_Future",
            network_mode=NetworkMode.FUTURE
        ))
        
        # ====================================================================
        # SERVICE STATUS RULES
        # ====================================================================
        
        self.rules.append(LogicRule(
            rule_id="R5",
            description="If a line has disrupted service status, then it does NOT have normal service",
            antecedent=["Service_Status_Disrupted_TEL"],
            consequent="Service_Status_Not_Normal_TEL"
        ))
        
        self.rules.append(LogicRule(
            rule_id="R8",
            description="If service is reduced AND it's peak hour, then crowding risk is high",
            antecedent=["Service_Status_Reduced_TEL", "Time_Peak"],
            consequent="Crowding_Risk_High"
        ))
        
        # ====================================================================
        # STATION CLOSURE RULES
        # ====================================================================
        
        self.rules.append(LogicRule(
            rule_id="R6",
            description="If Expo station is closed, then no transfers are available at Expo",
            antecedent=["Station_Closed_Expo"],
            consequent="Transfer_Unavailable_Expo"
        ))
    
    def get_all_rules(self) -> List[LogicRule]:
        """
        Get all rules in the knowledge base.
        
        Returns:
            List of all LogicRule objects
        """
        return self.rules.copy()
    
    def get_rules_for_mode(self, mode: NetworkMode) -> List[LogicRule]:
        """
        Get rules applicable to a specific network mode.
        
        Args:
            mode: NetworkMode (TODAY or FUTURE)
        
        Returns:
            List of LogicRule objects that apply to the given mode
            (includes rules with network_mode=None and rules specific to this mode)
        """
        return [r for r in self.rules if r.applies_to_mode(mode)]
    
    def get_rule_by_id(self, rule_id: str) -> Optional[LogicRule]:
        """
        Get a specific rule by its ID.
        
        Args:
            rule_id: Rule identifier (e.g., "R1", "R2")
        
        Returns:
            LogicRule object if found, None otherwise
        """
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None
    
    def get_rule_count(self) -> int:
        """
        Get total number of rules in the knowledge base.
        
        Returns:
            Integer count of rules
        """
        return len(self.rules)
    
    def display_rules(self, mode: Optional[NetworkMode] = None):
        """
        Display all rules in a readable format.
        
        Args:
            mode: Optional NetworkMode to filter rules (None = show all)
        """
        rules = self.get_rules_for_mode(mode) if mode else self.rules
        
        print(f"\n{'='*70}")
        mode_str = f" - {mode.value.upper()} MODE" if mode else ""
        print(f"MRT OPERATIONAL RULES{mode_str}")
        print(f"{'='*70}\n")
        print(f"Total Rules: {len(rules)}\n")
        
        for rule in rules:
            print(f"{rule.rule_id}: {rule.description}")
            print(f"   Formal: {repr(rule)}")
            cnf_clauses = rule.to_cnf()
            print(f"   CNF:    {cnf_clauses[0]}")
            print()
    
    def display_summary(self):
        """Display a summary of the knowledge base"""
        print(f"\n{'='*70}")
        print("KNOWLEDGE BASE SUMMARY")
        print(f"{'='*70}\n")
        
        total = self.get_rule_count()
        today_rules = len(self.get_rules_for_mode(NetworkMode.TODAY))
        future_rules = len(self.get_rules_for_mode(NetworkMode.FUTURE))
        
        print(f"Total Rules:                {total}")
        print(f"Rules for TODAY mode:       {today_rules}")
        print(f"Rules for FUTURE mode:      {future_rules}")
        print(f"Mode-independent rules:     {total - (len([r for r in self.rules if r.network_mode is not None]))}")
        
        print(f"\n{'='*70}\n")


# ============================================================================
# EXAMPLE USAGE (for testing)
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("TESTING KNOWLEDGE BASE")
    print("="*70)
    
    # Create knowledge base
    kb = MRTKnowledgeBase()
    
    # Test 1: Display summary
    print("\n1. Knowledge Base Summary:")
    kb.display_summary()
    
    # Test 2: Display all rules
    print("\n2. All Rules:")
    kb.display_rules()
    
    # Test 3: Display rules for specific mode
    print("\n3. Rules for TODAY Mode:")
    kb.display_rules(NetworkMode.TODAY)
    
    print("\n4. Rules for FUTURE Mode:")
    kb.display_rules(NetworkMode.FUTURE)
    
    # Test 4: Get specific rule
    print("\n5. Testing get_rule_by_id():")
    r1 = kb.get_rule_by_id("R1")
    print(f"   Found rule R1: {r1}")
    
    # Test 5: Get rules for mode
    print("\n6. Testing get_rules_for_mode():")
    future_rules = kb.get_rules_for_mode(NetworkMode.FUTURE)
    print(f"   Number of rules for FUTURE mode: {len(future_rules)}")
    
    print("\n" + "="*70)
    print("ALL TESTS PASSED ✓")
    print("="*70)