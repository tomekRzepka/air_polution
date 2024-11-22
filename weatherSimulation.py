import numpy as np
import matplotlib.pyplot as plt


def gaussian_dispersion_monte_carlo(num_simulations, wind_speed_range, temp_range, pressure_range, humidity_range,
                                    emission_rate, stack_height):
    """
    Simulate air pollutant dispersion using the Gaussian model and Monte Carlo sampling.

    Parameters:
        num_simulations (int): Number of Monte Carlo simulations.
        wind_speed_range (tuple): Min and max wind speed (m/s).
        temp_range (tuple): Min and max temperature (K).
        pressure_range (tuple): Min and max pressure (Pa).
        humidity_range (tuple): Min and max humidity (%) or rain (mm).
        emission_rate (float): Pollutant emission rate (g/s).
        stack_height (float): Stack height (meters).

    Returns:
        results (dict): Contains simulated concentrations and input distributions.
    """
    # Initialize results
    results = {"concentrations": [], "inputs": []}

    # Gaussian plume constants
    y = 0  # Assume centerline
    z = 0  # Ground-level concentration

    for _ in range(num_simulations):
        # Randomly sample inputs
        wind_speed = np.random.uniform(*wind_speed_range)
        temperature = np.random.uniform(*temp_range)
        pressure = np.random.uniform(*pressure_range)
        humidity = np.random.uniform(*humidity_range)

        # Effective stack height
        delta_h = 1.5 * (temperature / pressure)  # Simplified plume rise formula
        effective_height = stack_height + delta_h

        # Calculate dispersion coefficients (simplified linear approximation)
        sigma_y = 0.1 * effective_height
        sigma_z = 0.05 * effective_height

        # Downwind distance (assume fixed for demonstration)
        x = 1000  # meters

        # Gaussian concentration equation
        concentration = (emission_rate / (wind_speed * sigma_y * sigma_z * 2 * np.pi)) * \
                        np.exp(-y ** 2 / (2 * sigma_y ** 2)) * \
                        (np.exp(-((z - effective_height) ** 2) / (2 * sigma_z ** 2)) +
                         np.exp(-((z + effective_height) ** 2) / (2 * sigma_z ** 2)))

        # Store results
        results["concentrations"].append(concentration)
        results["inputs"].append({
            "wind_speed": wind_speed,
            "temperature": temperature,
            "pressure": pressure,
            "humidity": humidity,
            "effective_height": effective_height
        })

    return results


# Parameters for simulation
num_simulations = 1000
wind_speed_range = (2, 10)  # m/s
temp_range = (280, 310)  # K
pressure_range = (95000, 105000)  # Pa
humidity_range = (0, 100)  # %
emission_rate = 100  # g/s
stack_height = 50  # meters

# Run simulation
results = gaussian_dispersion_monte_carlo(num_simulations, wind_speed_range, temp_range, pressure_range, humidity_range,
                                          emission_rate, stack_height)

# Analyze results
concentrations = results["concentrations"]
inputs = results["inputs"]

# Plot results
plt.hist(concentrations, bins=30, color='skyblue', alpha=0.7)
plt.title("Distribution of Pollutant Concentrations (Monte Carlo)")
plt.xlabel("Concentration (g/m³)")
plt.ylabel("Frequency")
plt.show()

# Print sample results
print("Sample Inputs and Concentrations:")
for i in range(5):  # Print first 5 results
    print(f"Run {i + 1}: {inputs[i]} -> Concentration: {concentrations[i]:.3f} g/m³")
