import open3d as o3d
import numpy as np
import pickle

def visualize_pcd(file_path):
    # Load the .pcd file
    point_cloud = o3d.io.read_point_cloud(file_path)
    
    # Visualize the point cloud
    o3d.visualization.draw_geometries([point_cloud],
                                      window_name="Point Cloud Visualization",
                                      width=800,
                                      height=600)

def visualize_pkl(file_path):
    # Load the .pkl file
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    
    # Assuming the .pkl file contains a numpy array of points
    if isinstance(data, np.ndarray):
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(data)
        
        # Visualize the point cloud
        o3d.visualization.draw_geometries([point_cloud],
                                          window_name="Point Cloud from .pkl",
                                          width=800,
                                          height=600)
    else:
        print("The .pkl file does not contain a numpy array.")

# Example usage
pcd_file_path = '/home/sudhujoshi/Desktop/Sem_4/MSD/a2/LIDAR/Common_Data/scan_team_common.pcd'
pkl_file_path = '/home/sudhujoshi/Desktop/Sem_4/MSD/a2/LIDAR/Common_Data/scan_vector_team_common_pkl'

# Visualize .pcd file
visualize_pcd(pcd_file_path)

# Visualize .pkl file
visualize_pkl(pkl_file_path)