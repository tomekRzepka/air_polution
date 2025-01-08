import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from  .keras.layers import LSTM, Dense, Input
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
import matplotlib.pyplot as plt

# Dataset loading and preprocessing
file_path = "pm10pomiaryTest.csv"
data = pd.read_csv(file_path, usecols=['Date', 'PM10'], parse_dates=['Date'])
data.index = pd.to_datetime(data['Date'], format='%d.%m.%Y %H:%M:%S')
temp = data['PM10']

# Normalize data to range [0, 1] for better LSTM performance
data_min = temp.min()
data_max = temp.max()
normalized_temp = (temp - data_min) / (data_max - data_min)

# Prepare the dataset for LSTM
def data_to_X_y(data, window_size=5):
    data_as_np = data.to_numpy()
    X = []
    y = []
    for i in range(len(data_as_np) - window_size):
        row = [[a] for a in data_as_np[i:i+window_size]]
        X.append(row)
        label = data_as_np[i + window_size]
        y.append(label)
    return np.array(X), np.array(y)

WINDOW_SIZE = 5
X, y = data_to_X_y(normalized_temp, WINDOW_SIZE)
X_train, y_train = X[:11000], y[:11000]
X_val, y_val = X[11000:13000], y[11000:13000]
X_test, y_test = X[13000:], y[13000:]

# Model definition
model1 = Sequential([
    Input(shape=(WINDOW_SIZE, 1)),
    LSTM(64),
    Dense(8, activation='relu'),
    Dense(1, activation='linear')
])

model1.summary()

# Model training
cp = ModelCheckpoint('model1.keras', save_best_only=True)
model1.compile(loss=MeanSquaredError(), optimizer=Adam(learning_rate=0.0001), metrics=[RootMeanSquaredError()])
model1.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=10, callbacks=[cp])

# Load the best model
model1 = load_model('model1.keras')

# Make predictions on the test set
test_predictions = model1.predict(X_test).flatten()

# De-normalize predictions and actual values to original scale
test_predictions = test_predictions * (data_max - data_min) + data_min
y_test = y_test * (data_max - data_min) + data_min

# Extract the last 24 predictions
last_24_predictions = test_predictions[-24:]
last_24_actuals = y_test[-24:]

# Plot predictions and actuals
plt.figure(figsize=(12, 6))
plt.plot(range(len(last_24_predictions)), last_24_predictions, label='Predictions', marker='o')
plt.plot(range(len(last_24_actuals)), last_24_actuals, label='Actuals', marker='x')
plt.title('Last 24 Predictions vs Actuals')
plt.xlabel('Time (Hours)')
plt.ylabel('PM10 Value')
plt.legend()
plt.show()

# Method to return the last 24 predictions
def get_last_24_predictions_reals():
    return test_predictions[-24:],y_test[-24:]
def last_24_predictions():
    # Return the last 24 predictions as a DataFrame
    return last_24_predictions

# Print the last 24 predictions
print("Last 24 Predictions:", last_24_predictions)
