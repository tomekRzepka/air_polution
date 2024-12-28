import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Input
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
X, y = data_to_X_y(temp, WINDOW_SIZE)
X_train, y_train = X[:11000], y[:11000]
X_val, y_val = X[11000:13000], y[11000:13000]
X_test, y_test = X[13000:], y[13000:]

(h)(11,11.2,..,n)  -> n - ilośc dni

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

# Model evaluation
model1 = load_model('model1.keras')
train_predictions = model1.predict(X_train).flatten()
train_result = pd.DataFrame({'Train Predictions': train_predictions, 'Actuals': y_train})

# Plot results
plt.plot(train_result['Train Predictions'], label='Predictions')
# plt.plot(train_result['Actuals'], label='Actuals')
plt.legend()
plt.show()
