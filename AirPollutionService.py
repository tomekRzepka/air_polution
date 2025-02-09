import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import ForecastService as fc
import AirPollutionRepository as repo
import PresentationService as ps

# Function to prepare pollution data, specifically for PM10
pollution_name = "NO2"
pollution_column = "no2"
station_name = "WarszawaNiepodleglosci"
station_code = "PL0140A"


def preparePollutionData():
    # Default min and max values for {pollution_name}

    try:
        predicted_data, real_data = fc.get_predictions_tests()  # Ensure this returns valid data
        return predicted_data, real_data,

    except Exception as e:
        raise Exception(f"Error while fetching last 24 predictions: {e}")


# Fetch pollution data and default ranges
predicted_data, real_data = preparePollutionData()

ps.test_prediction_view(predicted_data, real_data, pollution_name)

predicted_data_24 = predicted_data[-24:]
real_data_24 = real_data[-24:]
pollution_min = min(predicted_data_24)
pollution_max = max(predicted_data_24)

if predicted_data_24 is None:
    raise Exception(f"Unable to load {pollution_name} data.")



mean_predicted = np.mean(predicted_data_24)
Cavg_predicted = round(mean_predicted, 2)
Clow_predicted = round(pollution_min, 2)
Chigh_predicted = round(pollution_max, 2)

mean_real = np.mean(real_data_24)
Cavg_real = round(mean_real, 2)
Clow_real = round(min(real_data_24), 2)
Chigh_real = round(max(real_data_24), 2)

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
# print(f"Predicted AQI US :  {predicted_indexUS}")
print(f"Real AQI EU :  {real_indexEU}")
# print(f"Real AQI US :  {real_indexUS}")

# Save or update the data
repo.save_pollution_data(station_name,station_code, pollution_column, predicted_indexEU, real_indexEU)
# Fetch highest AQI pair from database for selected station
max_predicted, max_predicted_column, max_real, max_real_column = repo.fetch_max_AQI_values_for_station(station_code)
print("______________________________________")
print(f"For station {station_code} AQImax based on predicted values : {max_predicted_column}: {max_predicted} ")
print(f"For station {station_code} AQImax based on real values: {max_real_column}: {max_real} ")


ps.get_24_results_view(predicted_data_24, real_data_24, pollution_name)

