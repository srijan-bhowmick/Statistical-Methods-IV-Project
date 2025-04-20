import pandas as pd
import matplotlib.pyplot as plt

# Assuming kolkata_data is already loaded and has a 'date' column and 'NO2 (ug/m3)' column
kolkata_data = pd.read_csv("kolkata_daily_data.csv", parse_dates=["date"])
kolkata_data = kolkata_data.sort_values("date")
no2_series = kolkata_data.set_index("date")["NO2 (ug/m3)"]

# 30-day and 90-day moving averages
no2_30ma = no2_series.rolling(window=30, center=True).mean()
no2_90ma = no2_series.rolling(window=90, center=True).mean()

# Plot
plt.figure(figsize=(14, 6))
plt.plot(no2_series, label="Original NO₂", alpha=0.5)
plt.plot(no2_30ma, label="30-day Moving Average", linewidth=2)
plt.plot(no2_90ma, label="90-day Moving Average", linewidth=2)
plt.title("NO₂ Concentration and Moving Averages (Trend Estimation)")
plt.xlabel("Date")
plt.ylabel("NO₂ (µg/m³)")
plt.legend()
plt.grid(True)
plt.show()
