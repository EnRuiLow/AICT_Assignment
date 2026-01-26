"""
Data Models for Logical Inference System

This module contains core data structures:
- Proposition: Atomic logic statements
- Clause: CNF clauses (disjunctions of propositions)
- Enums: NetworkMode, ServiceStatus

Author: [Your Name]
Student ID: [Your ID]
"""

from dataclasses import dataclass
from typing import Set
from enum import Enum


class NetworkMode(Enum):
    """
    Network operation mode for MRT system.
    
    TODAY: Current EWL airport branch operations (Tanah Merah → Expo → Changi Airport)
    FUTURE: With TELe/CRL extensions (TEL to T5, CRL to T5, EWL branch converted to TEL)
    """
    TODAY = "today"
    FUTURE = "future"
    
    def __str__(self):
        return self.value.upper()


class ServiceStatus(Enum):
    """
    Service status for MRT lines and stations.
    
    NORMAL: Regular scheduled service
    REDUCED: Reduced frequency or capacity (e.g., during integration works)
    DISRUPTED: Service suspension or major disruption
    """
    NORMAL = "normal"
    REDUCED = "reduced"
    DISRUPTED = "disrupted"
    
    def __str__(self):
        return self.value.capitalize()


@dataclass
class Proposition:
    """
    Represents a propositional logic statement (atomic formula).
    
    A proposition has:
    - name: Identifier (e.g., "Station_Open_Expo")
    - value: Truth value (True or False)
    
    Examples:
        Station_Open_Expo = True  → "Expo station is open"
        Station_Open_Expo = False → "Expo station is NOT open" (¬Station_Open_Expo)
    """
    name: str
    value: bool
    
    def __repr__(self) -> str:
        """String representation: Station_Open_Expo or ¬Station_Open_Expo"""
        return f"{self.name}" if self.value else f"¬{self.name}"
    
    def negate(self) -> 'Proposition':
        """
        Return the logical negation of this proposition.
        
        Returns:
            New Proposition with inverted truth value
        
        Example:
            p = Proposition("Station_Open_Expo", True)
            p.negate() → Proposition("Station_Open_Expo", False)
        """
        return Proposition(self.name, not self.value)
    
    def __eq__(self, other) -> bool:
        """Two propositions are equal if they have same name AND value"""
        if not isinstance(other, Proposition):
            return False
        return self.name == other.name and self.value == other.value
    
    def __hash__(self) -> int:
        """Hash based on name and value (allows use in sets/dicts)"""
        return hash((self.name, self.value))


@dataclass
class Clause:
    """
    Represents a clause in Conjunctive Normal Form (CNF).
    
    A clause is a disjunction (OR) of propositions:
        (A ∨ B ∨ ¬C ∨ D)
    
    In resolution-based inference, we work entirely with CNF clauses.
    
    Special cases:
    - Unit clause: Single proposition (e.g., "A")
    - Empty clause: No propositions (□) - represents contradiction
    
    Attributes:
        propositions: Set of Proposition objects joined by OR
    
    Example:
        Clause({Prop("A", True), Prop("B", False), Prop("C", True)})
        Represents: (A ∨ ¬B ∨ C)
    """
    propositions: Set[Proposition]
    
    def __repr__(self) -> str:
        """
        String representation of the clause.
        
        Returns:
            "□" for empty clause (contradiction)
            "A ∨ ¬B ∨ C" for normal clauses
        """
        if not self.propositions:
            return "□"  # Empty clause symbol
        
        # Sort by name for consistent display
        sorted_props = sorted(self.propositions, key=lambda x: x.name)
        return " ∨ ".join(str(p) for p in sorted_props)
    
    def __hash__(self) -> int:
        """Hash based on frozen set of propositions"""
        return hash(frozenset(self.propositions))
    
    def __eq__(self, other) -> bool:
        """Two clauses are equal if they have same propositions"""
        if not isinstance(other, Clause):
            return False
        return self.propositions == other.propositions
    
    def is_empty(self) -> bool:
        """
        Check if this is an empty clause.
        
        An empty clause (□) represents a logical contradiction.
        In resolution, deriving an empty clause proves the query.
        
        Returns:
            True if clause has no propositions, False otherwise
        """
        return len(self.propositions) == 0
    
    def is_unit_clause(self) -> bool:
        """
        Check if this is a unit clause (single proposition).
        
        Unit clauses represent known facts.
        
        Returns:
            True if clause has exactly one proposition
        """
        return len(self.propositions) == 1
    
    def get_proposition(self) -> Proposition:
        """
        Get the single proposition from a unit clause.
        
        Returns:
            The proposition if this is a unit clause
        
        Raises:
            ValueError if not a unit clause
        """
        if not self.is_unit_clause():
            raise ValueError("Not a unit clause")
        return next(iter(self.propositions))


# ============================================================================
# EXAMPLE USAGE (for testing)
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("TESTING DATA MODELS")
    print("="*70)
    
    # Test Propositions
    print("\n1. Testing Propositions:")
    p1 = Proposition("Station_Open_Expo", True)
    p2 = Proposition("Station_Open_Expo", False)
    p3 = p1.negate()
    
    print(f"   p1: {p1}")
    print(f"   p2: {p2}")
    print(f"   p3 (negation of p1): {p3}")
    print(f"   p2 == p3: {p2 == p3}")
    
    # Test Clauses
    print("\n2. Testing Clauses:")
    c1 = Clause({
        Proposition("Station_Open_Expo", True),
        Proposition("Line_Active_TEL", False),
        Proposition("Transfer_Available", True)
    })
    print(f"   Normal clause: {c1}")
    
    c2 = Clause({Proposition("Station_Open_Expo", True)})
    print(f"   Unit clause: {c2}")
    print(f"   Is unit clause? {c2.is_unit_clause()}")
    
    c3 = Clause(set())
    print(f"   Empty clause: {c3}")
    print(f"   Is empty? {c3.is_empty()}")
    
    # Test Enums
    print("\n3. Testing Enums:")
    print(f"   Network Mode TODAY: {NetworkMode.TODAY}")
    print(f"   Network Mode FUTURE: {NetworkMode.FUTURE}")
    print(f"   Service Status NORMAL: {ServiceStatus.NORMAL}")
    print(f"   Service Status DISRUPTED: {ServiceStatus.DISRUPTED}")
    
    print("\n" + "="*70)
    print("ALL TESTS PASSED ✓")
    print("="*70)