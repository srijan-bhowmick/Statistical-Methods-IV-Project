import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf



# Load and preprocess data
data_dir = r"C:\Users\SRIJAN\Downloads\archive"  # Or wherever the file is saved
file_path = os.path.join(data_dir, "kolkata_daily_data.csv")
kolkata_data = pd.read_csv(file_path, parse_dates=["date"])
kolkata_data.columns = kolkata_data.columns.str.strip()
kolkata_data = kolkata_data.sort_values("date")

# Extract NO2 and drop missing values
no2_df = kolkata_data[["date", "NO2 (ug/m3)"]].dropna()
no2_df = no2_df[no2_df["date"] >= "2019-08-30"]  # Threshold date

# Convert date to ordinal for regression
no2_df["date_ordinal"] = no2_df["date"].map(pd.Timestamp.toordinal)

# Fit linear regression model
X = no2_df["date_ordinal"].values.reshape(-1, 1)
y = no2_df["NO2 (ug/m3)"].values
linreg = LinearRegression()
linreg.fit(X, y)

# Predict trend
no2_df["trend"] = linreg.predict(X)

# Plot original vs. trend
plt.figure(figsize=(14, 5))
plt.plot(no2_df["date"], no2_df["NO2 (ug/m3)"], label="Actual NO2", color="blue")
plt.plot(no2_df["date"], no2_df["trend"], label="Linear Trend", color="red", linewidth=2)
plt.title("Linear Trend Fit for NO2 (ug/m3) in Kolkata")
plt.xlabel("Date")
plt.ylabel("NO2 (ug/m3)")
plt.legend()
plt.grid(True)
plt.tight_layout()
#plt.savefig("NO2 Trend Component.png", dpi=300, bbox_inches='tight')
plt.show()


no2_df["detrended"] = no2_df["NO2 (ug/m3)"] / no2_df["trend"]

plt.figure(figsize=(14, 5))
plt.plot(no2_df["date"], no2_df["detrended"], label="Detrended Series", color="purple")
plt.title("Detrended NO2 (Multiplicative Model)")
plt.xlabel("Date")
plt.ylabel("Ratio (Actual / Trend)")
plt.grid(True)
plt.tight_layout()
#plt.savefig("Detrended NO2.png", dpi=300, bbox_inches='tight')
plt.show()


# Ensure regular frequency
no2_df.set_index("date", inplace=True)
no2_df = no2_df.asfreq("D")  # fill missing days as NaN

# Fill missing values if needed (interpolate or forward-fill)
no2_df["NO2 (ug/m3)"] = no2_df["NO2 (ug/m3)"].interpolate()

# Apply seasonal decomposition
result = seasonal_decompose(no2_df["NO2 (ug/m3)"], model="multiplicative", period=365)
result.plot()

# Adjust the X-axis label font size
plt.xticks(fontsize=8)  # Change the number 8 to whatever size you prefer

plt.tight_layout()
# plt.savefig("NO2 decomposition.png", dpi=300, bbox_inches='tight')
plt.show()



# Drop NaNs from residuals
residuals = result.resid.dropna()

# Plot residuals
plt.figure(figsize=(14, 5))
plt.plot(residuals, color='teal')
plt.title("Residuals from Multiplicative Decomposition of NO₂")
plt.xlabel("Date")
plt.ylabel("Residual")
plt.grid(True)
plt.tight_layout()
#plt.savefig("NO2_residuals_plot.png", dpi=300, bbox_inches='tight')
plt.show()

# Plot ACF of residuals
plot_acf(residuals, lags=50)
plt.title("ACF of Residuals (NO₂)")
plt.tight_layout()
#plt.savefig("NO2_residuals_ACF.png", dpi=300, bbox_inches='tight')
plt.show()
