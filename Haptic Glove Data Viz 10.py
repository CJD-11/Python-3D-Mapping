import pandas as pd
import numpy as np
import trimesh
import open3d as o3d
import os

# Load dataset
file_path = "C:\\Users\\dziad\\PyCharmMiscProject\\haptic_glove_dataset.csv"
data = pd.read_csv(file_path)

# Load 3D model with textures
obj_path = "C:\\Users\\dziad\\PyCharmMiscProject\\3_16_2025.obj"
mesh = trimesh.load_mesh(obj_path, process=True)

# Convert Trimesh mesh to Open3D format
o3d_mesh = o3d.geometry.TriangleMesh()
o3d_mesh.vertices = o3d.utility.Vector3dVector(mesh.vertices)
o3d_mesh.triangles = o3d.utility.Vector3iVector(mesh.faces)

# Try to apply texture if available
if isinstance(mesh.visual, trimesh.visual.TextureVisuals) and mesh.visual.material:
    texture_image = mesh.visual.material.image  # Get texture image

    if texture_image is not None:
        print("✅ Textures detected, applying them!")
        o3d_texture = o3d.geometry.Image(np.asarray(texture_image))

        # Open3D requires a separate UV coordinate array
        if hasattr(mesh.visual, "uv") and mesh.visual.uv is not None:
            o3d_mesh.triangle_uvs = o3d.utility.Vector2dVector(mesh.visual.uv)

        # Set texture map
        o3d_mesh.textures = [o3d_texture]
    else:
        print("⚠ No valid texture image found, displaying mesh in solid color.")
else:
    print("⚠ No texture detected, rendering as a solid color.")

# Normalize and scale sensor data
accel_scale = 50
x = data["AccX"] * accel_scale
y = data["AccY"] * accel_scale
z = data["AccZ"] * accel_scale

# Create point cloud for motion data
motion_points = np.vstack((x, y, z)).T
motion_pcd = o3d.geometry.PointCloud()
motion_pcd.points = o3d.utility.Vector3dVector(motion_points)
motion_pcd.paint_uniform_color([1, 0, 0])  # Red color for motion data

# Create Open3D visualization window
vis = o3d.visualization.Visualizer()
vis.create_window(window_name="3D Object with Motion Data")

# Add mesh and motion data
vis.add_geometry(o3d_mesh)
vis.add_geometry(motion_pcd)

# Run visualization
vis.run()
vis.destroy_window()
