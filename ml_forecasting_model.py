import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
import os

# Load the dataset
def load_data(file_path):
    """Load solar panel and electricity usage data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        raise Exception(f"File {file_path} not found")

# Preprocess the data
def preprocess_data(data, lookback=24):
    """
    Scale and prepare data for LSTM model.
    
    Parameters:
    - data: Pandas DataFrame containing the dataset.
    - lookback: Number of time steps for the input sequence.
    
    Returns:
    - x, y: Features and labels as numpy arrays.
    - scaler: Scaler object for inverse transformation.
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    x, y = [], []
    for i in range(lookback, len(scaled_data)):
        x.append(scaled_data[i-lookback:i])
        y.append(scaled_data[i, 0])  # Assuming the target is the first column (electricity usage)

    return np.array(x), np.array(y), scaler

# Build LSTM model
def build_model(input_shape):
    """
    Build an LSTM model for time-series forecasting.
    
    Parameters:
    - input_shape: Shape of the input data.
    
    Returns:
    - model: Compiled LSTM model.
    """
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50))
    model.add(Dense(1))  # Predicting one value (electricity usage)

    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Train the model
def train_model(model, x_train, y_train, epochs=50, batch_size=32):
    """Train the LSTM model on the provided training data."""
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)
    return model

# Save and load model
def save_model(model, filepath='model.h5'):
    """Save the trained model to a file."""
    model.save(filepath)

def load_model(filepath='model.h5'):
    """Load a saved model from file."""
    return tf.keras.models.load_model(filepath)

# Forecast the emissions
def forecast_emissions(model, x_input, scaler):
    """Use the model to forecast emissions."""
    predictions = model.predict(x_input)
    predicted_emissions = scaler.inverse_transform(predictions)
    return predicted_emissions

if __name__ == '__main__':
    data = load_data('solar_panel_data.csv')
    x, y, scaler = preprocess_data(data)
    model = build_model((x.shape[1], x.shape[2]))
    trained_model = train_model(model, x, y)
    save_model(trained_model)
    emissions_forecast = forecast_emissions(trained_model, x[-24:], scaler)
    print("Forecasted Carbon Emissions:", emissions_forecast)
