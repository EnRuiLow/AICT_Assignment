# ChangiLink AI - System Architecture

## System Overview

```
╔════════════════════════════════════════════════════════════════════════════╗
║                    CHANGILINK AI INTEGRATED SYSTEM                         ║
║                 Changi Airport Terminal 5 MRT Routing System               ║
╚════════════════════════════════════════════════════════════════════════════╝

                                    main.py
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
                    ▼                  ▼                  ▼
         ┌──────────────────┐ ┌──────────────┐ ┌─────────────────┐
         │  ROUTE PLANNING  │ │   LOGICAL    │ │    BAYESIAN     │
         │                  │ │  INFERENCE   │ │    NETWORK      │
         └──────────────────┘ └──────────────┘ └─────────────────┘
                  │                   │                   │
                  │                   │                   │
         ┌────────▼────────┐ ┌────────▼──────┐ ┌─────────▼────────┐
         │ Search Algos:   │ │ Resolution    │ │ Probabilistic    │
         │ • BFS           │ │ Engine        │ │ Reasoning        │
         │ • DFS           │ │               │ │                  │
         │ • Greedy BFS    │ │ Knowledge     │ │ Variables:       │
         │ • A*            │ │ Base          │ │ • Weather        │
         │                 │ │               │ │ • Time           │
         │ Output:         │ │ Output:       │ │ • Service Status │
         │ • Path          │ │ • Valid/      │ │                  │
         │ • Cost          │ │   Invalid     │ │ Output:          │
         │ • Transfers     │ │ • Violations  │ │ • Risk Level     │
         └─────────────────┘ └───────────────┘ └──────────────────┘
```

## Component Integration Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERACTION                             │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   MAIN MENU (main.py)  │
                    └────────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐      ┌──────────────────┐      ┌──────────────┐
│ ROUTE REQUEST │      │ VALIDATION       │      │ CROWDING     │
│               │      │ REQUEST          │      │ PREDICTION   │
└───────┬───────┘      └────────┬─────────┘      └──────┬───────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐      ┌──────────────────┐      ┌──────────────┐
│ Route Planning│      │ Logical Inference│      │ Bayesian Net │
│ Module        │      │ Module           │      │ Module       │
└───────┬───────┘      └────────┬─────────┘      └──────┬───────┘
        │                       │                       │
        └───────────────┬───────┴───────┬───────────────┘
                        │               │
                        ▼               ▼
                ┌────────────────────────────┐
                │ INTEGRATED RESULT DISPLAY  │
                └────────────────────────────┘
```

## Module Interconnections

```
                            ┌──────────────┐
                            │   Station    │
                            │     Data     │
                            └──────┬───────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
        ┌────────────────┐  ┌────────────┐  ┌──────────┐
        │ Graph Structure│  │ Rules for  │  │ Network  │
        │ (Stations &    │  │ Station    │  │ Context  │
        │  Connections)  │  │ Operations │  │          │
        └────────────────┘  └────────────┘  └──────────┘
                │                  │              │
                │                  │              │
        Network Mode         Network Mode    Network Mode
        (Today/Future)      (Today/Future)  (Today/Future)
```

## Data Flow Example: Complete Route Analysis

```
1. USER INPUT
   ┌────────────────────────────────────────┐
   │ From: Changi Airport                   │
   │ To: Marina Bay                         │
   │ Time: Morning, Weekday                 │
   │ Conditions: Rainy, Normal Service      │
   └────────────────────────────────────────┘
                     │
                     ▼
2. ROUTE PLANNING
   ┌────────────────────────────────────────┐
   │ A* Algorithm                           │
   │ Path: Changi Airport → Expo →          │
   │       Tanah Merah → Paya Lebar →       │
   │       Bugis → Promenade → Marina Bay   │
   │ Cost: 9.5, Transfers: 2                │
   └────────────────────────────────────────┘
                     │
                     ▼
3. LOGICAL VALIDATION
   ┌────────────────────────────────────────┐
   │ Facts:                                 │
   │ • Station_Open_Expo = true             │
   │ • Route_EWL_T5 = true                  │
   │ • Service_Normal_EWL = true            │
   │                                        │
   │ Result: ✓ VALID - No violations        │
   └────────────────────────────────────────┘
                     │
                     ▼
4. CROWDING PREDICTION
   ┌────────────────────────────────────────┐
   │ Evidence:                              │
   │ • Weather = Rainy                      │
   │ • Time = Morning                       │
   │ • Day = Weekday                        │
   │ • Service = Normal                     │
   │                                        │
   │ Result: Medium Risk (45%)              │
   │ Recommendation: Allow extra time       │
   └────────────────────────────────────────┘
                     │
                     ▼
5. INTEGRATED RECOMMENDATION
   ┌────────────────────────────────────────┐
   │ ✓ Route Available                      │
   │ ✓ Route Valid (no violations)          │
   │ ⚠ Moderate Crowding Expected           │
   │                                        │
   │ Advice: Route is good, but allow       │
   │         extra 10-15 min for crowds     │
   └────────────────────────────────────────┘
```

## Menu Structure

```
MAIN MENU
├── 1. Route Planning
│   ├── 1. BFS (Breadth-First Search)
│   ├── 2. DFS (Depth-First Search)
│   ├── 3. Greedy Best-First Search
│   ├── 4. A* Algorithm
│   ├── 5. Compare All Algorithms
│   ├── 6. Compare Today vs Future
│   ├── 7. View Available Stations
│   └── 8. Back to Main Menu
│
├── 2. Display Knowledge Base Rules
│   ├── 1. Display All Rules
│   ├── 2. Display TODAY Mode Rules
│   ├── 3. Display FUTURE Mode Rules
│   ├── 4. Display Specific Rule by ID
│   └── 5. Back to Main Menu
│
├── 3. Run Test Scenarios
│   ├── 1. Run All Test Scenarios
│   ├── 2. Run TODAY Mode Scenarios
│   ├── 3. Run FUTURE Mode Scenarios
│   └── 4. Back to Main Menu
│
├── 4. Custom Route Validation
│   └── [Interactive fact entry and validation]
│
├── 5. Crowding Risk Prediction
│   ├── 1. Interactive Crowding Prediction
│   ├── 2. Compare Today vs Future Mode
│   ├── 3. Scenario Analysis (Weather Impact)
│   ├── 4. Scenario Analysis (Time Impact)
│   ├── 5. View Network Structure
│   └── 6. Back to Main Menu
│
├── 6. Display Knowledge Base Summary
│
├── 7. About This System
│
└── 8. Exit
```

## Technical Architecture

### Component Technologies

```
┌─────────────────────────────────────────────────────────────┐
│                      ROUTE PLANNING                         │
├─────────────────────────────────────────────────────────────┤
│ • Language: Python                                          │
│ • Algorithms: BFS, DFS, Greedy BFS, A*                      │
│ • Data Structures: Graphs, Queues, Priority Queues          │
│ • Dependencies: math, collections, heapq                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   LOGICAL INFERENCE                         │
├─────────────────────────────────────────────────────────────┤
│ • Language: Python                                          │
│ • Method: Resolution Theorem Proving                        │
│ • Logic: Propositional Logic with CNF                       │
│ • Features: Rule validation, Consistency checking           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    BAYESIAN NETWORK                         │
├─────────────────────────────────────────────────────────────┤
│ • Language: Python                                          │
│ • Library: pgmpy (Probabilistic Graphical Models)           │
│ • Inference: Variable Elimination                           │
│ • Dependencies: pandas, numpy, matplotlib                   │
└─────────────────────────────────────────────────────────────┘
```

## Network Modes

```
┌─────────────────────────────────────────────────────────────┐
│                       TODAY MODE                            │
├─────────────────────────────────────────────────────────────┤
│ Current network configuration:                              │
│ • East-West Line (EWL) to Changi Airport                    │
│ • Existing Downtown Line (DTL)                              │
│ • Current Circle Line (CCL)                                 │
│ • Existing Thomson-East Coast Line (TECL)                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      FUTURE MODE                            │
├─────────────────────────────────────────────────────────────┤
│ Future network with Terminal 5 extensions:                  │
│ • Thomson-East Coast Line Extension (TELe) to T5            │
│ • Cross Island Line (CRL) to T5                             │
│ • Enhanced connectivity and capacity                        │
│ • Reduced crowding risk                                     │
└─────────────────────────────────────────────────────────────┘
```

## Key Features Summary

| Feature | Module | Input | Output |
|---------|--------|-------|--------|
| **Pathfinding** | Route Planning | Start, End stations | Path, Cost, Transfers |
| **Validation** | Logical Inference | Service facts | Valid/Invalid, Violations |
| **Risk Prediction** | Bayesian Network | Conditions | Probability distribution |
| **Comparison** | All Modules | Network mode | Today vs Future analysis |
| **Analysis** | All Modules | Various | Comprehensive insights |

## Usage Patterns

### Pattern 1: Route Discovery
```
User → Route Planning → Path Found → Display Results
```

### Pattern 2: Service Validation
```
User → Logical Inference → Facts Entry → Validation → Results
```

### Pattern 3: Risk Assessment
```
User → Bayesian Network → Conditions → Prediction → Recommendations
```

### Pattern 4: Comprehensive Analysis
```
User → Route Planning → Logical Inference → Bayesian Network → Integrated Result
```

---

## File Organization

```
AICT_Assignment/
│
├── main.py                           ← Integrated console (START HERE)
├── requirements.txt                  ← Dependencies
├── README.md                         ← General overview
├── README_INTEGRATED_CONSOLE.md      ← Detailed documentation
├── QUICK_START.md                    ← Quick start guide
├── SYSTEM_ARCHITECTURE.md            ← This file
│
├── route_planning/
│   ├── Route Planning with Search Algorithms.py
│   └── [supporting files]
│
├── logical_inference/
│   ├── __init__.py
│   ├── inference_engine.py
│   ├── knowledge_base.py
│   ├── models.py
│   ├── rules.py
│   ├── test_scenarios.py
│   └── [supporting files]
│
└── bayesian_network/
    ├── bayesian_network.py
    ├── demo_bayesian_network.py
    └── [supporting files]
```

---

**System Version 1.0 | February 2026 | AICT Assignment**
