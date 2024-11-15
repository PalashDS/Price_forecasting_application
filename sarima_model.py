
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import matplotlib.pyplot as plt

# Load preprocessed data
data = pd.read_csv("hourly_data.csv", index_col="Datetime", parse_dates=True)

# Split data
split_index = int(len(data) * 0.8)
train_data = data.iloc[:split_index]
test_data = data.iloc[split_index:]

# Train SARIMA model
model = SARIMAX(train_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 24))
fitted_model = model.fit(disp=False)

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
plt.plot(forecast_series, label="SARIMA Forecast", color="red")
plt.title("SARIMA Model: Actual vs Forecast")
plt.xlabel("Datetime")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()
