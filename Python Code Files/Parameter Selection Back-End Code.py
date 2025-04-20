import pandas as pd

kolkata_data = pd.read_csv("kolkata_daily_data.csv", parse_dates=["date"])

# Clean up any extra spaces in column names
kolkata_data.columns = kolkata_data.columns.str.strip()

selected_parameters = [
    'PM2.5 (ug/m3)', 'PM10 (ug/m3)', 'NO2 (ug/m3)', 'SO2 (ug/m3)',
    'CO (mg/m3)', 'Ozone (ug/m3)',
    'Temp (degree C)', 'RH (%)', 'WS (m/s)', 'WD (degree)',
    'RF (mm)', 'BP (mmHg)'
]

parameter_scores = []

for param in selected_parameters:
    count_col = f"{param}_count"
    if param in kolkata_data.columns and count_col in kolkata_data.columns:
        valid_counts = kolkata_data[count_col]
        completeness = valid_counts.mean() / 168
        std_dev = kolkata_data[param].std()
        relevance = 1 if param in ["PM2.5 (ug/m3)", "PM10 (ug/m3)"] else 0.5
        score = completeness * (1 / (1 + std_dev)) * relevance
        parameter_scores.append((param, score))

parameter_scores.sort(key=lambda x: x[1], reverse=True)
print(parameter_scores)
