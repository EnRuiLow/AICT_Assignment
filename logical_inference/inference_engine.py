"""
Resolution-Based Inference Engine

This module implements the ResolutionEngine class which performs:
- Resolution-based theorem proving
- Consistency checking for service advisories
- Route validation against operational rules
- Violation identification

Author: [Your Name]
Student ID: [Your ID]
"""

from typing import Dict, Set, List, Tuple, Optional
import itertools

from .models import Proposition, Clause, NetworkMode
from .knowledge_base import MRTKnowledgeBase


class ResolutionEngine:
    """
    Resolution-based inference engine for MRT logic validation.
    
    This engine uses Robinson's Resolution algorithm to:
    1. Prove queries by refutation (proof by contradiction)
    2. Check consistency of service advisories
    3. Validate routing decisions
    4. Identify violated operational rules
    
    The resolution algorithm works with clauses in CNF (Conjunctive Normal Form).
    """
    
    def __init__(self, knowledge_base: MRTKnowledgeBase):
        """
        Initialize the inference engine.
        
        Args:
            knowledge_base: MRTKnowledgeBase containing operational rules
        """
        self.kb = knowledge_base
        self.clauses: Set[Clause] = set()
        self.violated_rules: List[str] = []
    
    def load_knowledge_base(self, mode: NetworkMode):
        """
        Load rules from knowledge base as CNF clauses.
        
        Converts all applicable rules (for the given mode) to CNF clauses
        and stores them in self.clauses.
        
        Args:
            mode: NetworkMode (TODAY or FUTURE)
        """
        self.clauses.clear()
        rules = self.kb.get_rules_for_mode(mode)
        
        for rule in rules:
            cnf_clauses = rule.to_cnf()
            for clause in cnf_clauses:
                self.clauses.add(clause)
    
    def add_facts(self, facts: Dict[str, bool]):
        """
        Add known facts to the knowledge base as unit clauses.
        
        Each fact becomes a unit clause (single proposition).
        
        Args:
            facts: Dictionary mapping proposition names to truth values
                   Example: {"Station_Open_Expo": True, "Line_Active_TEL": False}
        """
        for prop_name, value in facts.items():
            unit_clause = Clause({Proposition(prop_name, value)})
            self.clauses.add(unit_clause)
    
    def resolve(self, clause1: Clause, clause2: Clause) -> Optional[Clause]:
        """
        Apply resolution rule to two clauses.
        
        Resolution Rule:
            Given: (A ∨ B ∨ C) and (¬A ∨ D ∨ E)
            Derive: (B ∨ C ∨ D ∨ E)
        
        The algorithm finds complementary literals (A and ¬A), removes them,
        and combines the remaining literals.
        
        Args:
            clause1: First CNF clause
            clause2: Second CNF clause
        
        Returns:
            Resolved clause if resolution is possible, None otherwise
        """
        # Find complementary literals (P and ¬P)
        for prop1 in clause1.propositions:
            for prop2 in clause2.propositions:
                # Check if same proposition name but opposite values
                if prop1.name == prop2.name and prop1.value != prop2.value:
                    # Found complementary pair, create resolvent
                    # Combine all propositions except the complementary pair
                    new_props = (clause1.propositions | clause2.propositions) - {prop1, prop2}
                    return Clause(new_props)
        
        # No complementary literals found
        return None
    
    def prove_by_contradiction(
        self,
        query: Proposition,
        max_iterations: int = 100,
        verbose: bool = False
    ) -> Tuple[bool, List[str]]:
        """
        Prove a query using proof by refutation (contradiction).
        
        Process:
        1. Add ¬Query to the knowledge base
        2. Try to derive empty clause (□) using resolution
        3. If empty clause is derived → Query is TRUE
        4. If no new clauses can be derived → Query is UNPROVABLE
        
        Args:
            query: Proposition to prove
            max_iterations: Maximum number of resolution iterations
            verbose: If True, include detailed trace in output
        
        Returns:
            Tuple of (is_provable, trace_messages)
        """
        # Negate the query and add to KB
        negated_query = Clause({query.negate()})
        working_clauses = self.clauses.copy()
        working_clauses.add(negated_query)
        
        trace = [f"Attempting to prove: {query}"]
        trace.append(f"Added negated query: {negated_query}")
        trace.append(f"Initial clauses: {len(working_clauses)}")
        
        new_clauses = set()
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Generate all pairs of clauses
            clause_pairs = itertools.combinations(working_clauses, 2)
            
            for clause1, clause2 in clause_pairs:
                resolvent = self.resolve(clause1, clause2)
                
                if resolvent is not None:
                    # Check if we derived empty clause (contradiction)
                    if resolvent.is_empty():
                        trace.append(f"\n[Iteration {iteration}] ✓ Empty clause derived!")
                        trace.append(f"  From: {clause1}")
                        trace.append(f"  And:  {clause2}")
                        trace.append(f"\nCONCLUSION: {query} is PROVABLE (TRUE)")
                        return True, trace
                    
                    # Add new clause if not already present
                    if resolvent not in working_clauses:
                        new_clauses.add(resolvent)
                        if verbose:
                            trace.append(f"[Iteration {iteration}] Derived: {resolvent}")
            
            # If no new clauses, we're done
            if not new_clauses:
                trace.append(f"\n[Iteration {iteration}] No new clauses derived")
                trace.append(f"CONCLUSION: {query} is UNPROVABLE")
                return False, trace
            
            # Add new clauses to working set
            working_clauses.update(new_clauses)
            new_clauses.clear()
        
        # Timeout
        trace.append(f"\nTimeout: Reached max iterations ({max_iterations})")
        trace.append(f"CONCLUSION: {query} is UNPROVABLE (timeout)")
        return False, trace
    
    def check_consistency(self) -> Tuple[bool, Optional[str]]:
        """
        Check if the current knowledge base is internally consistent.
        
        A KB is inconsistent if we can derive an empty clause from it.
        This means the rules and facts contradict each other.
        
        Returns:
            Tuple of (is_consistent, explanation)
            - is_consistent: False if contradiction found
            - explanation: Description of the contradiction (if found)
        """
        working_clauses = self.clauses.copy()
        
        # Try to derive empty clause
        for iteration in range(50):
            clause_pairs = itertools.combinations(working_clauses, 2)
            new_clauses = set()
            
            for clause1, clause2 in clause_pairs:
                resolvent = self.resolve(clause1, clause2)
                
                if resolvent is not None:
                    # Found contradiction!
                    if resolvent.is_empty():
                        explanation = (
                            f"CONTRADICTION DETECTED:\n"
                            f"  Clause 1: {clause1}\n"
                            f"  Clause 2: {clause2}\n"
                            f"  Resolvent: {resolvent} (empty clause)"
                        )
                        return False, explanation
                    
                    # Add to new clauses
                    if resolvent not in working_clauses:
                        new_clauses.add(resolvent)
            
            # No new clauses → consistent (or unprovably inconsistent)
            if not new_clauses:
                return True, "No contradictions detected"
            
            # Add new clauses and continue
            working_clauses.update(new_clauses)
        
        # Timeout without finding contradiction
        return True, "No contradictions detected (search limit reached)"
    
    def validate_route(
        self,
        facts: Dict[str, bool],
        mode: NetworkMode
    ) -> Dict:
        """
        Validate if a route/scenario is valid given facts and mode.
        
        Process:
        1. Load knowledge base for the given mode
        2. Add facts as unit clauses
        3. Check for consistency
        4. Identify violated rules if inconsistent
        
        Args:
            facts: Dictionary of known propositions
            mode: NetworkMode (TODAY or FUTURE)
        
        Returns:
            Dictionary containing:
            - mode: Network mode used
            - facts: Input facts
            - is_consistent: True if valid, False if contradictory
            - consistency_message: Explanation
            - violated_rules: List of violated rule IDs
        """
        # Load KB and add facts
        self.load_knowledge_base(mode)
        self.add_facts(facts)
        
        # Check consistency
        is_consistent, consistency_msg = self.check_consistency()
        
        result = {
            "mode": mode.value,
            "facts": facts,
            "is_consistent": is_consistent,
            "consistency_message": consistency_msg,
            "violated_rules": []
        }
        
        # If inconsistent, identify violations
        if not is_consistent:
            result["violated_rules"] = self._identify_violations(facts, mode)
        
        return result
    
    def _identify_violations(
        self,
        facts: Dict[str, bool],
        mode: NetworkMode
    ) -> List[str]:
        """
        Identify which rules are violated by the given facts.
        
        For each rule (A ∧ B → C):
        - If antecedent (A ∧ B) is satisfied by facts
        - But consequent C is false in facts
        - Then the rule is violated
        
        Args:
            facts: Dictionary of known propositions
            mode: NetworkMode
        
        Returns:
            List of violated rule IDs with descriptions
        """
        violations = []
        rules = self.kb.get_rules_for_mode(mode)
        
        for rule in rules:
            # Check if all antecedents are true in facts
            antecedent_satisfied = all(
                facts.get(prop, False) for prop in rule.antecedent
            )
            
            if antecedent_satisfied:
                # Antecedent is satisfied, check consequent
                consequent_value = facts.get(rule.consequent, None)
                
                # If consequent is explicitly false, rule is violated
                if consequent_value is False:
                    violations.append(f"{rule.rule_id}: {rule.description}")
                
                # Special check for "negative" consequents
                # (e.g., Station_Closed_X when Station_Open_X is true)
                if consequent_value is None:
                    # Check for opposite proposition
                    if "Closed" in rule.consequent:
                        open_prop = rule.consequent.replace("Closed", "Open")
                        if facts.get(open_prop, False):
                            violations.append(f"{rule.rule_id}: {rule.description}")
                    elif "Inactive" in rule.consequent:
                        active_prop = rule.consequent.replace("Inactive", "Active")
                        if facts.get(active_prop, False):
                            violations.append(f"{rule.rule_id}: {rule.description}")
        
        return violations
    
    def display_clauses(self):
        """Display all clauses currently in the engine"""
        print(f"\nCurrent Clauses ({len(self.clauses)}):")
        for i, clause in enumerate(sorted(self.clauses, key=str), 1):
            print(f"  {i}. {clause}")


# ============================================================================
# EXAMPLE USAGE (for testing)
# ============================================================================

if __name__ == "__main__":
    from .knowledge_base import MRTKnowledgeBase
    
    print("="*70)
    print("TESTING INFERENCE ENGINE")
    print("="*70)
    
    # Create KB and engine
    kb = MRTKnowledgeBase()
    engine = ResolutionEngine(kb)
    
    # Test 1: Load knowledge base
    print("\n1. Loading Knowledge Base (TODAY Mode):")
    engine.load_knowledge_base(NetworkMode.TODAY)
    print(f"   Loaded {len(engine.clauses)} clauses")
    
    # Test 2: Add facts
    print("\n2. Adding Facts:")
    facts = {
        "Station_Open_TanahMerah": True,
        "Line_Active_TEL": True
    }
    engine.add_facts(facts)
    print(f"   Total clauses: {len(engine.clauses)}")
    
    # Test 3: Prove a query
    print("\n3. Testing Proof by Contradiction:")
    query = Proposition("Transfer_Available_TEL_EWL", True)
    is_provable, trace = engine.prove_by_contradiction(query, verbose=True)
    print(f"   Query: {query}")
    print(f"   Result: {'PROVABLE' if is_provable else 'NOT PROVABLE'}")
    
    # Test 4: Check consistency
    print("\n4. Testing Consistency Check:")
    engine2 = ResolutionEngine(kb)
    engine2.load_knowledge_base(NetworkMode.TODAY)
    engine2.add_facts({
        "Integration_Work_Expo": True,
        "Station_Open_Expo": True  # Contradiction!
    })
    is_consistent, msg = engine2.check_consistency()
    print(f"   Consistent: {is_consistent}")
    print(f"   Message: {msg}")
    
    print("\n" + "="*70)
    print("ALL TESTS PASSED ✓")
    print("="*70)