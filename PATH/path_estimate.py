import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Constants
PULSE_TO_MM = 0.095  # Each encoder pulse corresponds to 0.095 mm
TRACK_WIDTH = 0.105  # Distance between the tracks in meters (10.5 cm)

# Function to clean and preprocess the data
def clean_data(data):
    # Convert timestamp to datetime
    if 'timestamp' in data.columns:
        data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')

    # Handle missing values with forward and backward filling
    data.ffill(inplace=True)
    data.bfill(inplace=True)

    return data

# Function to reconstruct the trajectory
def reconstruct_trajectory(data):
    # Compute time step differences
    data['dt'] = data['timestamp'].diff().dt.total_seconds().fillna(0)

    # Compute displacement for left and right tracks (convert mm to meters)
    data['left_displacement'] = data['left_encoder_count'].diff().fillna(0) * PULSE_TO_MM / 1000
    data['right_displacement'] = data['right_encoder_count'].diff().fillna(0) * PULSE_TO_MM / 1000

    # Compute change in orientation (delta_theta)
    data['delta_theta'] = (data['right_displacement'] - data['left_displacement']) / TRACK_WIDTH

    # Use magnetometer heading as primary orientation
    data['theta'] = np.radians(data['heading'])

    # Compute displacement magnitude (average displacement)
    data['average_displacement'] = (data['left_displacement'] + data['right_displacement']) / 2

    # Compute x and y position changes
    data['delta_x'] = data['average_displacement'] * np.cos(data['theta'])
    data['delta_y'] = data['average_displacement'] * np.sin(data['theta'])

    # Compute cumulative x and y positions
    data['x'] = data['delta_x'].cumsum()
    data['y'] = data['delta_y'].cumsum()

    return data

# Load and clean datasets
file_path_1 = "/home/sudhujoshi/Desktop/Sem_4/MSD/a2/PATH/telemetry_data/path_1_telemetry.csv"
file_path_2 = "/home/sudhujoshi/Desktop/Sem_4/MSD/a2/PATH/telemetry_data/path_2_telemetry.csv"

data1 = clean_data(pd.read_csv(file_path_1))
data2 = clean_data(pd.read_csv(file_path_2))

# Reconstruct trajectories
trajectory1 = reconstruct_trajectory(data1)
trajectory2 = reconstruct_trajectory(data2)

# Create a grid of subplots
fig, axs = plt.subplots(3, 2, figsize=(12, 8))
fig.suptitle('Sensor Data Comparison')

# Plot Left Encoder Count
axs[0, 0].plot(data1['timestamp'], data1['left_encoder_count'], label='Path 1')
axs[0, 0].plot(data2['timestamp'], data2['left_encoder_count'], label='Path 2', linestyle='dashed')
axs[0, 0].set_title('Left Encoder Count')
axs[0, 0].legend()
axs[0, 0].grid()

# Plot Right Encoder Count
axs[0, 1].plot(data1['timestamp'], data1['right_encoder_count'], label='Path 1')
axs[0, 1].plot(data2['timestamp'], data2['right_encoder_count'], label='Path 2', linestyle='dashed')
axs[0, 1].set_title('Right Encoder Count')
axs[0, 1].legend()
axs[0, 1].grid()

# Plot Acceleration (X)
axs[1, 0].plot(data1['timestamp'], data1['accel_x'], label='Path 1')
axs[1, 0].plot(data2['timestamp'], data2['accel_x'], label='Path 2', linestyle='dashed')
axs[1, 0].set_title('Acceleration (X)')
axs[1, 0].legend()
axs[1, 0].grid()

# Plot Gyro Z-Axis
axs[1, 1].plot(data1['timestamp'], data1['gyro_z'], label='Path 1')
axs[1, 1].plot(data2['timestamp'], data2['gyro_z'], label='Path 2', linestyle='dashed')
axs[1, 1].set_title('Gyro Z-Axis')
axs[1, 1].legend()
axs[1, 1].grid()

# Plot Magnetometer Heading
axs[2, 0].plot(data1['timestamp'], data1['heading'], label='Path 1')
axs[2, 0].plot(data2['timestamp'], data2['heading'], label='Path 2', linestyle='dashed')
axs[2, 0].set_title('Heading')
axs[2, 0].legend()
axs[2, 0].grid()

# Hide the last subplot (unused)
axs[2, 1].axis('off')

# Adjust layout and show plots
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# Plot reconstructed trajectories separately
plt.figure(figsize=(10, 6))
plt.plot(trajectory1['x'], trajectory1['y'], label='Path 1 (Straight Line)', marker='o', linestyle='-')
plt.plot(trajectory2['x'], trajectory2['y'], label='Path 2 (L-Shaped)', marker='s', linestyle='-')
plt.xlabel('X Position (m)')
plt.ylabel('Y Position (m)')
plt.title('Reconstructed 2D Path of the Vehicle')
plt.legend()
plt.grid(True)
plt.show()