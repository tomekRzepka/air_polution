import numpy as np
from scipy import stats

# Example simulation data (replace with your actual simulation results)
simulation_results = [102, 98, 105, 101, 100, 99, 103, 98, 97, 104]  # replace with actual simulation data

# Calculate the mean
mean_result = np.mean(simulation_results)

# Calculate the sample standard deviation
std_dev = np.std(simulation_results, ddof=1)  # ddof=1 for sample standard deviation

# Number of simulations
n = len(simulation_results)

# Calculate the standard error
standard_error = std_dev / np.sqrt(n)

# Confidence level
confidence = 0.95
t_critical = stats.t.ppf((1 + confidence) / 2, df=n-1)  # t critical value for 95% confidence

# Margin of error
margin_of_error = t_critical * standard_error

# Confidence interval
ci_lower = mean_result - margin_of_error
ci_upper = mean_result + margin_of_error

print(f"Mean: {mean_result}")
print(f"95% Confidence Interval: ({ci_lower}, {ci_upper})")
