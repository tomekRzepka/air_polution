import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

# Parameters for pollutants (mean and standard deviation estimated from the given data range)
pollutants = {
    'PM2.5': {'actual_value': 102, 'min': 64, 'max': 139},
    'PM10': {'actual_value': 53, 'min': 23, 'max': 58},
    'O3': {'actual_value': 3, 'min': 1, 'max': 15},
    'NO2': {'actual_value': 8, 'min': 6, 'max': 21},
}

# Number of Monte Carlo simulations
NUM_SIMULATIONS = 10000

# Initialize results dictionary for both 24 and 48 hours
simulation_results = {'24_hour': {}, '48_hour': {}}


# Function to calculate confidence interval
def confidence_interval(data, confidence=0.95):
    mean = np.mean(data)
    se = stats.sem(data)  # Standard error
    margin = se * stats.t.ppf((1 + confidence) / 2., len(data) - 1)
    return mean, mean - margin, mean + margin


# Monte Carlo simulation for each pollutant and each time period
for period in simulation_results.keys():
    multiplier = 1 if period == '24_hour' else 2  # Adjust for 48-hour period
    for pollutant, params in pollutants.items():
        min_val = params['min']
        max_val = params['max']
        actual_value = params['actual_value']

        # Estimate mean and std deviation from min and max for a normal distribution
        mean_val = (min_val + max_val) / 2
        std_dev = (max_val - min_val) / 4  # Approximation assuming 95% of data within 2 std dev

        # Simulate values for the given period
        simulated_values = np.random.normal(mean_val * multiplier, std_dev * np.sqrt(multiplier), NUM_SIMULATIONS)

        # Calculate confidence interval
        mean, lower_ci, upper_ci = confidence_interval(simulated_values)

        # Save results
        simulation_results[period][pollutant] = {
            'simulated_values': simulated_values,
            'mean': mean,
            'confidence_interval': (lower_ci, upper_ci),
            'actual_value': actual_value
        }

# Plotting the results for 24-hour and 48-hour simulations
plt.figure(figsize=(14, 12))
for idx, pollutant in enumerate(pollutants.keys()):
    # Plot for 24-hour period
    plt.subplot(4, 2, idx * 2 + 1)
    results_24 = simulation_results['24_hour'][pollutant]
    plt.hist(results_24['simulated_values'], bins=50, alpha=0.6, color='skyblue', density=True)
    plt.axvline(results_24['actual_value'], color='red', linestyle='--',
                label=f'Actual {pollutant} AQI = {results_24["actual_value"]}')
    lower_ci_24, upper_ci_24 = results_24['confidence_interval']
    plt.axvline(lower_ci_24, color='green', linestyle=':', label='95% Confidence Interval')
    plt.axvline(upper_ci_24, color='green', linestyle=':')
    plt.title(f'{pollutant} AQI Simulation (24-Hour)')
    plt.xlabel('Simulated AQI')
    plt.ylabel('Density')
    plt.legend()

    # Plot for 48-hour period
    plt.subplot(4, 2, idx * 2 + 2)
    results_48 = simulation_results['48_hour'][pollutant]
    plt.hist(results_48['simulated_values'], bins=50, alpha=0.6, color='lightcoral', density=True)
    plt.axvline(results_48['actual_value'], color='red', linestyle='--',
                label=f'Actual {pollutant} AQI = {results_48["actual_value"]}')
    lower_ci_48, upper_ci_48 = results_48['confidence_interval']
    plt.axvline(lower_ci_48, color='green', linestyle=':', label='95% Confidence Interval')
    plt.axvline(upper_ci_48, color='green', linestyle=':')
    plt.title(f'{pollutant} AQI Simulation (48-Hour)')
    plt.xlabel('Simulated AQI')
    plt.ylabel('Density')
    plt.legend()

plt.tight_layout()
plt.show()

# Print confidence intervals and deltas for both periods
for period, results in simulation_results.items():
    print(f"\n--- {period.replace('_', '-').title()} Simulation Results ---")
    for pollutant, stats in results.items():
        mean = stats['mean']
        lower_ci, upper_ci = stats['confidence_interval']
        delta = stats['actual_value'] - mean  # Delta between actual and simulated mean
        print(f"{pollutant} AQI ({period.replace('_', ' ')}):")
        print(f"  Mean simulated AQI: {mean:.2f}")
        print(f"  95% Confidence Interval: ({lower_ci:.2f}, {upper_ci:.2f})")
        print(f"  Actual AQI: {stats['actual_value']}")
        print(f"  Delta (Actual - Simulated Mean): {delta:.2f}")
        print()
