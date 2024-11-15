
import pandas as pd
import matplotlib.pyplot as plt

# Load data
file_paths = [
    "20210201_CME Oil Data.xlsx",
    "20210202_CME Oil Data.xlsx",
    "20210203_CME Oil Data.xlsx",
    # Add other file paths
]

combined_data = pd.DataFrame()

# Combine all files
for file in file_paths:
    df = pd.read_excel(file)
    combined_data = pd.concat([combined_data, df])

# Rename columns for clarity
combined_data.columns = ["Date", "Time", "Price", "Value", "Indicator"]
combined_data["Datetime"] = pd.to_datetime(combined_data["Date"] + " " + combined_data["Time"])
combined_data = combined_data.dropna(subset=["Datetime", "Price"])
combined_data = combined_data.sort_values("Datetime")
time_series_data = combined_data[["Datetime", "Price"]].set_index("Datetime")
hourly_data = time_series_data.resample("H").mean().fillna(method="ffill")

# Save processed data
hourly_data.to_csv("hourly_data.csv")

# Plot Preprocessing
plt.figure(figsize=(12, 6))
plt.plot(time_series_data["Price"], label="Original Data", alpha=0.5)
plt.plot(hourly_data["Price"], label="Resampled Data (Hourly)", linewidth=2)
plt.title("Data Preprocessing: Original vs Resampled Data")
plt.xlabel("Datetime")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()
