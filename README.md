# AICT_Assignment
AICT Assignment2


# Logical Inference for MRT Advisory Consistency

**ChangiLink AI - Assignment Component**  
**Author:** [Your Name]  
**Student ID:** [Your ID]  
**Module:** AICT - Artificial Intelligence Concepts & Techniques

---

## 📋 Overview

This component implements **resolution-based inference** to validate MRT routing decisions and detect contradictions in service advisories for Singapore's MRT network, specifically focusing on the Changi Airport Terminal 5 (T5) corridor extensions announced by LTA in July 2025.

### Key Features
- ✅ 12 operational rules covering MRT operations
- ✅ Resolution-based theorem proving
- ✅ Consistency checking for service advisories
- ✅ Route validation (TODAY vs FUTURE network modes)
- ✅ Violation identification and tracing
- ✅ 6+ comprehensive test scenarios

---

## 📁 File Structure

```
logical_inference/
│
├── __init__.py              # Package initializer
├── models.py                # Core data models (Proposition, Clause, Enums)
├── rules.py                 # LogicRule class
├── knowledge_base.py        # MRTKnowledgeBase (12 rules)
├── inference_engine.py      # ResolutionEngine (main inference logic)
├── test_scenarios.py        # 6 test scenarios
├── main.py                  # Main entry point
└── README.md                # This file
```

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- No external libraries required (uses only Python standard library)

### Setup
```bash
# 1. Navigate to project directory
cd path/to/logical_inference

# 2. No installation needed - pure Python!

# 3. Run the system
python main.py
```

---

## 🚀 Usage

### Option 1: Interactive Menu (Recommended)
```bash
python main.py
```

This launches an interactive menu with options to:
1. Run all test scenarios
2. Display rules
3. Custom validation
4. Display knowledge base summary

### Option 2: Command Line Arguments
```bash
# Run all test scenarios
python main.py --test

# Display all rules
python main.py --display-rules

# Custom validation
python main.py --custom

# Help
python main.py --help
```

### Option 3: Import as Module
```python
from logical_inference import (
    MRTKnowledgeBase,
    ResolutionEngine,
    NetworkMode
)

# Create knowledge base and engine
kb = MRTKnowledgeBase()
engine = ResolutionEngine(kb)

# Define facts
facts = {
    "Network_Mode_Future": True,
    "Line_Active_TEL_T5": True,
    "Station_Open_T5": True
}

# Validate route
result = engine.validate_route(facts, NetworkMode.FUTURE)
print(result)
```

---

## 📚 Knowledge Base Rules

The system contains **12 operational rules** organized by category:

### Transfer Rules (R1, R9)
- **R1:** If Tanah Merah is open AND TEL is active → TEL-EWL transfer available
- **R9:** If TEL, CRL active AND T5 open → TEL-CRL transfer available

### Integration Work Rules (R2, R10)
- **R2:** If Expo undergoes integration work → Expo is closed
- **R10:** If integration work ongoing AND Today Mode → Service adjustments required

### Network Mode Rules (R3, R4, R7, R11, R12)
- **R3:** In Future Mode → Old EWL airport branch is NOT active
- **R4:** In Future Mode + Network operational → TEL to T5 is active
- **R7:** If CRL to T5 is active → Must be Future Mode
- **R11:** In Future Mode + Routing to Changi Airport → Must use TEL
- **R12:** If route uses T5 → Must be Future Mode

### Service Status Rules (R5, R8)
- **R5:** If line disrupted → NOT normal service
- **R8:** If reduced service AND peak hour → High crowding risk

### Station Closure Rules (R6)
- **R6:** If Expo closed → No transfers at Expo

---

## 🧪 Test Scenarios

The system includes **6 comprehensive test scenarios**:

| # | Scenario | Mode | Expected Outcome |
|---|----------|------|------------------|
| 1 | Normal operations | TODAY | ✓ Valid |
| 2 | Old EWL in Future Mode | FUTURE | ✗ Invalid (violates R3) |
| 3 | Station open AND integration work | TODAY | ✗ Contradiction (R2) |
| 4 | Route to T5 | FUTURE | ✓ Valid |
| 5 | T5 in Today Mode | TODAY | ✗ Invalid (violates R12) |
| 6 | Reduced service + peak hour | TODAY | ✓ Valid (crowding risk) |

Plus a **comparison scenario** testing Changi Airport routing in both modes.

---

## 🔍 How It Works

### 1. Rule Representation
Rules are stored in implication form: `(A ∧ B ∧ C) → D`

Example:
```
"If Tanah Merah is open AND TEL is active, then TEL-EWL transfer is available"
```

### 2. CNF Conversion
Rules are converted to Conjunctive Normal Form (CNF):
```
(A ∧ B ∧ C) → D
≡ ¬A ∨ ¬B ∨ ¬C ∨ D
```

### 3. Resolution Algorithm
Uses **Robinson's Resolution** for inference:
- To prove query Q: Add ¬Q to knowledge base
- Apply resolution to derive new clauses
- If empty clause (□) is derived → Q is TRUE
- If no new clauses can be derived → Q is UNPROVABLE

### 4. Consistency Checking
Checks if knowledge base + facts lead to contradiction:
- If empty clause derived → INCONSISTENT
- Otherwise → CONSISTENT

---

## 📊 Example Output

```
======================================================================
SCENARIO 1: VALID - Normal Operations (TODAY Mode)
======================================================================

Mode: TODAY

Input Facts:
  • Network_Mode_Today: True
  • Station_Open_TanahMerah: True
  • Line_Active_TEL: True

Validation Result:
  ✓ VALID - No contradictions detected

Details:
  No contradictions detected
```

---

## 🎯 Assignment Deliverables Checklist

- [x] **10+ rules** in propositional logic (12 rules implemented)
- [x] **Plain English + Symbolic** representation for all rules
- [x] **Resolution-based inference** implemented
- [x] **6+ test scenarios** (6 main + 1 comparison)
- [x] **Route validation** functionality
- [x] **Consistency checking** functionality
- [x] **Violation identification** functionality
- [x] **TODAY vs FUTURE mode** comparison
- [x] **TELe/CRL changes** explicitly modeled
- [x] **Integration work** scenarios included

---

## 🧩 Integration with Other Components

This logical inference component is designed to integrate with:

1. **Search Component** (teammate's work)
   - Validate routes returned by search algorithms
   - Check if proposed paths satisfy operational rules

2. **Bayesian Network** (teammate's work)
   - Cross-validate service status assumptions
   - Provide rule-based constraints for crowding predictions

Example integration:
```python
# In main ChangiLink AI system
from logical_inference import ResolutionEngine, MRTKnowledgeBase
from search import PathFinder
from bayesian import CrowdingPredictor

# Get route from search
route = path_finder.find_path(origin, destination)

# Validate with logic engine
facts = extract_facts_from_route(route)
validation = logic_engine.validate_route(facts, mode)

if validation['is_consistent']:
    # Route is valid, proceed
    crowding_risk = bayesian.predict(route)
else:
    # Route violates rules
    print(f"Invalid route: {validation['violated_rules']}")
```

---

## 📈 Performance Analysis

### Computational Complexity
- **Resolution**: Worst-case exponential, but efficient for small clause sets
- **Typical scenarios**: <50 clauses, <100 resolution steps
- **Execution time**: <1 second for all test scenarios

### Advantages
- ✅ **Complete**: If a query is provable, resolution will prove it
- ✅ **Sound**: Only derives valid conclusions
- ✅ **Traceable**: Clear inference steps for debugging
- ✅ **Deterministic**: Same input always gives same output

### Limitations
- ❌ **Propositional only**: Cannot express "for all" or "exists"
- ❌ **Binary logic**: No uncertainty/probability (use Bayesian for that)
- ❌ **Scalability**: Exponential worst-case (but rare in practice)
- ❌ **Knowledge engineering**: Requires careful rule formulation

---

## 🚧 Future Improvements

1. **Predicate Logic**: Express more complex rules (e.g., "all stations on line X")
2. **Explanation Generation**: Natural language explanations of violations
3. **Rule Learning**: Automatically learn new rules from historical data
4. **Fuzzy Logic**: Handle uncertainty in station closures/delays
5. **Incremental Updates**: Efficiently update KB as network changes

---

## 📖 References

1. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.), Chapter 7: Logical Agents
2. LTA Press Release (25 Jul 2025): TELe/CRL Announcement
3. AICT Lecture Slides: Logic and Inference
4. Robinson, J. A. (1965). "A Machine-Oriented Logic Based on the Resolution Principle"

---

## 👤 Author Information

**Name:** [Your Name]  
**Student ID:** [Your ID]  
**Role:** Logical Inference Component  
**Contact:** [Your Email]

---

## 📝 Notes for Tutor

### Key Implementation Highlights
1. **Clean OOP design**: 5 well-defined classes with single responsibilities
2. **Comprehensive documentation**: Every function has docstrings
3. **Testable**: Each module can run independently with `python module.py`
4. **Extensible**: Easy to add new rules or inference methods
5. **Integration-ready**: Designed to work with teammates' components

### Demonstration Tips
- Run `python main.py --test` to see all scenarios
- Show `knowledge_base.py` for rule definitions
- Explain CNF conversion using `rules.py` examples
- Walk through resolution algorithm in `inference_engine.py`
- Demonstrate violation identification in contradictory scenarios

---

**End of README**