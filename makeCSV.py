import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Parameters
n_points = 5000
time_start = datetime(2024, 1, 1)
time_interval = timedelta(minutes=5)

time_series = [time_start + i * time_interval for i in range(n_points)]
values = np.zeros(n_points)

# Define positions and values for peaks and valleys (modifiable)
peak_positions = [500, 1500, 2500, 3500, 4500]  # Modify or extend this list as needed
peak_values = [10.0, 8.0, 12.0, 9.0, 11.0]      # Modify or extend this list as needed

valley_positions = [0, 1000, 2000, 3000]  # Modify or extend this list as needed
valley_values = [4.0, 2.0, 0.0, 3.0]       # Modify or extend this list as needed

# Ensure the lists are correctly aligned
assert len(peak_values) == len(peak_positions), "Number of peak values must match number of peak positions"
assert len(valley_values) == len(valley_positions), "Number of valley values must match number of valley positions"

# Assign values to peaks and valleys
for i, peak in enumerate(peak_positions):
    values[peak] = peak_values[i]
for i, valley in enumerate(valley_positions):
    values[valley] = valley_values[i]

# Interpolate smoothly between peaks and valleys
all_positions = sorted(peak_positions + valley_positions)
all_values = [values[pos] for pos in all_positions]

for i in range(len(all_positions) - 1):
    start = all_positions[i]
    end = all_positions[i + 1]
    start_value = all_values[i]
    end_value = all_values[i + 1]

    for j in range(start, end):
        interp_value = np.interp(j, [start, end], [start_value, end_value])
        noise = np.random.normal(0, 0.5)  # Adjust the standard deviation as needed
        values[j] = interp_value + noise

df = pd.DataFrame({
    'DateTime': time_series,
    'ValorDecimal': values
})

file_path = './patron1parecido.csv'
df.to_csv(file_path, index=False)
file_path