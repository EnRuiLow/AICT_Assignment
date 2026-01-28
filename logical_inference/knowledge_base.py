"""
MRT Knowledge Base - FINAL VERSION (Concise Rules)

Single-statement rule descriptions for clarity and brevity.

Author: [Your Name]
Student ID: [Your ID]
Version: 6.0 (FINAL - Concise descriptions)
"""

from typing import List, Optional
from logical_inference.models import NetworkMode
from logical_inference.rules import LogicRule


class MRTKnowledgeBase:
    """
    Knowledge base containing MRT operational rules.
    
    TODAY Mode: TEL terminus at Sungei Bedok; CG line separate (3 stations)
    FUTURE Mode: TELe loop extends to T5; CG stations absorbed into TEL
    
    Contains 27 operational rules with concise descriptions
    """
    
    def __init__(self):
        """Initialize the knowledge base with operational rules"""
        self.rules: List[LogicRule] = []
        self._initialize_rules()
    
    def _initialize_rules(self):
        """Initialize the 27 operational rules with concise descriptions"""
        
        # ====================================================================
        # CURRENT NETWORK INTERCHANGE RULES
        # ====================================================================
        
        self.rules.append(LogicRule(
            rule_id="R1",
            description="If TEL active and Woodlands open, TEL-NSL transfer available",
            antecedent=["Line_Active_TEL", "Station_Open_Woodlands"],
            consequent="Transfer_Available_TEL_NSL_Woodlands"
        ))
        
        self.rules.append(LogicRule(
            rule_id="R2",
            description="If TEL active and Outram Park open, TEL-NEL transfer available",
            antecedent=["Line_Active_TEL", "Station_Open_OutramPark"],
            consequent="Transfer_Available_TEL_NEL_OutramPark"
        ))
        
        self.rules.append(LogicRule(
            rule_id="R3",
            description="If TEL active and Caldecott open, TEL-CCL transfer available",
            antecedent=["Line_Active_TEL", "Station_Open_Caldecott"],
            consequent="Transfer_Available_TEL_CCL_Caldecott"
        ))
        
        self.rules.append(LogicRule(
            rule_id="R4",
            description="If TEL active and Sungei Bedok open, TEL-DTL transfer available",
            antecedent=["Line_Active_TEL", "Station_Open_SungeiBedok"],
            consequent="Transfer_Available_TEL_DTL_SungeiBedok"
        ))
        
        self.rules.append(LogicRule(
            rule_id="R5",
            description="If TEL active and Marina Bay open, TEL-NSL-CCL triple interchange available",
            antecedent=["Line_Active_TEL", "Station_Open_MarinaBay"],
            consequent="Transfer_Available_TEL_NSL_CCL_MarinaBay"
        ))
        
        self.rules.append(LogicRule(
            rule_id="R6",
            description="If TEL active and Orchard open, TEL-NSL transfer available",
            antecedent=["Line_Active_TEL", "Station_Open_Orchard"],
            consequent="Transfer_Available_TEL_NSL_Orchard"
        ))
        
        # ====================================================================
        # TODAY MODE NETWORK CHARACTERISTICS
        # ====================================================================
        
        self.rules.append(LogicRule(
            rule_id="R7",
            description="If Today Mode and TEL active, TEL terminates at Sungei Bedok",
            antecedent=["Network_Mode_Today", "Line_Active_TEL"],
            consequent="TEL_Terminus_Sungei_Bedok",
            network_mode=NetworkMode.TODAY
        ))
        
        self.rules.append(LogicRule(
            rule_id="R8",
            description="If Today Mode and routing to airport, route uses CG line",
            antecedent=["Network_Mode_Today", "Destination_Changi_Airport"],
            consequent="Route_Uses_CG_Line",
            network_mode=NetworkMode.TODAY
        ))
        
        self.rules.append(LogicRule(
            rule_id="R9",
            description="If Today Mode and CG line active, Tanah Merah-Expo-Changi route operational",
            antecedent=["Network_Mode_Today", "Line_Active_CG"],
            consequent="CG_Line_Tanah_Merah_Expo_Changi_Operational",
            network_mode=NetworkMode.TODAY
        ))
        
        # ====================================================================
        # SERVICE STATUS RULES
        # ====================================================================
        
        self.rules.append(LogicRule(
            rule_id="R10",
            description="If line disrupted, normal service: False",
            antecedent=["Service_Status_Disrupted"],
            consequent="Service_Status_Not_Normal"
        ))
        
        self.rules.append(LogicRule(
            rule_id="R11",
            description="If service reduced and peak hour, crowding risk: High",
            antecedent=["Service_Status_Reduced", "Time_Peak"],
            consequent="Crowding_Risk_High"
        ))
        
        # ====================================================================
        # INTEGRATION WORK RULES
        # ====================================================================
        
        self.rules.append(LogicRule(
            rule_id="R12",
            description="If Expo integration work ongoing, Expo: Closed",
            antecedent=["Integration_Work_Expo"],
            consequent="Station_Closed_Expo"
        ))
        
        self.rules.append(LogicRule(
            rule_id="R13",
            description="If integration work ongoing and Today Mode, service adjustments required",
            antecedent=["Integration_Work_Active", "Network_Mode_Today"],
            consequent="Service_Adjustments_Required",
            network_mode=NetworkMode.TODAY
        ))
        
        self.rules.append(LogicRule(
            rule_id="R14",
            description="If Expo closed, transfers at Expo: Unavailable",
            antecedent=["Station_Closed_Expo"],
            consequent="Transfer_Unavailable_Expo"
        ))
        
        # ====================================================================
        # FUTURE MODE ROUTING CONSTRAINTS
        # ====================================================================
        
        self.rules.append(LogicRule(
            rule_id="R15",
            description="If Future Mode, CG line as separate entity: Inactive",
            antecedent=["Network_Mode_Future"],
            consequent="Line_Inactive_CG_Separate",
            network_mode=NetworkMode.FUTURE
        ))
        
        self.rules.append(LogicRule(
            rule_id="R16",
            description="If Future Mode and network operational, TEL extension to T5: Active",
            antecedent=["Network_Mode_Future", "Network_Operational"],
            consequent="Line_Active_TEL_T5",
            network_mode=NetworkMode.FUTURE
        ))
        
        self.rules.append(LogicRule(
            rule_id="R17",
            description="If route uses T5, network mode: Future",
            antecedent=["Route_Uses_T5"],
            consequent="Network_Mode_Future",
            network_mode=NetworkMode.FUTURE
        ))
        
        # ====================================================================
        # FUTURE MODE TRANSFER RULES
        # ====================================================================
        
        self.rules.append(LogicRule(
            rule_id="R18",
            description="If Future Mode and TEL+CRL active at T5, TEL-CRL transfer available",
            antecedent=["Line_Active_TEL", "Line_Active_CRL", "Station_Open_T5"],
            consequent="Transfer_Available_TEL_CRL_T5",
            network_mode=NetworkMode.FUTURE
        ))
        
        self.rules.append(LogicRule(
            rule_id="R19",
            description="If Future Mode and Tanah Merah open with EWL+TEL active, dual platform access: Available",
            antecedent=["Station_Open_TanahMerah", "Line_Active_EWL", "Line_Active_TEL", "Network_Mode_Future"],
            consequent="Dual_Platform_Access_TanahMerah_EW4_TE31",
            network_mode=NetworkMode.FUTURE
        ))
        
        # ====================================================================
        # SYSTEMS INTEGRATION RULES
        # ====================================================================
        
        self.rules.append(LogicRule(
            rule_id="R20",
            description="If systems integration active, service adjustments required",
            antecedent=["Systems_Integration_Active"],
            consequent="Service_Adjustments_Required"
        ))
        
        self.rules.append(LogicRule(
            rule_id="R21",
            description="If signalling conversion active, service disruptions: Yes",
            antecedent=["Station_Signalling_Conversion_Active"],
            consequent="Service_Adjustments_Required"
        ))
        
        self.rules.append(LogicRule(
            rule_id="R22",
            description="If platform doors modification active, station capacity: Reduced",
            antecedent=["Platform_Doors_Modification_Active"],
            consequent="Station_Reduced_Capacity"
        ))
        
        self.rules.append(LogicRule(
            rule_id="R23",
            description="If power supply conversion active, alternative routing: Required",
            antecedent=["Power_Supply_Conversion_Active"],
            consequent="Alternative_Routing_Required"
        ))
        
        # ====================================================================
        # TELe LOOP STRUCTURE RULES (FUTURE MODE)
        # ====================================================================
        
        self.rules.append(LogicRule(
            rule_id="R24",
            description="If Future Mode and TELe loop operational, former CG stations accessible via TELe",
            antecedent=["TELe_Loop_Operational", "Network_Mode_Future"],
            consequent="Former_CG_Stations_Via_TELe_Loop",
            network_mode=NetworkMode.FUTURE
        ))
        
        self.rules.append(LogicRule(
            rule_id="R25",
            description="If Future Mode and airport open with TELe loop, airport access via TEL-Tanah Merah interchange",
            antecedent=["Network_Mode_Future", "Station_Open_Changi_Airport", "TELe_Loop_Operational"],
            consequent="Changi_Airport_Via_TEL_Tanah_Merah_Interchange",
            network_mode=NetworkMode.FUTURE
        ))
        
        self.rules.append(LogicRule(
            rule_id="R26",
            description="If Future Mode and routing to airport via TEL, route passes through Tanah Merah TE31",
            antecedent=["Network_Mode_Future", "Destination_Changi_Airport", "Route_Uses_TEL"],
            consequent="Route_Via_TanahMerah_TE31_Interchange",
            network_mode=NetworkMode.FUTURE
        ))
        
        self.rules.append(LogicRule(
            rule_id="R27",
            description="If Future Mode and Tanah Merah open with TELe loop, Tanah Merah TE31: Loop entry point",
            antecedent=["Station_Open_TanahMerah", "Network_Mode_Future", "TELe_Loop_Operational"],
            consequent="TanahMerah_TE31_Is_TELe_Loop_Entry",
            network_mode=NetworkMode.FUTURE
        ))
    
    def get_all_rules(self) -> List[LogicRule]:
        """Get all rules in the knowledge base"""
        return self.rules.copy()
    
    def get_rules_for_mode(self, mode: NetworkMode) -> List[LogicRule]:
        """Get rules applicable to a specific network mode"""
        return [r for r in self.rules if r.applies_to_mode(mode)]
    
    def get_rule_by_id(self, rule_id: str) -> Optional[LogicRule]:
        """Get a specific rule by its ID"""
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None
    
    def get_today_only_rules(self) -> List[LogicRule]:
        """Get rules that ONLY apply to TODAY mode"""
        return [r for r in self.rules if r.network_mode == NetworkMode.TODAY]
    
    def get_future_only_rules(self) -> List[LogicRule]:
        """Get rules that ONLY apply to FUTURE mode"""
        return [r for r in self.rules if r.network_mode == NetworkMode.FUTURE]
    
    def get_interchange_rules(self) -> List[LogicRule]:
        """Get all interchange-related rules"""
        interchange_ids = ["R1", "R2", "R3", "R4", "R5", "R6", "R18", "R19"]
        return [r for r in self.rules if r.rule_id in interchange_ids]
    
    def get_rule_count(self) -> int:
        """Get total number of rules in the knowledge base"""
        return len(self.rules)
    
    def display_rules(self, mode: Optional[NetworkMode] = None, 
                     today_only: bool = False,
                     future_only: bool = False,
                     interchange_only: bool = False,
                     format: str = "standard"):
        """
        Display rules in a readable format
        
        Args:
            mode: Filter by NetworkMode
            today_only: Show only TODAY-specific rules
            future_only: Show only FUTURE-specific rules
            interchange_only: Show only interchange rules
            format: "standard" or "concise" (just rule ID and description)
        """
        if today_only:
            rules = self.get_today_only_rules()
            header = "TODAY MODE ONLY RULES"
        elif future_only:
            rules = self.get_future_only_rules()
            header = "FUTURE MODE ONLY RULES"
        elif interchange_only:
            rules = self.get_interchange_rules()
            header = "INTERCHANGE RULES"
        elif mode:
            rules = self.get_rules_for_mode(mode)
            header = f"RULES APPLICABLE TO {mode.value.upper()} MODE"
        else:
            rules = self.rules
            header = "ALL MRT OPERATIONAL RULES"
        
        print(f"\n{'='*80}")
        print(header)
        print(f"{'='*80}\n")
        print(f"Total Rules: {len(rules)}\n")
        
        if format == "concise":
            for rule in rules:
                print(f"{rule.rule_id}: {rule.description}")
        else:
            for rule in rules:
                print(f"{rule.rule_id}: {rule.description}")
                print(f"   Formal: {repr(rule)}")
                cnf_clauses = rule.to_cnf()
                print(f"   CNF:    {cnf_clauses[0]}")
                print()
    
    def display_summary(self):
        """Display a summary of the knowledge base"""
        print(f"\n{'='*80}")
        print("KNOWLEDGE BASE SUMMARY - CONCISE VERSION")
        print(f"{'='*80}\n")
        
        total = self.get_rule_count()
        today_rules = len(self.get_rules_for_mode(NetworkMode.TODAY))
        future_rules = len(self.get_rules_for_mode(NetworkMode.FUTURE))
        today_only = len(self.get_today_only_rules())
        future_only = len(self.get_future_only_rules())
        
        print(f"Total Rules:                      {total}")
        print(f"\nRules applicable to TODAY mode:   {today_rules}")
        print(f"  - TODAY-only rules:             {today_only}")
        print(f"\nRules applicable to FUTURE mode:  {future_rules}")
        print(f"  - FUTURE-only rules:            {future_only}")
        print(f"\nMode-independent rules:           {total - today_only - future_only}")
        
        print(f"\n{'='*80}\n")
    
    def display_rules_concise(self):
        """Display all rules in concise format (ID + description only)"""
        print(f"\n{'='*80}")
        print("ALL RULES - CONCISE FORMAT")
        print(f"{'='*80}\n")
        
        for rule in self.rules:
            mode_tag = ""
            if rule.network_mode == NetworkMode.TODAY:
                mode_tag = " [TODAY]"
            elif rule.network_mode == NetworkMode.FUTURE:
                mode_tag = " [FUTURE]"
            
            print(f"{rule.rule_id}: {rule.description}{mode_tag}")
        
        print(f"\n{'='*80}\n")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("="*80)
    print("MRT KNOWLEDGE BASE - CONCISE RULE DESCRIPTIONS")
    print("="*80)
    
    kb = MRTKnowledgeBase()
    
    # Display summary
    kb.display_summary()
    
    # Display all rules in concise format
    kb.display_rules_concise()
    
    # Display TODAY-only rules
    print("\n" + "="*80)
    print("TODAY MODE ONLY RULES (Concise)")
    print("="*80)
    kb.display_rules(today_only=True, format="concise")
    
    # Display FUTURE-only rules
    print("\n" + "="*80)
    print("FUTURE MODE ONLY RULES (Concise)")
    print("="*80)
    kb.display_rules(future_only=True, format="concise")
    
    print("\n" + "="*80)
    print("✓ CONCISE VERSION COMPLETE")
    print("="*80)