import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import requests

# API endpoint and token
url = "https://api.waqi.info/feed/here/?token=853cea3387dc974cf970e30ae0e64ba50e3dface"

file_path = "pm10pomiary.csv"
# Function to prepare pollution data
def preparePolutionData(iaqi):
    # Default min and max values for PM10
    default_ranges = {
        'PM10': {'min': 7.1, 'max': 25.2}
    }

    pollutants = {}

    # Load PM10 data from CSV file
    try:
        # Read data from the CSV file
        data = pd.read_csv(file_path, usecols=['Date', 'PM10'], parse_dates=['Date'])

        # Get the latest PM10 value (assuming data is in chronological order)
        latest_pm10_value = data['PM10'].iloc[-1]

        # Set up pollutant data for PM10
        min_val = default_ranges['PM10']['min']
        max_val = default_ranges['PM10']['max']

        pollutants['PM10'] = {
            "actual_value": latest_pm10_value,
            "min": min_val,
            "max": max_val
        }

        print("Pollutant data successfully retrieved from CSV.")

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty.")
    except KeyError:
        print("Error: CSV file does not contain 'PM10' column.")

    return pollutants


# Fetch data from the API
response = requests.get(url)
data = response.json()

# Check if the response is valid
if data["status"] == "ok":
    print("Pollution data: " , data)
    iaqi = data["data"]["iaqi"]
    # Populate pollutants dictionary with actual values from API response
    pollutants = preparePolutionData(iaqi)
    print("Pollutant data successfully retrieved:")
    print(pollutants)
else:
    print("Failed to retrieve data from API:", data["status"])

# Number of Monte Carlo simulations
NUM_SIMULATIONS = 10

# Toggle for showing real data
SHOW_REAL_DATA = False

# Generate example real data (for visualization only)
real_data_samples = {
    'PM2.5': np.random.normal(102, 10, 50),
    'PM10': np.random.normal(53, 5, 50),
    'NO2': np.random.normal(8, 2, 50)
}

# Initialize results dictionary for 24 hours
simulation_results = {'24_hour': {}}


# Function to calculate confidence interval
def confidence_interval(data, confidence=0.95):
    mean = np.mean(data)
    se = stats.sem(data)  # Standard error
    margin = se * stats.t.ppf((1 + confidence) / 2., len(data) - 1)
    return mean, mean - margin, mean + margin


# Monte Carlo simulation for each pollutant over 24 hours
for pollutant, params in pollutants.items():
    min_val = params['min']
    max_val = params['max']
    actual_value = params['actual_value']

    # Estimate mean and std deviation for normal distribution
    mean_val = (min_val + max_val) / 2
    std_dev = (max_val - min_val) / 4

    # Run simulation and record mean and confidence interval
    hourly_means = []
    hourly_confidence_intervals = []

    for hour in range(1, 25):  # Simulate for each hour
        simulated_values = np.random.normal(mean_val, std_dev, NUM_SIMULATIONS)
        mean, lower_ci, upper_ci = confidence_interval(simulated_values)
        hourly_means.append(mean)
        hourly_confidence_intervals.append((lower_ci, upper_ci))

    # Store results for plotting
    simulation_results['24_hour'][pollutant] = {
        'hourly_means': hourly_means,
        'hourly_confidence_intervals': hourly_confidence_intervals,
        'actual_value': actual_value
    }

# Plot hourly simulation results
plt.figure(figsize=(14, 10))

for idx, pollutant in enumerate(pollutants.keys()):
    results_24 = simulation_results['24_hour'][pollutant]
    hours = list(range(1, 25))
    means = results_24['hourly_means']
    lower_cis = [ci[0] for ci in results_24['hourly_confidence_intervals']]
    upper_cis = [ci[1] for ci in results_24['hourly_confidence_intervals']]

    plt.subplot(5, 1, idx + 1)
    plt.plot(hours, means, color='skyblue', label=f"Simulated Mean {pollutant} AQI")
    plt.fill_between(hours, lower_cis, upper_cis, color='skyblue', alpha=0.2, label="95% Confidence Interval")
    plt.axhline(results_24['actual_value'], color='red', linestyle='--',
                label=f'Actual {pollutant} AQI = {results_24["actual_value"]}')
    plt.title(f'{pollutant} AQI Simulation Over 24 Hours')
    plt.xlabel('Hour')
    plt.ylabel('Simulated AQI')
    plt.legend()

plt.tight_layout()
plt.show()

# Print confidence intervals and deltas for each pollutant
for pollutant, stats in simulation_results['24_hour'].items():
    actual_value = stats['actual_value']
    print(f"\n--- {pollutant} AQI (24-Hour Simulation) ---")
    for hour, (mean, ci) in enumerate(zip(stats['hourly_means'], stats['hourly_confidence_intervals']), start=1):
        delta = actual_value - mean  # Delta between actual and simulated mean
        print(f"Hour {hour}:")
        print(f"  Mean simulated AQI: {mean:.2f}")
        print(f"  95% Confidence Interval: ({ci[0]:.2f}, {ci[1]:.2f})")
        print(f"  Delta (Actual - Simulated Mean): {delta:.2f}")
