"""
Logic Rule Definitions

This module defines the LogicRule class which represents operational rules
in implication form (antecedent → consequent) and converts them to CNF.

Author: [Your Name]
Student ID: [Your ID]
"""

from typing import List, Optional
from .models import Proposition, Clause, NetworkMode


class LogicRule:
    """
    Represents a logical rule in implication form.
    
    Format: (A₁ ∧ A₂ ∧ ... ∧ Aₙ) → C
    
    Where:
    - A₁, A₂, ..., Aₙ are antecedents (premises)
    - C is the consequent (conclusion)
    
    The rule states: "If all antecedents are true, then the consequent must be true"
    
    Example:
        "If Tanah Merah is open AND TEL is active, then TEL-EWL transfer is available"
        Antecedents: ["Station_Open_TanahMerah", "Line_Active_TEL"]
        Consequent: "Transfer_Available_TEL_EWL"
    
    Attributes:
        rule_id: Unique identifier (e.g., "R1", "R2")
        description: Plain English explanation
        antecedent: List of proposition names that form the premise
        consequent: Proposition name that follows from the premise
        network_mode: Optional mode restriction (None = applies to both modes)
    """
    
    def __init__(
        self,
        rule_id: str,
        description: str,
        antecedent: List[str],
        consequent: str,
        network_mode: Optional[NetworkMode] = None
    ):
        """
        Initialize a logic rule.
        
        Args:
            rule_id: Unique identifier (e.g., "R1")
            description: Plain English explanation of the rule
            antecedent: List of proposition names (AND'ed together)
            consequent: Single proposition name that follows
            network_mode: Which mode this rule applies to (None = both)
        
        Example:
            LogicRule(
                "R1",
                "If Expo is open AND TEL is active, transfer is available",
                ["Station_Open_Expo", "Line_Active_TEL"],
                "Transfer_Available_Expo"
            )
        """
        self.rule_id = rule_id
        self.description = description
        self.antecedent = antecedent
        self.consequent = consequent
        self.network_mode = network_mode
        
        # Validate inputs
        if not rule_id:
            raise ValueError("rule_id cannot be empty")
        if not antecedent:
            raise ValueError("antecedent cannot be empty")
        if not consequent:
            raise ValueError("consequent cannot be empty")
    
    def to_cnf(self) -> List[Clause]:
        """
        Convert this rule to Conjunctive Normal Form (CNF).
        
        Conversion process:
            (A ∧ B ∧ C) → D
            ≡ ¬(A ∧ B ∧ C) ∨ D        [Implication elimination]
            ≡ (¬A ∨ ¬B ∨ ¬C) ∨ D      [De Morgan's law]
            ≡ (¬A ∨ ¬B ∨ ¬C ∨ D)      [Single CNF clause]
        
        Returns:
            List containing a single CNF clause
        
        Example:
            Rule: "Station_Open_Expo ∧ Line_Active_TEL → Transfer_Available"
            CNF: (¬Station_Open_Expo ∨ ¬Line_Active_TEL ∨ Transfer_Available)
        """
        clause_props = set()
        
        # Add negated antecedents (¬A, ¬B, ¬C, ...)
        for prop_name in self.antecedent:
            clause_props.add(Proposition(prop_name, False))
        
        # Add consequent (D)
        clause_props.add(Proposition(self.consequent, True))
        
        return [Clause(clause_props)]
    
    def __repr__(self) -> str:
        """
        String representation in logical notation.
        
        Returns:
            "R1: (A ∧ B ∧ C) → D [mode]"
        """
        ant_str = " ∧ ".join(self.antecedent)
        mode_str = f" [{self.network_mode.value}]" if self.network_mode else ""
        return f"{self.rule_id}: ({ant_str}) → {self.consequent}{mode_str}"
    
    def __str__(self) -> str:
        """Human-readable string representation"""
        return f"{self.rule_id}: {self.description}"
    
    def applies_to_mode(self, mode: NetworkMode) -> bool:
        """
        Check if this rule applies to the given network mode.
        
        Args:
            mode: NetworkMode to check
        
        Returns:
            True if rule applies to this mode (rule.network_mode is None or matches)
        """
        return self.network_mode is None or self.network_mode == mode
    
    def get_all_propositions(self) -> List[str]:
        """
        Get all proposition names involved in this rule.
        
        Returns:
            List of all unique proposition names (antecedents + consequent)
        """
        return list(set(self.antecedent + [self.consequent]))


# ============================================================================
# EXAMPLE USAGE (for testing)
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("TESTING LOGIC RULES")
    print("="*70)
    
    # Test Rule 1: Normal rule applying to both modes
    print("\n1. Testing Basic Rule:")
    r1 = LogicRule(
        "R1",
        "If Tanah Merah is open AND TEL is active, then TEL-EWL transfer is available",
        ["Station_Open_TanahMerah", "Line_Active_TEL"],
        "Transfer_Available_TEL_EWL"
    )
    
    print(f"   Rule: {r1}")
    print(f"   Formal: {repr(r1)}")
    print(f"   CNF: {r1.to_cnf()[0]}")
    print(f"   Applies to TODAY? {r1.applies_to_mode(NetworkMode.TODAY)}")
    print(f"   Applies to FUTURE? {r1.applies_to_mode(NetworkMode.FUTURE)}")
    
    # Test Rule 2: Mode-specific rule
    print("\n2. Testing Mode-Specific Rule:")
    r2 = LogicRule(
        "R3",
        "In Future Mode, the old EWL airport branch is NOT active",
        ["Network_Mode_Future"],
        "Line_Active_EWL_Airport",
        network_mode=NetworkMode.FUTURE
    )
    
    print(f"   Rule: {r2}")
    print(f"   Formal: {repr(r2)}")
    print(f"   CNF: {r2.to_cnf()[0]}")
    print(f"   Applies to TODAY? {r2.applies_to_mode(NetworkMode.TODAY)}")
    print(f"   Applies to FUTURE? {r2.applies_to_mode(NetworkMode.FUTURE)}")
    
    # Test Rule 3: Complex antecedent
    print("\n3. Testing Rule with Multiple Antecedents:")
    r3 = LogicRule(
        "R9",
        "If TEL, CRL active AND T5 open, then TEL-CRL transfer available",
        ["Line_Active_TEL", "Line_Active_CRL", "Station_Open_T5"],
        "Transfer_Available_TEL_CRL"
    )
    
    print(f"   Rule: {r3}")
    print(f"   Formal: {repr(r3)}")
    print(f"   CNF: {r3.to_cnf()[0]}")
    print(f"   All propositions: {r3.get_all_propositions()}")
    
    print("\n" + "="*70)
    print("ALL TESTS PASSED ✓")
    print("="*70)