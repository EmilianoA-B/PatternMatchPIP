import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Parameters
n_points = 4000
time_start = datetime(2024, 1, 1)
time_interval = timedelta(minutes=5)

time_series = [time_start + i * time_interval for i in range(n_points)]
values = np.zeros(n_points)

# Asignar datos
all_positions = [0,1000,2000,3000,4000]
all_values = [10.0,-4.7,3.5,1.1,4.9]

# Puntos de incio y puntos de final
for i in range(len(all_positions) - 1):
    start = all_positions[i]
    end = all_positions[i + 1]
    start_value = all_values[i]
    end_value = all_values[i + 1]

    for j in range(start, end):
        interp_value = np.interp(j, [start, end], [start_value, end_value])
        noise = np.random.normal(0, 0.5)  # Adjust the standard deviation as needed
        values[j] = interp_value + noise

# Asignar valores al data frame
df = pd.DataFrame({
    'DateTime': time_series,
    'ValorDecimal': values
})

#Crear csv
file_path = './patrones/patron1kindofparecido.csv'
df.to_csv(file_path, index=False)
file_path