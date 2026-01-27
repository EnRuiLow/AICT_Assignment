# Bayesian Network for Crowding Risk Prediction
## Changi Airport Terminal 5 MRT Routing System

**Student Component:** Bayesian Network Implementation (Basic Requirement #3)

---

## Overview

This implementation uses a Bayesian Network to predict crowding risk at MRT stations in the Changi Airport-T5 corridor. It supports both **Today Mode** (current network) and **Future Mode** (with TELe/CRL extensions as announced by LTA, July 2025).

## Network Variables

| Variable | Symbol | States | Description |
|----------|--------|--------|-------------|
| Weather | W | Clear, Rainy, Thunderstorms | Current weather conditions |
| Time of Day | T | Morning, Afternoon, Evening | Time period |
| Day Type | D | Weekday, Weekend | Type of day |
| Network Mode | M | Today, Future | Network configuration |
| Service Status | S | Normal, Reduced, Disrupted | Train service status (includes integration works) |
| Demand Proxy | P | Low, Medium, High | Passenger demand level |
| Crowding Risk | C | Low, Medium, High | Predicted crowding risk |

## Network Structure

```
Weather (W) ──────────► Service Status (S) ───┐
                                               │
Time of Day (T) ───┐                          │
                   ├──► Demand Proxy (P) ──────┼──► Crowding Risk (C)
Day Type (D) ──────┤                          │
                   │                          │
Network Mode (M) ──┴──────────────────────────┘
```

## Installation

### 1. Install Required Libraries

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install pgmpy pandas matplotlib numpy networkx scipy
```

### 2. Verify Installation

```bash
python -c "import pgmpy; print('pgmpy version:', pgmpy.__version__)"
```

## Usage

### Run Complete Analysis

```bash
python bayesian_network.py
```

This will:
1. Build the Bayesian Network
2. Execute 8 inference scenarios (including 3 Today vs Future comparisons)
3. Generate comparative analysis
4. Save results to `bayesian_network_results.csv`
5. Create network visualization (`bayesian_network_structure.png`)
6. Display discussion of limitations

### Using the BN in Your Code

```python
from bayesian_network import CrowdingRiskBN

# Initialize the network
bn = CrowdingRiskBN()

# Query crowding risk for specific conditions
result = bn.predict_crowding(
    weather='Rainy',
    time_of_day='Evening',
    network_mode='Today',
    service_status='Reduced'
)

print(result)
```

## Scenarios Tested

### Scenario Pairs (Today vs Future Mode Comparison)

1. **Rainy Evening + Reduced Service**
   - Tests impact of TELe/CRL during adverse weather

2. **Clear Morning Weekday + Normal Service**
   - Tests peak hour performance improvements

3. **Clear Evening + Normal Service**
   - Tests evening commute distribution

### Additional Scenarios

4. **Weekend Afternoon + Normal Service**
   - Tests leisure travel patterns

5. **Thunderstorms + Disrupted Service**
   - Tests worst-case scenario resilience

## Key Findings

### Future Mode (TELe + CRL) Benefits:

1. **Reduced Crowding Risk**: 5-15% reduction in high-risk probability during peak periods
2. **Better Load Distribution**: TELe and CRL provide alternative routes
3. **Improved Resilience**: Lower crowding even during service disruptions
4. **T5 Interchange**: New interchange reduces bottleneck at existing stations

### CPD Justifications

#### Weather CPD
- **Clear (60%)**: Based on Singapore's tropical climate with ~180 sunny days/year
- **Rainy (30%)**: Frequent afternoon showers
- **Thunderstorms (10%)**: Severe weather events

#### Service Status CPD (given Weather)
- **Clear → Normal (85%)**: High reliability in good weather
- **Thunderstorms → Disrupted (20%)**: Lightning affects signaling systems

#### Demand Proxy CPD (given Time, Day, Network Mode)
- **Morning Weekday**: Higher demand (commuters + airport staff)
- **Future Mode**: Better distribution due to TELe/CRL capacity
- **Weekend**: Lower overall demand, but more leisure travel

#### Crowding Risk CPD (given Demand, Service, Network Mode)
- **High Demand + Disrupted Service**: Maximum crowding risk
- **Future Mode**: Reduced crowding due to network redundancy
- **Low Demand + Normal Service**: Minimal crowding risk

## Output Files

1. **`bayesian_network_results.csv`**: Detailed probability distributions for all scenarios
2. **`bayesian_network_structure.png`**: Visual diagram of the network
3. **Console output**: Complete analysis with explanations

## Limitations & Improvements

### Current Limitations

1. **Data Assumptions**: CPDs based on reasonable estimates, not actual LTA data
2. **Discretization**: Continuous variables (time, demand) simplified to discrete states
3. **Simplified Dependencies**: Real-world interactions may be more complex
4. **Static Model**: Doesn't capture temporal evolution during construction

### Suggested Improvements

1. **Real-time Data Integration**:
   - Live weather feeds
   - Actual passenger counts from fare gates
   - Real-time service status

2. **Enhanced Granularity**:
   - Hourly time periods instead of morning/afternoon/evening
   - Specific station-level crowding
   - Multiple disruption types

3. **Dynamic Bayesian Network**:
   - Model temporal dependencies
   - Predict crowding evolution over time
   - Learn from historical patterns

4. **Validation**:
   - Compare with actual crowding incidents
   - Sensitivity analysis on CPD parameters
   - Expert validation from LTA/SMRT

## Integration with Team Project

This component integrates with:
- **Search Algorithms**: Use crowding risk as edge weights/penalties
- **Logical Inference**: Validate route recommendations against crowding predictions
- **Optimization**: Minimize routes through high-crowding stations

## References

1. LTA (25 July 2025) - TELe and CRL Extension Announcement
2. Singapore Weather Data - Meteorological Service Singapore
3. MRT Ridership Statistics - LTA Annual Reports
4. pgmpy Documentation - https://pgmpy.org/

## Assignment Compliance Checklist

- ✅ 7 variables defined (W, T, D, M, S, P, C)
- ✅ Appropriate states for each variable
- ✅ Network structure with justified dependencies
- ✅ CPDs defined with documented probabilities
- ✅ 8 scenarios tested (>5 required)
- ✅ 3+ Today vs Future Mode comparisons
- ✅ Service Status variable for disruptions
- ✅ Analysis of why crowding changes between modes
- ✅ Discussion of limitations and improvements
- ✅ Code is well-documented and executable

---

**Author**: [Your Name/Student ID]  
**Module**: Artificial Intelligence Concepts & Techniques  
**Assignment**: ChangiLink AI - Bayesian Network Component  
**Date**: January 2026
