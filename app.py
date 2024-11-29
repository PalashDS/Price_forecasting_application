import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dropout, Dense

# Rebuild the LSTM model (if needed)
MODEL_PATH = "updated_lstm_model.h5"

try:
    # Load the pre-trained model
    model = load_model(MODEL_PATH)
    st.write("Model loaded successfully.")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Load scaled data
DATA_SCALED_PATH = "data_scaled.npy"
try:
    data_scaled = np.load(DATA_SCALED_PATH)
    st.write(f"Data loaded successfully. Shape: {data_scaled.shape}")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Streamlit app setup
st.title("LSTM Time-Series Forecasting")
st.write("Predict future time steps using the pre-trained LSTM model.")

# User input for future time steps
sequence_length = 50
future_steps = st.number_input("Enter the number of future time steps to predict:", min_value=1, max_value=100, value=10)

if st.button("Predict"):
    st.write("Starting prediction...")

    try:
        # Extract the last sequence from the scaled data
        last_sequence = data_scaled[-sequence_length:]
        forecast_sequence = last_sequence.reshape(1, sequence_length, 1)

        # Generate forecasts
        forecasted_prices = []
        for step in range(future_steps):
            next_price_scaled = model.predict(forecast_sequence)
            forecasted_prices.append(next_price_scaled[0, 0])
            next_price_scaled = next_price_scaled.reshape(1, 1, 1)
            forecast_sequence = np.append(forecast_sequence[:, 1:, :], next_price_scaled, axis=1)

        # Display results
        st.write(f"### Forecasted Prices for the Next {future_steps} Time Steps:")
        for i, price in enumerate(forecasted_prices, 1):
            st.write(f"Time Step {i}: {price:.2f}")

        # Plot the results
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(range(1, future_steps + 1), forecasted_prices, marker="o", linestyle="--")
        ax.set_xlabel("Future Time Step")
        ax.set_ylabel("Predicted Scaled Price")
        ax.set_title("LSTM Forecast")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error during prediction: {e}")
