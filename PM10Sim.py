import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import DataRepository as dr
import DataService as ds


# Fetch pollution data and default ranges
day=13
real_time_data, pm10_min, pm10_max = dr.getPM10Values(day)
hourly_data = dr.getHourlyPM10Values(day)
pollution_data = ds.forecastData(hourly_data)
if pollution_data is None:
    raise Exception("Unable to load PM10 data.")

# Number of Monte Carlo simulations per hour
NUM_SIMULATIONS = 10

# Initialize lists for plotting results
hours = []
simulated_means = []
lower_conf_intervals = []
upper_conf_intervals = []
actual_values = []


# Function to calculate confidence interval
def confidence_interval(data, confidence=0.95):
    # print(f"Data: {data}")
    mean = np.mean(data)
    print(f"MEAN: {mean}")
    se = stats.sem(data)  # Standard error
    print(f"Standard error: {se}")
    margin = se * stats.t.ppf((1 + confidence) / 2., len(data) - 1)
    return mean, mean - margin, mean + margin


# Monte Carlo simulation for each hour
counter = 0
for row in pollution_data:

    # Estimate mean and std deviation for normal distribution
    mean_by_real_value = np.mean(pollution_data)
    std_dev_by_real_value = np.std(pollution_data, ddof=1)

    # Run simulations for the current hour
    # simulated_values = np.random.normal(mean_val, std_dev, NUM_SIMULATIONS)
    simulated_values = np.random.normal(row, std_dev_by_real_value, NUM_SIMULATIONS)
    print(f"Row value: {row}")
    mean, lower_ci, upper_ci = confidence_interval(simulated_values)

    # Append results for plotting
    hours.append(counter)
    simulated_means.append(mean)
    Cavg = round(np.mean(simulated_means))
    Clow = round(min(simulated_means), 2)
    Chigh = round(max(simulated_means), 2)
    lower_conf_intervals.append(lower_ci)
    upper_conf_intervals.append(upper_ci)
    actual_values.append(real_time_data['pm10'][counter])
    counter += 1

print("______________________________________")
print("AIR QUALITY INDEX for SIMULATION")
print(f"Index mean:  {Cavg}")
print(f"Min sim: {Clow}")
print(f"Max sim: {Chigh}")

IhighEU = 0
IlowEU = 0
# CAQI - European Index table
match Cavg:
    case Cavg if Cavg <= 25:
        IhighEU = 25
        IlowEU = 0
    case Cavg if 26 <= Cavg <= 50:
        IhighEU = 50
        IlowEU = 25
    case Cavg if 50 < Cavg <= 90:
        IhighEU = 75
        IlowEU = 50
    case Cavg if 90 < Cavg <= 180:
        IhighEU = 100
        IlowEU = 75
IhighUS = 0
IlowUS = 0
match Cavg:
    case Cavg if Cavg <= 54:
        IhighUS = 50
        IlowUS = 0
    case Cavg if 54 < Cavg <= 154:
        IhighUS = 100
        IlowUS = 51
    case Cavg if 154 < Cavg <= 254:
        IhighUS = 150
        IlowUS = 101
    case Cavg if 254 < Cavg <= 354:
        IhighUS = 200
        IlowUS = 151
Sim_indexEU = ((IhighEU - IlowEU) / (Chigh - Clow)) * (Cavg - Clow) + IlowEU
Sim_indexUS = ((IhighUS - IlowUS) / (Chigh - Clow)) * (Cavg - Clow) + IlowUS

print(f"Simulation AQI EU :  {Sim_indexEU}")
print(f"Simulation AQI US :  {Sim_indexUS}")

print(f"Random points for simulation: {simulated_means}")
print(f"Standard deviation of source data: {std_dev_by_real_value}")
# Plotting
plt.figure(figsize=(12, 6))

# Plot the mean simulated values with confidence intervals as a shaded area
plt.plot(hours, simulated_means, color='blue', label="Mean Simulated PM10")
plt.scatter(hours, lower_conf_intervals, upper_conf_intervals, color='skyblue', alpha=0.3,
            label="conf_intervals_Lower")
plt.scatter(hours, upper_conf_intervals, color='black', alpha=0.3,
            label="conf_intervals_Upper")
# Plot the actual PM10 values as points
plt.plot(hours, actual_values, 'ro-', label="Actual PM10", markersize=5)
plt.plot(hours, pollution_data, color='brown', label="Simulated PM10 Core", markersize=5)
# Labels and Legend
plt.title("PM10 Simulation Over 24 Hours X10")
plt.xlabel("Hour")
plt.ylabel("PM10 Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Print summary of results
for hour, mean, ci, actual,forecast in zip(hours, simulated_means, zip(lower_conf_intervals, upper_conf_intervals),
                                  actual_values,pollution_data):
    print(f"\n--- Hour {hour} ---")
    print(f"Mean simulated PM10: {mean:.2f}")
    print(f"95% Confidence Interval: ({ci[0]:.2f}, {ci[1]:.2f})")
    print(f"Actual PM10: {actual}")
    print(f"Forecast PM10: {forecast}")
    print(f"Delta (Actual - Simulated Mean): {actual - mean:.2f}")
