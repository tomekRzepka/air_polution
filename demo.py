import numpy as np
import scipy.stats as stats


def monte_carlo_stats(estimates):
    """
    Calculate the mean, standard deviation, and Monte Carlo error for a set of estimates
    using Monte Carlo simulation as described in the article.

    Parameters:
        estimates (array-like): An array of simulation results (θ̂ values).

    Returns:
        dict: A dictionary containing the mean, standard deviation, empirical standard error,
              and Monte Carlo error of the standard deviation.
    """
    nsim = len(estimates)

    if nsim < 2:
        raise ValueError("At least two simulation estimates are required to calculate statistics.")

    # Calculate the mean
    mean_estimate = np.mean(estimates)

    # Calculate the empirical standard deviation (EmpSÊ)
    empirical_std = np.std(estimates, ddof=1)  # Use ddof=1 for sample standard deviation

    # Monte Carlo error of EmpSÊ
    mc_error = empirical_std / np.sqrt(2 * (nsim - 1))

    return {
        "mean": mean_estimate,
        "standard_deviation": empirical_std,
        "monte_carlo_error": mc_error
    }


# Example usage
if __name__ == "__main__":
    # Example: Simulated estimates from Monte Carlo simulations
    simulated_estimates = np.random.normal(10, 2, size=1000)  # 1000 simulations with mean=10, std=2

    stats_result = monte_carlo_stats(simulated_estimates)

    print("Monte Carlo Simulation Results:")
    print(f"Mean: {stats_result['mean']:.4f}")
    print(f"Standard Deviation (EmpSÊ): {stats_result['standard_deviation']:.4f}")
    print(f"Monte Carlo Error of Std Dev: {stats_result['monte_carlo_error']:.4f}")


def std(numbers):
    n = len(numbers)
    mean_value = sum(numbers) / n
    variance = sum((x - mean_value) ** 2 for x in numbers) / n
    return variance ** 0.5