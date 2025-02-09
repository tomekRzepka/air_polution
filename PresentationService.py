import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from django.template.defaultfilters import length
from matplotlib.pyplot import ylabel

def datasets_view(temp, data, pollution_name):
    fig, ax = plt.subplots(figsize=(15, 5))
    train = temp.loc[data.index < '2024-09-15']
    validation = temp.loc[(data.index >= '2024-05-28') & (data.index < '2024-09-15')]
    test = temp.loc[data.index >= '2024-09-15']
    train.plot(ax=ax, label='Training set', title=f'{pollution_name} Data Train/ Validation Set / Test Set', ylabel = f"{pollution_name} µg/m^3")
    validation.plot(ax=ax, label='Validation set')
    test.plot(ax=ax, label='Test set')
    ax.axvline(x='2024-05-28', color='red', ls='--',  label="Validation Start")
    ax.axvline(x='2024-09-15', color='black', ls='--', label="Test Start")
    ax.legend(['Training Set', 'Validation Set','Test Set', 'Validation Start', 'Test Start'])
    plt.show()


def test_prediction_view(test_predictions, y_test, pollution_name):
    start_date = "2024-09-15"
    # Tworzenie listy pełnych znaczników czasowych co godzinę
    start_date = pd.to_datetime(start_date)  # Konwersja na obiekt daty
    x_hours = pd.date_range(start=start_date, periods=length(test_predictions), freq='h')

    # Tworzenie wykresu
    plt.figure(figsize=(15, 6))
    plt.plot(x_hours, test_predictions, label="Predicted Values", color='blue', marker='o', markersize=2, alpha=0.7)
    plt.plot(x_hours, y_test, label="Actual Values", color='red', linestyle='--', marker='x', markersize=2, alpha=0.7)

    # Dodanie tytułu, etykiet osi i legendy
    plt.title(f"Comparison of Predicted and Test {pollution_name} Values Over test period", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel(f"{pollution_name} Value (µg/m³)", fontsize=12)


    plt.xticks(ticks=x_hours[::7 * 24], labels=[date.strftime('%Y-%m-%d') for date in x_hours[::7 * 24]], rotation=45)

    plt.legend()
    plt.grid(True)

    # Wyświetlenie wykresu
    plt.tight_layout()
    plt.show()



def get_24_results_view(predicted_data_24, real_data_24, pollution_name):
    # Tworzenie listy godzinnych znaczników czasu dla wybranego dnia
    selected_date = pd.to_datetime("2024-12-31")  # Konwersja na datetime
    x_hours = pd.date_range(start=selected_date, periods=24, freq='H')  # Co godzinę od 00:00 do 23:00

    # Tworzenie wykresu
    plt.figure(figsize=(12, 6))

    # Rysowanie linii dla prognozowanych wartości
    plt.plot(x_hours, predicted_data_24, color='blue', label=f"Predicted {pollution_name}", marker='o', markersize=4)

    # Rysowanie linii dla rzeczywistych wartości
    plt.plot(x_hours, real_data_24, 'ro-', label=f"Actual {pollution_name}", markersize=4)

    # Ustawienie tytułów i etykiet
    plt.title(f"{pollution_name} Prediction for {selected_date.strftime('%Y-%m-%d')}", fontsize=14)
    plt.xlabel("Time (Hour)", fontsize=12)
    plt.ylabel(f"{pollution_name} Value (µg/m³)", fontsize=12)

    # Poprawne oznaczenia osi X (co godzinę)
    plt.xticks(ticks=x_hours, labels=[time.strftime('%H:%M') for time in x_hours], rotation=45)

    # Dodatkowe opcje wizualne
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Wyświetlenie wykresu
    plt.show()