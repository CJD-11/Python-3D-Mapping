import pandas as pd
import numpy as np
import trimesh
import open3d as o3d

# Load dataset
file_path = "C:\\Users\\dziad\\PyCharmMiscProject\\haptic_glove_dataset.csv"
data = pd.read_csv(file_path)

# Load 3D model
obj_path = "C:\\Users\\dziad\\PyCharmMiscProject\\3_16_2025.obj"
mesh = trimesh.load_mesh(obj_path, process=True)

# Check if mesh loaded
print(f"Number of vertices: {len(mesh.vertices)}")
print(f"Number of faces: {len(mesh.faces)}")

# Convert to Open3D mesh
o3d_mesh = o3d.geometry.TriangleMesh()
o3d_mesh.vertices = o3d.utility.Vector3dVector(mesh.vertices)
o3d_mesh.triangles = o3d.utility.Vector3iVector(mesh.faces)

# Apply color so it's visible
o3d_mesh.compute_vertex_normals()  # Fix normals
o3d_mesh.paint_uniform_color([0.5, 0.5, 0.5])  # Gray color

# Scale to fit
o3d_mesh.scale(0.1, center=o3d_mesh.get_center())

# Normalize and scale motion data
accel_scale = 50
x = data["AccX"] * accel_scale
y = data["AccY"] * accel_scale
z = data["AccZ"] * accel_scale

# Create motion data as red points
motion_points = np.vstack((x, y, z)).T
motion_pcd = o3d.geometry.PointCloud()
motion_pcd.points = o3d.utility.Vector3dVector(motion_points)
motion_pcd.paint_uniform_color([1, 0, 0])  # Red color
motion_pcd.scale(0.1, center=motion_pcd.get_center())  # Match scaling

# Visualize
vis = o3d.visualization.Visualizer()
vis.create_window(window_name="3D Object with Motion Data")
vis.add_geometry(o3d_mesh)  # Add object
vis.add_geometry(motion_pcd)  # Add red points
vis.run()
vis.destroy_window()
