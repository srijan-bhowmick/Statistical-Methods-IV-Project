import os
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

# Load and preprocess data
data_dir = r"C:\Users\SRIJAN\Downloads\archive"  # Or wherever the file is saved
file_path = os.path.join(data_dir, "kolkata_daily_data.csv")
kolkata_data = pd.read_csv(file_path, parse_dates=["date"])



kolkata_data['date'] = pd.to_datetime(kolkata_data['date'])
kolkata_data.set_index('date', inplace=True)
kolkata_data = kolkata_data.asfreq('D')

# Extract the NO2 values (you might need to adjust the column name based on your data)
no2_data = kolkata_data['NO2 (ug/m3)']

# Fit the SARIMA model
sarima_model = SARIMAX(no2_data, 
                       order=(1, 1, 1),  # p, d, q
                       seasonal_order=(1, 1, 1, 7),  # P, D, Q, s
                       enforce_stationarity=False,
                       enforce_invertibility=False)

sarima_result = sarima_model.fit(disp=False)

# Print the model summary
print(sarima_result.summary())

# Plot the fitted values against the original data
plt.figure(figsize=(12, 6))
plt.plot(no2_data, label='Original NO2 Data')
plt.plot(sarima_result.fittedvalues, label='Fitted NO2 Data', color='orange')
plt.title('SARIMA Model Fit to NO2 Data')
plt.xlabel('Date')
plt.ylabel('NO2 (ug/m3)')
plt.legend()
plt.grid(True)
plt.savefig("NO2_SARIMA_fit_s=7.png", dpi=300, bbox_inches='tight')
plt.show()
