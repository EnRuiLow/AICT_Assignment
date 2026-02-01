# ChangiLink AI - Integrated Console Application

## Overview

This integrated console application combines three AI components for the Changi Airport Terminal 5 MRT routing and advisory system:

1. **Route Planning with Search Algorithms** - BFS, DFS, Greedy BFS, A*
2. **Logical Inference Engine** - Resolution-based reasoning and validation
3. **Bayesian Network** - Crowding risk prediction

## Installation

### Prerequisites

- Python 3.8 or higher
- Required packages (install via requirements.txt):
  ```bash
  pip install -r requirements.txt
  ```

### Required Packages

The following packages are needed:
- pgmpy (for Bayesian Network)
- pandas
- matplotlib
- numpy

## Running the Application

### Interactive Mode (Recommended)

Simply run the main script to access the interactive menu:

```bash
python main.py
```

This will display the main menu with all available options:

```
================================================================================
  CHANGILINK AI - MAIN MENU
================================================================================

  ┌─ ROUTE PLANNING ──────────────────────────────────────────────┐
  │ 1. Route Planning with Search Algorithms                      │
  └───────────────────────────────────────────────────────────────┘

  ┌─ LOGICAL INFERENCE ────────────────────────────────────────────┐
  │ 2. Display Knowledge Base Rules                               │
  │ 3. Run Test Scenarios                                         │
  │ 4. Custom Route Validation                                    │
  └───────────────────────────────────────────────────────────────┘

  ┌─ BAYESIAN NETWORK ─────────────────────────────────────────────┐
  │ 5. Crowding Risk Prediction                                   │
  └───────────────────────────────────────────────────────────────┘

  ┌─ SYSTEM ───────────────────────────────────────────────────────┐
  │ 6. Display Knowledge Base Summary                             │
  │ 7. About This System                                          │
  │ 8. Exit                                                       │
  └───────────────────────────────────────────────────────────────┘
```

## Features

### 1. Route Planning with Search Algorithms

Find optimal routes between MRT stations using various search algorithms:

- **BFS (Breadth-First Search)** - Explores level by level, guarantees shortest path
- **DFS (Depth-First Search)** - Explores depth-first, memory efficient
- **Greedy Best-First Search** - Uses heuristic for faster search
- **A\* Algorithm** - Optimal pathfinding with heuristic and cost

**Features:**
- Compare all algorithms side-by-side
- Today vs Future network mode comparison
- View all available stations
- Calculate transfers and costs

**Example Usage:**
```
Enter choice (1-8): 1
Enter start station: Changi Airport
Enter destination station: Marina Bay
```

### 2. Logical Inference Engine

Validate service advisories and route decisions using resolution-based logical inference.

**Features:**
- Display operational rules (all, TODAY mode, FUTURE mode)
- Run predefined test scenarios
- Custom route validation with user-defined facts
- Identify rule violations and inconsistencies

**Example Custom Validation:**
```
Enter choice (1-8): 4

Select Network Mode:
1. TODAY (Current EWL airport branch)
2. FUTURE (TELe/CRL extensions)
Enter choice (1-2): 1

Enter facts (proposition_name=true/false)
Example: Station_Open_Expo=true
Fact: Station_Open_Expo=true
Fact: Route_EWL_T5=true
Fact: done
```

### 3. Bayesian Network - Crowding Risk Prediction

Predict crowding risk at MRT stations based on multiple factors.

**Variables Considered:**
- Weather (Clear, Rainy, Thunderstorms)
- Time of Day (Morning, Afternoon, Evening)
- Day Type (Weekday, Weekend)
- Network Mode (Today, Future)
- Service Status (Normal, Reduced, Disrupted)

**Features:**
- Interactive prediction with custom inputs
- Today vs Future mode comparison
- Weather impact analysis
- Time of day impact analysis
- View network structure and dependencies

**Example Usage:**
```
Enter choice (1-8): 5

Enter conditions (press Enter to skip any field):

Weather (Clear/Rainy/Thunderstorms): Rainy
Time of Day (Morning/Afternoon/Evening): Morning
Day Type (Weekday/Weekend): Weekday
Network Mode (Today/Future): Today
Service Status (Normal/Reduced/Disrupted): Normal
```

**Sample Output:**
```
Crowding Risk Probability Distribution:
  Low     :  25.00% ████████████
  Medium  :  45.00% ██████████████████████
  High    :  30.00% ███████████████

→ Most Likely Crowding Risk: Medium (45.00%)

Recommendations:
  ⚠ MODERATE CROWDING - Plan for potential delays
    • Allow extra travel time
    • Stay alert for service announcements
```

## Available Stations

The system includes the following MRT stations:

**East-West Line (EWL):**
- Changi Airport, Expo, Tanah Merah, Simei, Tampines
- Paya Lebar, Bugis, Lavender, Kallang, Aljunied
- Eunos, Kembangan, Bedok

**Downtown Line (DTL):**
- Upper Changi, Tampines East, Bugis

**North-South Line (NSL):**
- City Hall, Orchard, Bishan, Braddell, Toa Payoh
- Novena, Newton, Somerset, Dhoby Ghaut, Raffles Place

**Circle Line (CCL):**
- Bishan, Serangoon, Bartley, Tai Seng, MacPherson
- Dakota, Mountbatten, Stadium, Nicoll Highway
- Promenade, Bayfront

**Thomson-East Coast Line (TECL):**
- Marina Bay, Gardens by the Bay, Raffles Place

## Command-Line Options

For automated testing and specific operations:

```bash
# Display help
python main.py --help

# Run all logical inference test scenarios
python main.py --test

# Run TODAY mode scenarios only
python main.py --test-today

# Run FUTURE mode scenarios only
python main.py --test-future

# Display all rules
python main.py --display-rules

# Run custom validation
python main.py --custom
```

## File Structure

```
AICT_Assignment/
├── main.py                          # Integrated console application
├── requirements.txt                 # Python dependencies
├── README.md                        # General README
├── README_INTEGRATED_CONSOLE.md     # This file
│
├── route_planning/
│   ├── Route Planning with Search Algorithms.py
│   └── README.md
│
├── logical_inference/
│   ├── __init__.py
│   ├── inference_engine.py
│   ├── knowledge_base.py
│   ├── models.py
│   ├── rules.py
│   ├── test_scenarios.py
│   └── COMPLETE_WALKTHROUGH.md
│
└── bayesian_network/
    ├── bayesian_network.py
    ├── demo_bayesian_network.py
    ├── bayesian_network_results.csv
    └── README_BayesianNetwork.md
```

## Troubleshooting

### Import Errors

If you encounter import errors:
1. Ensure all required packages are installed: `pip install -r requirements.txt`
2. Check that Python 3.8+ is installed: `python --version`
3. Verify you're in the correct directory

### Module Not Found

If modules are not found:
1. The application automatically adds subdirectories to the Python path
2. Ensure the directory structure matches the layout above
3. Run from the main `AICT_Assignment` directory

### Bayesian Network Not Loading

If the Bayesian Network module fails to load:
1. Ensure pgmpy is installed: `pip install pgmpy`
2. Check pandas and numpy are installed
3. Try running the standalone demo: `python bayesian_network/demo_bayesian_network.py`

## Tips for Best Results

### Route Planning
- Use A* for optimal routes with transfer considerations
- Compare algorithms to see different search strategies
- Check Today vs Future mode for network improvements

### Logical Inference
- Start with predefined test scenarios to understand the system
- Review rules before custom validation
- Enter facts carefully (exact proposition names required)

### Bayesian Network
- Leave fields blank to see marginal probabilities
- Compare scenarios to understand factor impacts
- Use Today vs Future comparison to see network benefits

## System Integration

The three components work together to provide comprehensive MRT routing intelligence:

1. **Route Planning** finds the optimal physical path
2. **Logical Inference** validates the route against operational rules
3. **Bayesian Network** predicts crowding conditions along the route

For complete route intelligence, use all three components:
1. Find route with Route Planning (Option 1)
2. Validate route with Logical Inference (Option 4)
3. Check crowding risk with Bayesian Network (Option 5)

## Support

For questions or issues:
- Review the individual component README files
- Check the COMPLETE_WALKTHROUGH.md in logical_inference/
- Verify all dependencies are installed

## Version Information

- System Version: 1.0
- Date: February 2026
- Assignment: AICT Assignment - AI Techniques in Computing

---

**Developed for Changi Airport Terminal 5 MRT Routing System**
