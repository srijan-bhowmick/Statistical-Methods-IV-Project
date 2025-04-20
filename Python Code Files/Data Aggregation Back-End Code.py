import pandas as pd
import os

# Set the local data directory
data_dir = r"C:\Users\SRIJAN\Downloads\archive"

# Load station info file
stations_info_path = os.path.join(data_dir, "stations_info.csv")
stations_info_df = pd.read_csv(stations_info_path)

# Only focus on Kolkata
target_city = "Kolkata"

# Extract station codes for Kolkata
kolkata_station_codes = stations_info_df[stations_info_df["city"] == target_city]["file_name"].tolist()

# Parameters to retain
selected_parameters = [
    'PM2.5 (ug/m3)', 'PM10 (ug/m3)', 'NO2 (ug/m3)', 'SO2 (ug/m3)',
    'CO (mg/m3)', 'Ozone (ug/m3)',
    'Temp (degree C)', 'RH (%)', 'WS (m/s)', 'WD (degree)',
    'RF (mm)', 'BP (mmHg)'
]

# Date column
date_column = "From Date"

# Dictionary to store Kolkata's data
kolkata_data = {}

# To store the threshold date for Kolkata
kolkata_threshold_date = None

# First pass: determine the maximum of the minimum first date for Kolkata's stations
station_min_dates = []

for code in kolkata_station_codes:
    file_path = os.path.join(data_dir, f"{code}.csv")
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, usecols=[date_column], low_memory=False)
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce').dt.date
            min_date = df[date_column].min()
            if pd.notna(min_date):
                station_min_dates.append(min_date)
        except Exception as e:
            print(f"Error reading dates from {code}.csv: {e}")

if station_min_dates:
    kolkata_threshold_date = max(station_min_dates)
    print(f"Kolkata threshold date: {kolkata_threshold_date}")
else:
    print("No valid dates found for Kolkata.")

# Second pass: load and filter actual data for Kolkata
kolkata_frames = []

for code in kolkata_station_codes:
    file_path = os.path.join(data_dir, f"{code}.csv")
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, low_memory=False)
            df["station_code"] = code
            df["city"] = target_city
            df["date"] = pd.to_datetime(df[date_column], errors='coerce').dt.date
            df = df[df["date"] >= kolkata_threshold_date]  # Filter by threshold date
            cols_to_keep = ["date", "city", "station_code"] + [col for col in selected_parameters if col in df.columns]
            kolkata_frames.append(df[cols_to_keep])
        except Exception as e:
            print(f"Error loading {code}.csv: {e}")

if kolkata_frames:
    kolkata_df = pd.concat(kolkata_frames, ignore_index=True)

    # Compute daily means
    daily_means = kolkata_df.groupby(["city", "date"]).mean(numeric_only=True)

    # Compute daily counts (non-missing values)
    daily_counts = kolkata_df.groupby(["city", "date"])[selected_parameters].count()
    daily_counts.columns = [f"{col}_count" for col in daily_counts.columns]

    # Combine means and counts
    kolkata_daily = pd.concat([daily_means, daily_counts], axis=1).reset_index()

    kolkata_data = kolkata_daily


# Display the number of stations in Kolkata
num_stations_kolkata = len(kolkata_station_codes)
print(f"Number of stations in Kolkata: {num_stations_kolkata}")

pd.set_option('display.max_columns', None)  # Show all columns
print(kolkata_data.head(5))

print(kolkata_data)

kolkata_data.to_csv("kolkata_daily_data.csv", index=False)
