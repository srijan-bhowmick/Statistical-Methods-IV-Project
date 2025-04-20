import pandas as pd
import os
import matplotlib.pyplot as plt

kolkata_data = pd.read_csv("kolkata_daily_data.csv", parse_dates=["date"])

# Clean up any extra spaces in column names
kolkata_data.columns = kolkata_data.columns.str.strip()

selected_parameters = [
    'PM2.5 (ug/m3)', 'PM10 (ug/m3)', 'NO2 (ug/m3)', 'SO2 (ug/m3)',
    'CO (mg/m3)', 'Ozone (ug/m3)',
    'Temp (degree C)', 'RH (%)', 'WS (m/s)', 'WD (degree)',
    'RF (mm)', 'BP (mmHg)'
]

for parameter in selected_parameters:
    plt.figure(figsize=(12, 4))
    plt.plot(kolkata_data['date'], kolkata_data[parameter])
    title = f'Daily Average {parameter} Concentration in Kolkata'
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(parameter)
    plt.grid(True)

    # Save the plot
    filename = f"kolkata_{parameter.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '')}_timeseries.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')

    plt.show()


