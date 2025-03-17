import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
data = pd.read_csv('/home/sudhujoshi/Desktop/Sem_4/MSD/a2/TOF/tof_benchmark.csv')

# Convert the Timestamp column to datetime format
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Define the expected distances in millimeters and assign unique colors
expected_distances = {
    '0.5m': {'distance': 500, 'color': 'green'},   # 0.5m in mm
    '1m': {'distance': 1000, 'color': 'orange'},   # 1m in mm
    '1.55m': {'distance': 1550, 'color': 'purple'}, # 1.55m in mm
    '2.21m': {'distance': 2210, 'color': 'red'}     # 2.21m in mm
}

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(data['Timestamp'], data['Distance(mm)'], label='Measured Distance (mm)', color='blue', alpha=0.8)

# Add horizontal lines for expected distances with unique colors
for label, info in expected_distances.items():
    plt.axhline(y=info['distance'], color=info['color'], linestyle='--', label=f'Expected {label}')
plt.xlabel('Time')
plt.ylabel('Distance (mm)')
plt.title('Distance vs. Time for ToF Sensor with Color-Coded Expected Distances')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

