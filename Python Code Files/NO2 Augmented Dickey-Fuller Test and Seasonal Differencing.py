import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

# Load and preprocess data
data_dir = r"C:\Users\SRIJAN\Downloads\archive"  # Or wherever the file is saved
file_path = os.path.join(data_dir, "kolkata_daily_data.csv")
kolkata_data = pd.read_csv(file_path, parse_dates=["date"])

kolkata_data.columns = kolkata_data.columns.str.strip()
kolkata_data = kolkata_data.sort_values("date")

result = adfuller(kolkata_data['NO2 (ug/m3)'])
print("ADF Statistic:", result[0])
print("p-value:", result[1])

no2_diff = kolkata_data['NO2 (ug/m3)'].diff().dropna()
adf_result = adfuller(no2_diff)
print("ADF Statistic:", adf_result[0])
print("p-value:", adf_result[1])

seasonal_diff = kolkata_data['NO2 (ug/m3)'] - kolkata_data['NO2 (ug/m3)'].shift(365)
seasonal_diff = seasonal_diff.dropna()

# ADF test on seasonally differenced series
adf_result_seasonal = adfuller(seasonal_diff)
print("ADF Statistic (seasonal diff):", adf_result_seasonal[0])
print("p-value (seasonal diff):", adf_result_seasonal[1])


