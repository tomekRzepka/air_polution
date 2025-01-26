import pandas as pd
import numpy as np
import ForecastService as fr
import matplotlib.pyplot as plt
from matplotlib.pyplot import ylabel

def datasets_view(temp, data, pollution_name):
    fig, ax = plt.subplots(figsize=(15, 5))
    train = temp.loc[data.index < '2024-09-15']
    test = temp.loc[data.index >= '2024-09-15']
    train.plot(ax=ax, label='Training set', title=f'{pollution_name} Data Train / Test Set')
    test.plot(ax=ax, label='Test set')
    ax.axvline(x='2024-09-15', color='black', ls='--')
    ax.legend(['Training Set', 'Test Set'])
    plt.show()


def tree_month_prediction(test_predictions, y_test, pollution_name):
    days = 90
    samples_per_day = 24
    num_samples = days * samples_per_day
    test_predictions = test_predictions[-num_samples:]
    y_test = y_test[-num_samples:]

    # Ustalenie zakresu osi X (dni)
    x_days = np.linspace(1, days, num=len(test_predictions))

    # Tworzenie wykresu
    plt.figure(figsize=(15, 6))
    plt.plot(x_days, test_predictions, label="Predicted Values", color='blue', marker='o', markersize=2, alpha=0.7)
    plt.plot(x_days, y_test, label="Actual Values", color='red', linestyle='--', marker='x', markersize=2, alpha=0.7)

    # Dodanie tytułu, etykiet osi i legendy
    plt.title("Comparison of Predicted and Actual Values Over 90 Days", fontsize=14)
    plt.xlabel("Days", fontsize=12)
    plt.ylabel(f"{pollution_name} Value", fontsize=12)
    plt.xticks(ticks=np.linspace(1, days, 10), labels=[f"Day {int(x)}" for x in np.linspace(1, days, 10)])
    plt.legend()
    plt.grid(True)

    # Wyświetlenie wykresu
    plt.tight_layout()
    plt.show()


def get_24_results_view(predicted_data_24, real_data_24, pollution_name):
    hours = list(range(1, 25))
    plt.figure(figsize=(12, 6))

    # Plot the mean simulated values with confidence intervals as a shaded area
    plt.plot(hours, predicted_data_24, color='blue', label=f"Predicted {pollution_name}", markersize=3)
    # Plot the actual PM10 values as points
    plt.plot(hours, real_data_24, 'ro-', label=f"Actual {pollution_name}", markersize=3)

    # Labels and Legend
    plt.title(f"{pollution_name} Prediction Over 24 Hours")
    plt.xlabel("Hour")
    plt.ylabel(f"{pollution_name} Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
