import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import ForecastService as fc
import AirPollutionRepository as repo

# Function to prepare pollution data, specifically for PM10
pollution_name = "pm10"
station_name = "TEST"
station_code = "testCode"


def preparePollutionData():
    # Default min and max values for {pollution_name}

    try:
        predicted_data, real_data = fc.get_last_24_predictions_reals()  # Ensure this returns valid data
        return predicted_data, real_data, min(predicted_data), max(predicted_data)

    except Exception as e:
        raise Exception(f"Error while fetching last 24 predictions: {e}")


# Fetch pollution data and default ranges
pollution_data, real_data, pollution_min, pollution_max = preparePollutionData()
if pollution_data is None:
    raise Exception(f"Unable to load {pollution_name} data.")

hours = list(range(1, 25))

mean_predicted = np.mean(pollution_data)
Cavg_predicted = round(mean_predicted, 2)
Clow_predicted = round(pollution_min, 2)
Chigh_predicted = round(pollution_max, 2)

mean_real = np.mean(real_data)
Cavg_real = round(mean_real, 2)
Clow_real = round(min(real_data), 2)
Chigh_real = round(max(real_data), 2)

print("______________________________________")
print("AIR QUALITY INDEX FOR PREDICTIONS")
print(f"Predicted mean:  {Cavg_predicted}  Real mean: {Cavg_real}")
print(f"Predicted min: {Clow_predicted}   Real min: {Clow_real} ")
print(f"Predicted max: {Chigh_predicted}  Real max: {Chigh_real}")

IhighEU = 0
IlowEU = 0
# CAQI - European Index table
match Cavg_predicted:
    case Cavg_predicted if Cavg_predicted <= 25:
        IhighEU = 25
        IlowEU = 0
    case Cavg_predicted if 26 <= Cavg_predicted <= 50:
        IhighEU = 50
        IlowEU = 25
    case Cavg_predicted if 50 < Cavg_predicted <= 90:
        IhighEU = 75
        IlowEU = 50
    case Cavg_predicted if 90 < Cavg_predicted <= 180:
        IhighEU = 100
        IlowEU = 75
IhighUS = 0
IlowUS = 0
match Cavg_predicted:
    case Cavg_predicted if Cavg_predicted <= 54:
        IhighUS = 50
        IlowUS = 0
    case Cavg_predicted if 54 < Cavg_predicted <= 154:
        IhighUS = 100
        IlowUS = 51
    case Cavg_predicted if 154 < Cavg_predicted <= 254:
        IhighUS = 150
        IlowUS = 101
    case Cavg_predicted if 254 < Cavg_predicted <= 354:
        IhighUS = 200
        IlowUS = 151

predicted_indexEU = round(
    (((IhighEU - IlowEU) / (Chigh_predicted - Clow_predicted)) * (Cavg_predicted - Clow_predicted) + IlowEU), 2)
predicted_indexUS = round(
    (((IhighUS - IlowUS) / (Chigh_predicted - Clow_predicted)) * (Cavg_predicted - Clow_predicted) + IlowUS), 2)
real_indexEU = round((((IhighEU - IlowEU) / (Chigh_real - Clow_real)) * (Cavg_real - Clow_real) + IlowEU), 2)
real_indexUS = round((((IhighUS - IlowUS) / (Chigh_real - Clow_real)) * (Cavg_real - Clow_real) + IlowUS), 2)

print(f"Predicted AQI EU :  {predicted_indexEU}")
print(f"Predicted AQI US :  {predicted_indexUS}")
print(f"Real AQI EU :  {real_indexEU}")
print(f"Real AQI US :  {real_indexUS}")

# Save or update the data
repo.save_pollution_data(station_code,pollution_name, Cavg_predicted, Cavg_real)
# Fetch highest AQI pair from database for selected station
max_predicted, max_predicted_column, max_real, max_real_column = repo.fetch_max_AQI_values_for_station(station_code)
print("______________________________________")
print(f"For station {station_code} AQImax based on predicted values : {max_predicted_column}: {max_predicted} ")
print(f"For station {station_code} AQImax based on real values: {max_real_column}: {max_real} ")


# Plotting
plt.figure(figsize=(12, 6))

# Plot the mean simulated values with confidence intervals as a shaded area
plt.plot(hours, pollution_data, color='blue', label=f"Predicted {pollution_name}", markersize=3)
# Plot the actual PM10 values as points
plt.plot(hours, real_data, 'ro-', label=f"Actual {pollution_name}", markersize=3)

# Labels and Legend
plt.title(f"{pollution_name} Prediction Over 24 Hours")
plt.xlabel("Hour")
plt.ylabel(f"{pollution_name} Value")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
