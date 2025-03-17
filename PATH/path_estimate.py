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

# Plot Left Encoder Count
plt.figure(figsize=(10, 6))
plt.plot(data1['timestamp'], data1['left_encoder_count'], label='Path 1')
plt.plot(data2['timestamp'], data2['left_encoder_count'], label='Path 2', linestyle='dashed')
plt.title('Left Encoder Count')
plt.xlabel('Timestamp')
plt.ylabel('Count')
plt.legend()
plt.grid()
plt.show()

# Plot Right Encoder Count
plt.figure(figsize=(10, 6))
plt.plot(data1['timestamp'], data1['right_encoder_count'], label='Path 1')
plt.plot(data2['timestamp'], data2['right_encoder_count'], label='Path 2', linestyle='dashed')
plt.title('Right Encoder Count')
plt.xlabel('Timestamp')
plt.ylabel('Count')
plt.legend()
plt.grid()
plt.show()

# Plot Acceleration (X)
plt.figure(figsize=(10, 6))
plt.plot(data1['timestamp'], data1['accel_x'], label='Path 1')
plt.plot(data2['timestamp'], data2['accel_x'], label='Path 2', linestyle='dashed')
plt.title('Acceleration (X)')
plt.xlabel('Timestamp')
plt.ylabel('Acceleration (m/s²)')
plt.legend()
plt.grid()
plt.show()

# Plot Gyro Z-Axis
plt.figure(figsize=(10, 6))
plt.plot(data1['timestamp'], data1['gyro_z'], label='Path 1')
plt.plot(data2['timestamp'], data2['gyro_z'], label='Path 2', linestyle='dashed')
plt.title('Gyro Z-Axis')
plt.xlabel('Timestamp')
plt.ylabel('Angular Velocity (rad/s)')
plt.legend()
plt.grid()
plt.show()

# Plot Magnetometer Heading
plt.figure(figsize=(10, 6))
plt.plot(data1['timestamp'], data1['heading'], label='Path 1')
plt.plot(data2['timestamp'], data2['heading'], label='Path 2', linestyle='dashed')
plt.title('Magnetometer Heading')
plt.xlabel('Timestamp')
plt.ylabel('Heading (degrees)')
plt.legend()
plt.grid()
plt.show()

# Plot Reconstructed Trajectories
plt.figure(figsize=(10, 6))
plt.plot(trajectory1['x'], trajectory1['y'], label='Path 1 (Straight Line)', marker='o', linestyle='-')
plt.plot(trajectory2['x'], trajectory2['y'], label='Path 2 (L-Shaped)', marker='s', linestyle='-')
plt.xlabel('X Position (m)')
plt.ylabel('Y Position (m)')
plt.title('Reconstructed 2D Path of the Vehicle')
plt.legend()
plt.grid()
plt.show()