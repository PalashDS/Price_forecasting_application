
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import matplotlib.pyplot as plt

# Load preprocessed data
data = pd.read_csv("hourly_data.csv", index_col="Datetime", parse_dates=True)

# Split data
split_index = int(len(data) * 0.8)
train_data = data.iloc[:split_index]
test_data = data.iloc[split_index:]

# Train ARIMA model
model = ARIMA(train_data, order=(5, 1, 0))
fitted_model = model.fit()

# Forecast
forecast = fitted_model.forecast(steps=len(test_data))
forecast_series = pd.Series(forecast, index=test_data.index)

# Evaluate
mse = mean_squared_error(test_data, forecast_series)
mae = mean_absolute_error(test_data, forecast_series)
rmse = np.sqrt(mse)

# Print Evaluation Metrics
print(f"MSE: {mse}, MAE: {mae}, RMSE: {rmse}")

# Plot Actual vs Forecast
plt.figure(figsize=(12, 6))
plt.plot(train_data, label="Training Data")
plt.plot(test_data, label="Test Data")
plt.plot(forecast_series, label="ARIMA Forecast", color="green")
plt.title("ARIMA Model: Actual vs Forecast")
plt.xlabel("Datetime")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()
