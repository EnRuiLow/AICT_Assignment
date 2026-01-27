"""
Bayesian Network for Crowding Risk Prediction
Changi Airport Terminal 5 MRT Routing System

This module implements a Bayesian Network to predict crowding risk at MRT stations
in the Changi Airport-T5 corridor, supporting both Today Mode and Future Mode
(with TELe/CRL extensions as announced by LTA, July 2025).

Variables:
- Weather (W): Clear, Rainy, Thunderstorms
- Time of Day (T): Morning, Afternoon, Evening
- Day Type (D): Weekday, Weekend
- Network Mode (M): Today, Future
- Service Status (S): Normal, Reduced, Disrupted
- Demand Proxy (P): Low, Medium, High
- Crowding Risk (C): Low, Medium, High
"""

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


class CrowdingRiskBN:
    """Bayesian Network for predicting crowding risk in MRT stations."""
    
    def __init__(self):
        """Initialize the Bayesian Network structure."""
        self.model = None
        self.inference = None
        self.build_network()
        
    def build_network(self):
        """
        Build the Bayesian Network structure and define all CPDs.
        
        Network Structure:
        - Weather (W), Time of Day (T), Day Type (D), Network Mode (M) are root nodes
        - Service Status (S) depends on Weather
        - Demand Proxy (P) depends on Time, Day Type, and Network Mode
        - Crowding Risk (C) depends on Demand, Service Status, and Network Mode
        """
        # Define the network structure
        self.model = DiscreteBayesianNetwork([
            ('Weather', 'Service_Status'),
            ('Time_of_Day', 'Demand_Proxy'),
            ('Day_Type', 'Demand_Proxy'),
            ('Network_Mode', 'Demand_Proxy'),
            ('Demand_Proxy', 'Crowding_Risk'),
            ('Service_Status', 'Crowding_Risk'),
            ('Network_Mode', 'Crowding_Risk')
        ])
        
        # Define CPDs (Conditional Probability Distributions)
        self._define_cpds()
        
        # Add CPDs to model
        self.model.add_cpds(
            self.cpd_weather,
            self.cpd_time,
            self.cpd_day_type,
            self.cpd_network_mode,
            self.cpd_service_status,
            self.cpd_demand_proxy,
            self.cpd_crowding_risk
        )
        
        # Verify model
        assert self.model.check_model()
        
        # Create inference object
        self.inference = VariableElimination(self.model)
        
        print("Bayesian Network successfully constructed and validated!")
        
    def _define_cpds(self):
        """Define all Conditional Probability Distributions."""
        
        # CPD for Weather (W)
        # Clear: 60%, Rainy: 30%, Thunderstorms: 10%
        # Based on Singapore climate data (tropical, frequent rain)
        self.cpd_weather = TabularCPD(
            variable='Weather',
            variable_card=3,
            values=[[0.60],  # Clear
                    [0.30],  # Rainy
                    [0.10]], # Thunderstorms
            state_names={'Weather': ['Clear', 'Rainy', 'Thunderstorms']}
        )
        
        # CPD for Time of Day (T)
        # Morning: 33%, Afternoon: 33%, Evening: 34%
        self.cpd_time = TabularCPD(
            variable='Time_of_Day',
            variable_card=3,
            values=[[0.33],  # Morning
                    [0.33],  # Afternoon
                    [0.34]], # Evening
            state_names={'Time_of_Day': ['Morning', 'Afternoon', 'Evening']}
        )
        
        # CPD for Day Type (D)
        # Weekday: 71% (5/7), Weekend: 29% (2/7)
        self.cpd_day_type = TabularCPD(
            variable='Day_Type',
            variable_card=2,
            values=[[0.71],  # Weekday
                    [0.29]], # Weekend
            state_names={'Day_Type': ['Weekday', 'Weekend']}
        )
        
        # CPD for Network Mode (M)
        # Today: 100% (current), Future: 0% (for scenario testing)
        # This will be set as evidence during inference
        self.cpd_network_mode = TabularCPD(
            variable='Network_Mode',
            variable_card=2,
            values=[[0.50],  # Today
                    [0.50]], # Future
            state_names={'Network_Mode': ['Today', 'Future']}
        )
        
        # CPD for Service Status (S) given Weather (W)
        # Service is more likely disrupted during bad weather
        self.cpd_service_status = TabularCPD(
            variable='Service_Status',
            variable_card=3,
            values=[
                # Clear  Rainy  Thunderstorms
                [0.85,   0.70,  0.50],  # Normal
                [0.12,   0.20,  0.30],  # Reduced
                [0.03,   0.10,  0.20]   # Disrupted
            ],
            evidence=['Weather'],
            evidence_card=[3],
            state_names={
                'Service_Status': ['Normal', 'Reduced', 'Disrupted'],
                'Weather': ['Clear', 'Rainy', 'Thunderstorms']
            }
        )
        
        # CPD for Demand Proxy (P) given Time, Day Type, and Network Mode
        # Airport demand varies by time and day, with Future mode having better distribution
        # due to improved connectivity (TELe + CRL)
        # Columns: Time (3) x Day (2) x Mode (2) = 12 combinations
        self.cpd_demand_proxy = TabularCPD(
            variable='Demand_Proxy',
            variable_card=3,
            values=[
                # Time:      Morning      Afternoon     Evening
                # Day:     Wd    We    Wd    We    Wd    We
                # Mode:  T  F  T  F  T  F  T  F  T  F  T  F
                [0.15,0.25,0.35,0.45,0.20,0.30,0.30,0.40,0.10,0.20,0.25,0.35],  # Low
                [0.40,0.50,0.45,0.40,0.40,0.45,0.45,0.45,0.35,0.45,0.45,0.45],  # Medium
                [0.45,0.25,0.20,0.15,0.40,0.25,0.25,0.15,0.55,0.35,0.30,0.20]   # High
            ],
            evidence=['Time_of_Day', 'Day_Type', 'Network_Mode'],
            evidence_card=[3, 2, 2],
            state_names={
                'Demand_Proxy': ['Low', 'Medium', 'High'],
                'Time_of_Day': ['Morning', 'Afternoon', 'Evening'],
                'Day_Type': ['Weekday', 'Weekend'],
                'Network_Mode': ['Today', 'Future']
            }
        )
        
        # CPD for Crowding Risk (C) given Demand, Service Status, and Network Mode
        # Higher demand + worse service = higher crowding
        # Future mode has better distribution due to TELe+CRL reducing bottlenecks
        # Columns: Demand (3) x Service (3) x Mode (2) = 18 combinations
        self.cpd_crowding_risk = TabularCPD(
            variable='Crowding_Risk',
            variable_card=3,
            values=[
                # Demand:    Low          Medium         High
                # Service: N   R   D    N   R   D    N   R   D
                # Mode:   T F T F T F  T F T F T F  T F T F T F
                [0.80,0.85,0.60,0.70,0.40,0.50,0.50,0.60,0.30,0.40,0.15,0.25,0.25,0.35,0.10,0.20,0.05,0.10],  # Low
                [0.15,0.12,0.30,0.25,0.40,0.35,0.40,0.35,0.50,0.45,0.50,0.45,0.50,0.45,0.45,0.40,0.30,0.25],  # Medium
                [0.05,0.03,0.10,0.05,0.20,0.15,0.10,0.05,0.20,0.15,0.35,0.30,0.25,0.20,0.45,0.40,0.65,0.65]   # High
            ],
            evidence=['Demand_Proxy', 'Service_Status', 'Network_Mode'],
            evidence_card=[3, 3, 2],
            state_names={
                'Crowding_Risk': ['Low', 'Medium', 'High'],
                'Demand_Proxy': ['Low', 'Medium', 'High'],
                'Service_Status': ['Normal', 'Reduced', 'Disrupted'],
                'Network_Mode': ['Today', 'Future']
            }
        )
    
    def query(self, variables, evidence=None):
        """
        Perform inference on the Bayesian Network.
        
        Args:
            variables (list): List of variable names to query
            evidence (dict): Evidence dictionary, e.g., {'Weather': 'Rainy'}
            
        Returns:
            pandas.DataFrame: Probability distribution of queried variables
        """
        if evidence is None:
            evidence = {}
            
        result = self.inference.query(variables=variables, evidence=evidence)
        return result
    
    def predict_crowding(self, weather=None, time_of_day=None, day_type=None,
                        network_mode=None, service_status=None):
        """
        Predict crowding risk given specific conditions.
        
        Args:
            weather (str): 'Clear', 'Rainy', or 'Thunderstorms'
            time_of_day (str): 'Morning', 'Afternoon', or 'Evening'
            day_type (str): 'Weekday' or 'Weekend'
            network_mode (str): 'Today' or 'Future'
            service_status (str): 'Normal', 'Reduced', or 'Disrupted'
            
        Returns:
            dict: Probability distribution for Crowding_Risk
        """
        evidence = {}
        if weather:
            evidence['Weather'] = weather
        if time_of_day:
            evidence['Time_of_Day'] = time_of_day
        if day_type:
            evidence['Day_Type'] = day_type
        if network_mode:
            evidence['Network_Mode'] = network_mode
        if service_status:
            evidence['Service_Status'] = service_status
            
        result = self.query(['Crowding_Risk'], evidence)
        return result
    
    def get_network_info(self):
        """Get information about the network structure."""
        print("\n=== Bayesian Network Structure ===")
        print(f"Nodes: {self.model.nodes()}")
        print(f"Edges: {self.model.edges()}")
        print(f"\nParents of each node:")
        for node in self.model.nodes():
            parents = list(self.model.get_parents(node))
            print(f"  {node}: {parents if parents else 'None (root node)'}")
    
    def visualize_network(self, save_path=None):
        """
        Visualize the Bayesian Network structure.
        
        Args:
            save_path (str): Path to save the visualization image
        """
        try:
            import networkx as nx
            
            plt.figure(figsize=(14, 10))
            
            # Create layout
            pos = {
                'Weather': (0, 3),
                'Time_of_Day': (2, 3),
                'Day_Type': (4, 3),
                'Network_Mode': (6, 3),
                'Service_Status': (1, 2),
                'Demand_Proxy': (4, 2),
                'Crowding_Risk': (3, 1)
            }
            
            # Draw network
            nx.draw(self.model, pos, with_labels=True, node_color='lightblue',
                   node_size=3000, font_size=10, font_weight='bold',
                   arrows=True, arrowsize=20, edge_color='gray',
                   arrowstyle='->', connectionstyle='arc3,rad=0.1')
            
            plt.title('Bayesian Network for Crowding Risk Prediction\nChangi Airport Terminal 5 Corridor',
                     fontsize=14, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"Network visualization saved to {save_path}")
            
            plt.show()
            
        except ImportError:
            print("NetworkX is required for visualization. Install with: pip install networkx")


def run_scenarios():
    """Run all required inference scenarios and compare Today vs Future modes."""
    
    print("\n" + "="*80)
    print("CROWDING RISK PREDICTION - BAYESIAN NETWORK INFERENCE")
    print("Changi Airport Terminal 5 MRT Corridor")
    print("="*80)
    
    # Initialize the Bayesian Network
    bn = CrowdingRiskBN()
    
    # Define scenarios (at least 5, with at least 3 comparing Today vs Future)
    scenarios = [
        {
            'name': 'Scenario 1a: Rainy Evening + Reduced Service (Today Mode)',
            'evidence': {
                'Weather': 'Rainy',
                'Time_of_Day': 'Evening',
                'Network_Mode': 'Today',
                'Service_Status': 'Reduced'
            }
        },
        {
            'name': 'Scenario 1b: Rainy Evening + Reduced Service (Future Mode)',
            'evidence': {
                'Weather': 'Rainy',
                'Time_of_Day': 'Evening',
                'Network_Mode': 'Future',
                'Service_Status': 'Reduced'
            }
        },
        {
            'name': 'Scenario 2a: Clear Morning Weekday + Normal Service (Today Mode)',
            'evidence': {
                'Weather': 'Clear',
                'Time_of_Day': 'Morning',
                'Day_Type': 'Weekday',
                'Network_Mode': 'Today',
                'Service_Status': 'Normal'
            }
        },
        {
            'name': 'Scenario 2b: Clear Morning Weekday + Normal Service (Future Mode)',
            'evidence': {
                'Weather': 'Clear',
                'Time_of_Day': 'Morning',
                'Day_Type': 'Weekday',
                'Network_Mode': 'Future',
                'Service_Status': 'Normal'
            }
        },
        {
            'name': 'Scenario 3: Weekend Afternoon + Normal Service',
            'evidence': {
                'Time_of_Day': 'Afternoon',
                'Day_Type': 'Weekend',
                'Service_Status': 'Normal'
            }
        },
        {
            'name': 'Scenario 4: Disrupted Service Near Airport Corridor (Thunderstorms)',
            'evidence': {
                'Weather': 'Thunderstorms',
                'Service_Status': 'Disrupted',
                'Network_Mode': 'Today'
            }
        },
        {
            'name': 'Scenario 5a: Clear Evening + Normal Service (Today Mode)',
            'evidence': {
                'Weather': 'Clear',
                'Time_of_Day': 'Evening',
                'Network_Mode': 'Today',
                'Service_Status': 'Normal'
            }
        },
        {
            'name': 'Scenario 5b: Clear Evening + Normal Service (Future Mode)',
            'evidence': {
                'Weather': 'Clear',
                'Time_of_Day': 'Evening',
                'Network_Mode': 'Future',
                'Service_Status': 'Normal'
            }
        },
    ]
    
    results = []
    
    for scenario in scenarios:
        print(f"\n{'-'*80}")
        print(f"{scenario['name']}")
        print(f"{'-'*80}")
        print(f"Evidence: {scenario['evidence']}")
        
        # Query crowding risk
        result = bn.query(['Crowding_Risk'], scenario['evidence'])
        
        print(f"\nCrowding Risk Probability Distribution:")
        print(result)
        
        # Extract probabilities
        values = result.values
        states = result.state_names['Crowding_Risk']
        probs = {state: float(prob) for state, prob in zip(states, values)}
        
        # Determine most likely outcome
        max_state = max(probs, key=probs.get)
        max_prob = probs[max_state]
        
        print(f"\nMost Likely Crowding Risk: {max_state} ({max_prob:.2%})")
        
        # Store results for comparison
        results.append({
            'scenario': scenario['name'],
            'evidence': scenario['evidence'],
            'probabilities': probs,
            'prediction': max_state
        })
    
    # Comparative Analysis
    print("\n" + "="*80)
    print("COMPARATIVE ANALYSIS: TODAY MODE vs FUTURE MODE (TELe + CRL)")
    print("="*80)
    
    comparisons = [
        (0, 1, "Rainy Evening + Reduced Service"),
        (2, 3, "Clear Morning Weekday + Normal Service"),
        (6, 7, "Clear Evening + Normal Service")
    ]
    
    for idx1, idx2, desc in comparisons:
        print(f"\n{'-'*80}")
        print(f"Comparison: {desc}")
        print(f"{'-'*80}")
        
        today_result = results[idx1]
        future_result = results[idx2]
        
        print(f"\nToday Mode Probabilities:")
        for state in ['Low', 'Medium', 'High']:
            print(f"  {state}: {today_result['probabilities'][state]:.2%}")
        
        print(f"\nFuture Mode Probabilities:")
        for state in ['Low', 'Medium', 'High']:
            print(f"  {future_result['probabilities'][state]:.2%}")
        
        print(f"\nChange in Probabilities (Future - Today):")
        for state in ['Low', 'Medium', 'High']:
            change = future_result['probabilities'][state] - today_result['probabilities'][state]
            direction = "↑" if change > 0 else "↓" if change < 0 else "→"
            print(f"  {state}: {change:+.2%} {direction}")
        
        # Analysis
        print(f"\nAnalysis:")
        high_risk_today = today_result['probabilities']['High']
        high_risk_future = future_result['probabilities']['High']
        
        if high_risk_future < high_risk_today:
            improvement = high_risk_today - high_risk_future
            print(f"  Future mode shows {improvement:.2%} reduction in high crowding risk")
            print(f"  TELe + CRL extensions improve passenger distribution")
            print(f"  Additional interchange at T5 provides alternative routes")
        elif high_risk_future > high_risk_today:
            print(f"  Future mode shows increased crowding risk")
            print(f"  Possible factors: Systems integration works, service adjustments")
        else:
            print(f"  No significant change in crowding risk between modes")
    
    # Save results summary
    save_results_summary(results)
    
    return bn, results


def save_results_summary(results):
    """Save results summary to a CSV file."""
    
    data = []
    for r in results:
        row = {
            'Scenario': r['scenario'],
            'Prediction': r['prediction'],
            'Low_Prob': f"{r['probabilities']['Low']:.4f}",
            'Medium_Prob': f"{r['probabilities']['Medium']:.4f}",
            'High_Prob': f"{r['probabilities']['High']:.4f}",
        }
        # evidence
        for key, value in r['evidence'].items():
            row[key] = value
        data.append(row)
    
    df = pd.DataFrame(data)
    output_file = 'bayesian_network_results.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✓ Results summary saved to {output_file}")

if __name__ == "__main__":
    """Main execution."""
    
    print("Starting Bayesian Network for Crowding Risk Prediction...")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Run all scenarios
    bn, results = run_scenarios()
    
    # Get network information
    bn.get_network_info()
    
    # Visualize network (optional, requires networkx)
    try:
        bn.visualize_network(save_path='bayesian_network_structure.png')
    except Exception as e:
        print(f"\nVisualization skipped: {e}")
