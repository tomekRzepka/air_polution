import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Load the dataset
file_path = "two_week_data.csv"
data = pd.read_csv(file_path)

# Parse the date column and set it as the index
data = pd.read_csv(file_path, usecols=['Date','CO','PM10','NO2','PM25','SO2'], parse_dates=['Date'])
# data.set_index('date', inplace=True)

# Select the column to forecast (e.g., 'PM10')
target_column = 'PM10'

# Ensure the data is sorted by date
# data = data.sort_index()

# Drop rows with missing values in the target column
# data = data[[target_column]].dropna()

# Plot the data to visualize trends
plt.figure(figsize=(12, 6))
plt.plot(data, label=f'{target_column} values', color='blue')
plt.title(f'{target_column} - Last 2 Weeks')
plt.xlabel('Date')
plt.ylabel(target_column)
plt.legend()
plt.show()

# Train/Test Split: Use last 7 days for testing and the rest for training
train = data[:-24]  # All but the last 24 hours
test = data[-24:]   # Last 24 hours for evaluation

# Fit an ARIMA model (you can adjust p, d, q based on data behavior)
p, d, q = 2, 1, 2  # Hyperparameters of ARIMA
model = ARIMA(train, order=(p, d, q))
model_fit = model.fit()

# Print model summary
print(model_fit.summary())

# Forecast the next 24 hours (next day)
forecast = model_fit.forecast(steps=24)
forecast_index = pd.date_range(start=data.index[-1] + pd.Timedelta(hours=1), periods=24, freq='H')
forecast_series = pd.Series(forecast, index=forecast_index)

# Plot the forecast vs actual values
plt.figure(figsize=(12, 6))
plt.plot(data, label='Actual Values', color='blue')
plt.plot(forecast_series, label='Forecast (Next Day)', color='orange', linestyle='--')
plt.axvline(x=data.index[-1], color='red', linestyle='--', label='Forecast Start')
plt.title(f'Forecast for {target_column} (Next Day)')
plt.xlabel('Date')
plt.ylabel(target_column)
plt.legend()
plt.show()

# Combine forecast with test data for evaluation
result_df = pd.DataFrame({
    'Actual': test[target_column] if not test.empty else None,
    'Forecast': forecast_series
})

print("\nForecast vs Actual Values:")
print(result_df)
