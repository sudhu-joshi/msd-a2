import numpy as np
import cv2

# Depth range for normalization
min_depth, max_depth = 0.1, 10.0

# File paths
input_depth_matrix_path = "/home/sudhujoshi/Desktop/Sem_4/MSD/a2/ZEDCAM/ZED_data/lab2_depth_matrix.npy"  # Input depth matrix
output_ply_path = "/home/sudhujoshi/Desktop/Sem_4/MSD/a2/ZEDCAM/ZED_data/lab2_point_cloud.ply"  # Output PLY file
color_1_image_path = "/home/sudhujoshi/Desktop/Sem_4/MSD/a2/ZEDCAM/ZED_data/lab2_color.png"  # Color image

def create_ply_from_depth(depth_matrix, color_image, output_ply_path):
    """Create a PLY point cloud file from depth matrix without external libraries"""
    height, width = depth_matrix.shape
    
    # Define camera intrinsics (specific to your ZED camera)
    fx, fy = 957.08, 957.08  # Focal length in pixels
    cx, cy = 649.15, 370.98  # Principal point
    
    # Create arrays for storing the 3D points and colors
    points = []
    
    # Generate 3D points from depth map
    for v in range(height):
        for u in range(width):
            z = depth_matrix[v, u]  # Depth value
            
            # Skip invalid depth values
            if z <= 0 or z > max_depth:
                continue
            
            # Convert from image coordinates to 3D world coordinates
            x = (u - cx) * z / fx
            y = (v - cy) * z / fy
            
            # Get color for this point
            if color_image is not None:
                b, g, r = color_image[v, u]  # BGR format from OpenCV
            else:
                r, g, b = 128, 128, 128  # Default gray color
            
            # Add point and color to lists
            points.append((x, y, z, r, g, b))
    
    # Write PLY file manually
    with open(output_ply_path, 'w') as f:
        # Write header
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {len(points)}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("end_header\n")
        
        # Write vertex data
        for x, y, z, r, g, b in points:
            f.write(f"{x:.6f} {y:.6f} {z:.6f} {int(r)} {int(g)} {int(b)}\n")
    
    print(f"Point cloud saved to {output_ply_path}")
    print(f"Total points in cloud: {len(points)}")

if __name__ == "__main__":
    # Load depth matrix from .npy file
    depth_matrix = np.load(input_depth_matrix_path)
    
    # Load color image
    color_1_image = cv2.imread(color_1_image_path)

    if depth_matrix is not None:
        # Create PLY point cloud
        create_ply_from_depth(depth_matrix, color_1_image, output_ply_path)

# import numpy as np
# import cv2

# # Depth range for normalization
# min_depth, max_depth = 0.1, 10.0

# # File paths
# input_heatmap_path = "/home/sudhujoshi/Desktop/Sem_4/MSD/a2/ZEDCAM/ZED_data/lab2_depth_heatmap.png" # Input heatmap
# output_depth_matrix_path = "/home/sudhujoshi/Desktop/Sem_4/MSD/a2/ZEDCAM/ZED_data/lab2_depth_matrix.npy" # Output depth matrix
# output_ply_path = "/home/sudhujoshi/Desktop/Sem_4/MSD/a2/ZEDCAM/ZED_data/lab2_point_cloud.ply" # Output PLY file
# color_1_image_path = "/home/sudhujoshi/Desktop/Sem_4/MSD/a2/ZEDCAM/ZED_data/lab2_color.png"

# def convert_heatmap_to_depth_matrix(heatmap_path, output_path):
#     # Load heatmap as a BGR image
#     heatmap_bgr = cv2.imread(heatmap_path)
#     if heatmap_bgr is None:
#         print("Error: Unable to load heatmap image.")
#         return None
    
#     # Convert BGR to HSV
#     heatmap_hsv = cv2.cvtColor(heatmap_bgr, cv2.COLOR_BGR2HSV)

    
#     # Extract the Hue channel (depth information)
#     hue_channel = heatmap_hsv[:, :, 0].astype(np.float32) # OpenCV stores hue in [0, 180]
    
#     # Normalize depth from [0, 180] to [0.1m, 10m]
#     depth_matrix = (1-(hue_channel/180)) * (max_depth - min_depth) + min_depth

#     # Save as .npy file
#     np.save(output_path, depth_matrix)
#     print(f"Depth matrix saved to {output_path}")
    
#     return depth_matrix, heatmap_bgr

# def create_ply_from_depth(depth_matrix, color_image, output_ply_path):
#     """Create a PLY point cloud file from depth matrix without external libraries"""
#     height, width = depth_matrix.shape
    
#     # Define camera intrinsics (specific to your ZED camera)
#     fx, fy = 957.08, 957.08  # Focal length in pixels
#     cx, cy = 649.15, 370.98  # Principal point
    
#     # Create arrays for storing the 3D points and colors
#     points = []
    
#     # Generate 3D points from depth map
#     for v in range(height):
#         for u in range(width):
#             z = depth_matrix[v, u]  # Depth value
            
#             # Skip invalid depth values
#             if z <= 0 or z > max_depth:
#                 continue
            
#             # Convert from image coordinates to 3D world coordinates
#             x = (u - cx) * z / fx
#             y = (v - cy) * z / fy
            
#             # Get color for this point
#             if color_image is not None:
#                 b, g, r = color_image[v, u]  # BGR format from OpenCV
#             else:
#                 r, g, b = 128, 128, 128  # Default gray color
            
#             # Add point and color to lists
#             points.append((x, y, z, r, g, b))
    
#     # Write PLY file manually
#     with open(output_ply_path, 'w') as f:
#         # Write header
#         f.write("ply\n")
#         f.write("format ascii 1.0\n")
#         f.write(f"element vertex {len(points)}\n")
#         f.write("property float x\n")
#         f.write("property float y\n")
#         f.write("property float z\n")
#         f.write("property uchar red\n")
#         f.write("property uchar green\n")
#         f.write("property uchar blue\n")
#         f.write("end_header\n")
        
#         # Write vertex data
#         for x, y, z, r, g, b in points:
#             f.write(f"{x:.6f} {y:.6f} {z:.6f} {int(r)} {int(g)} {int(b)}\n")
    
#     print(f"Point cloud saved to {output_ply_path}")
#     print(f"Total points in cloud: {len(points)}")

# if __name__ == "__main__":
#     # Convert heatmap to depth matrix and get the original color image
#     depth_matrix, color_image = convert_heatmap_to_depth_matrix(input_heatmap_path, output_depth_matrix_path)
    
#     color_1_image = cv2.imread(color_1_image_path)

#     if depth_matrix is not None:
#         # Create PLY point cloud
#         create_ply_from_depth(depth_matrix, color_1_image, output_ply_path)