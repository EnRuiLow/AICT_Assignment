"""
Interactive Demo for Bayesian Network - Crowding Risk Prediction
This script provides a simple interactive interface to query the Bayesian Network
"""

from bayesian_network import CrowdingRiskBN
import pandas as pd


def print_header():
    """Print demo header."""
    print("=" * 80)
    print("CHANGILINK AI - BAYESIAN NETWORK DEMO")
    print("Crowding Risk Prediction for Changi Airport Terminal 5 Corridor")
    print("=" * 80)
    print()


def interactive_query():
    """Run interactive query interface."""
    print("\n--- Interactive Crowding Risk Prediction ---\n")
    
    # Initialize BN
    bn = CrowdingRiskBN()
    
    # Get user inputs
    print("Enter conditions (press Enter to skip any field):\n")
    
    weather = input("Weather (Clear/Rainy/Thunderstorms): ").strip()
    if weather and weather not in ['Clear', 'Rainy', 'Thunderstorms']:
        print(f"Invalid weather. Using default.")
        weather = None
    
    time_of_day = input("Time of Day (Morning/Afternoon/Evening): ").strip()
    if time_of_day and time_of_day not in ['Morning', 'Afternoon', 'Evening']:
        print(f"Invalid time. Using default.")
        time_of_day = None
    
    day_type = input("Day Type (Weekday/Weekend): ").strip()
    if day_type and day_type not in ['Weekday', 'Weekend']:
        print(f"Invalid day type. Using default.")
        day_type = None
    
    network_mode = input("Network Mode (Today/Future): ").strip()
    if network_mode and network_mode not in ['Today', 'Future']:
        print(f"Invalid network mode. Using default.")
        network_mode = None
    
    service_status = input("Service Status (Normal/Reduced/Disrupted): ").strip()
    if service_status and service_status not in ['Normal', 'Reduced', 'Disrupted']:
        print(f"Invalid service status. Using default.")
        service_status = None
    
    # Perform prediction
    print("\n" + "-" * 80)
    print("PREDICTION RESULTS")
    print("-" * 80)
    
    result = bn.predict_crowding(
        weather=weather if weather else None,
        time_of_day=time_of_day if time_of_day else None,
        day_type=day_type if day_type else None,
        network_mode=network_mode if network_mode else None,
        service_status=service_status if service_status else None
    )
    
    print("\nCrowding Risk Probability Distribution:")
    print(result)
    
    # Extract and display probabilities
    values = result.values
    states = result.state_names['Crowding_Risk']
    probs = {state: float(prob) for state, prob in zip(states, values)}
    
    print("\nSummary:")
    for state in ['Low', 'Medium', 'High']:
        prob = probs[state]
        bar = '█' * int(prob * 50)
        print(f"  {state:8s}: {prob:6.2%} {bar}")
    
    max_state = max(probs, key=probs.get)
    print(f"\n→ Most Likely Crowding Risk: {max_state} ({probs[max_state]:.2%})")
    
    # Recommendations
    print("\nRecommendations:")
    if probs['High'] > 0.5:
        print("HIGH CROWDING RISK - Consider alternative routes or timing")
        print("  • Use less crowded stations for interchange")
        print("  • Travel during off-peak hours if possible")
    elif probs['Medium'] > 0.5:
        print("MODERATE CROWDING - Plan for potential delays")
        print("  • Allow extra travel time")
        print("  • Stay alert for service announcements")
    else:
        print(" LOW CROWDING RISK - Normal travel conditions expected")


def compare_modes():
    """Compare Today vs Future mode for same conditions."""
    print("\n--- Today vs Future Mode Comparison ---\n")
    
    # Initialize BN
    bn = CrowdingRiskBN()
    
    print("Enter scenario conditions:\n")
    
    weather = input("Weather (Clear/Rainy/Thunderstorms) [Clear]: ").strip() or "Clear"
    time_of_day = input("Time of Day (Morning/Afternoon/Evening) [Evening]: ").strip() or "Evening"
    day_type = input("Day Type (Weekday/Weekend) [Weekday]: ").strip() or "Weekday"
    service_status = input("Service Status (Normal/Reduced/Disrupted) [Normal]: ").strip() or "Normal"
    
    print("\n" + "-" * 80)
    print("COMPARISON: TODAY MODE vs FUTURE MODE (TELe + CRL)")
    print("-" * 80)
    
    # Query Today mode
    result_today = bn.predict_crowding(
        weather=weather,
        time_of_day=time_of_day,
        day_type=day_type,
        network_mode='Today',
        service_status=service_status
    )
    
    # Query Future mode
    result_future = bn.predict_crowding(
        weather=weather,
        time_of_day=time_of_day,
        day_type=day_type,
        network_mode='Future',
        service_status=service_status
    )
    
    # Extract probabilities
    probs_today = {state: float(prob) for state, prob in 
                   zip(result_today.state_names['Crowding_Risk'], result_today.values)}
    probs_future = {state: float(prob) for state, prob in 
                    zip(result_future.state_names['Crowding_Risk'], result_future.values)}
    
    # Display comparison
    print(f"\nConditions: {weather}, {time_of_day}, {day_type}, {service_status}\n")
    
    print("TODAY MODE (Current Network):")
    for state in ['Low', 'Medium', 'High']:
        prob = probs_today[state]
        bar = '█' * int(prob * 40)
        print(f"  {state:8s}: {prob:6.2%} {bar}")
    
    print("\nFUTURE MODE (TELe + CRL):")
    for state in ['Low', 'Medium', 'High']:
        prob = probs_future[state]
        bar = '█' * int(prob * 40)
        print(f"  {state:8s}: {prob:6.2%} {bar}")
    
    print("\nChange (Future - Today):")
    for state in ['Low', 'Medium', 'High']:
        change = probs_future[state] - probs_today[state]
        direction = "↑" if change > 0 else "↓" if change < 0 else "→"
        print(f"  {state:8s}: {change:+6.2%} {direction}")
    
    # Analysis
    print("\nAnalysis:")
    if probs_future['High'] < probs_today['High']:
        improvement = probs_today['High'] - probs_future['High']
        print(f"  Future mode reduces high crowding risk by {improvement:.2%}")
        print(f"  • TELe provides alternative route from Sungei Bedok to Tanah Merah")
        print(f"  • CRL extension to T5 reduces load on existing lines")
        print(f"  • New T5 interchange (TE32/CR1) improves connectivity")
    elif probs_future['High'] > probs_today['High']:
        print(f"  Future mode shows increased crowding risk")
        print(f"  • May be affected by systems integration works")
        print(f"  • Service adjustments during construction phase")
    else:
        print(f"  → Similar crowding risk in both modes for these conditions")


def batch_scenarios():
    """Run predefined batch scenarios."""
    print("\n--- Batch Scenario Analysis ---\n")
    
    bn = CrowdingRiskBN()
    
    scenarios = [
        ("Clear Morning Weekday, Normal", "Clear", "Morning", "Weekday", "Normal"),
        ("Rainy Evening Weekday, Reduced", "Rainy", "Evening", "Weekday", "Reduced"),
        ("Thunderstorms Any Time, Disrupted", "Thunderstorms", "Afternoon", "Weekday", "Disrupted"),
        ("Clear Weekend Afternoon, Normal", "Clear", "Afternoon", "Weekend", "Normal"),
    ]
    
    results = []
    
    for name, weather, time, day, service in scenarios:
        for mode in ['Today', 'Future']:
            result = bn.predict_crowding(
                weather=weather,
                time_of_day=time,
                day_type=day,
                network_mode=mode,
                service_status=service
            )
            
            probs = {state: float(prob) for state, prob in 
                    zip(result.state_names['Crowding_Risk'], result.values)}
            
            results.append({
                'Scenario': name,
                'Mode': mode,
                'Low': probs['Low'],
                'Medium': probs['Medium'],
                'High': probs['High'],
                'Prediction': max(probs, key=probs.get)
            })
    
    df = pd.DataFrame(results)
    print(df.to_string(index=False))
    print(" Batch analysis complete")


def main():
    """Main demo menu."""
    print_header()
    
    while True:
        print("\n" + "=" * 80)
        print("MENU")
        print("=" * 80)
        print("1. Interactive Query - Predict crowding risk")
        print("2. Compare Today vs Future Mode")
        print("3. Run Batch Scenarios")
        print("4. View Network Structure")
        print("5. Exit")
        print()
        
        choice = input("Select option (1-5): ").strip()
        
        if choice == '1':
            interactive_query()
        elif choice == '2':
            compare_modes()
        elif choice == '3':
            batch_scenarios()
        elif choice == '4':
            bn = CrowdingRiskBN()
            bn.get_network_info()
            try:
                bn.visualize_network()
            except Exception as e:
                print(f"Visualization error: {e}")
        elif choice == '5':
            print("\nThank you for using ChangiLink AI Bayesian Network Demo!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
