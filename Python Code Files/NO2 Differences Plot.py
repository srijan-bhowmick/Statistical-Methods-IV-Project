import matplotlib.pyplot as plt
import os
import pandas as pd

# Load and preprocess data
data_dir = r"C:\Users\SRIJAN\Downloads\archive"  # Or wherever the file is saved
file_path = os.path.join(data_dir, "kolkata_daily_data.csv")
kolkata_data = pd.read_csv(file_path, parse_dates=["date"])

# First-order differencing (d = 1)
no2_diff = kolkata_data['NO2 (ug/m3)'].diff().dropna()

# Plot the differenced series
plt.figure(figsize=(12, 4))
plt.plot(kolkata_data['date'][1:], no2_diff)  # Skip first NaN after differencing
plt.title('First-Order Differenced NO2 Time Series (d = 1)')
plt.xlabel('Date')
plt.ylabel('Differenced NO2 (ug/m3)')
plt.grid(True)
plt.tight_layout()

# Save the plot
plt.savefig("NO2_d1_diff_plot.png", dpi=300, bbox_inches='tight')

plt.show()
