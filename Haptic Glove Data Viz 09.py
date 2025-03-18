import pandas as pd
import numpy as np
import trimesh
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Load dataset
file_path = "C:\\Users\\dziad\\PyCharmMiscProject\\haptic_glove_dataset.csv"
data = pd.read_csv(file_path)

# Load 3D model with materials and textures
obj_path = "C:\\Users\\dziad\\PyCharmMiscProject\\3_16_2025.obj"
mtl_path = "C:\\Users\\dziad\\PyCharmMiscProject\\3_16_2025.mtl"
texture_dir = "C:\\Users\\dziad\\PyCharmMiscProject\\textures"

# Load mesh with textures
mesh = trimesh.load_mesh(obj_path, process=True)

# Extract mesh vertices and faces
vertices = mesh.vertices
faces = mesh.faces

# Normalize and scale sensor data
accel_scale = 50
x = data["AccX"] * accel_scale
y = data["AccY"] * accel_scale
z = data["AccZ"] * accel_scale

# ----------------- PLOTTING -----------------
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot textured 3D object
mesh_collection = Poly3DCollection(vertices[faces], alpha=0.85, facecolor='gray', edgecolor='none')
ax.add_collection3d(mesh_collection)

# Plot motion data inside the 3D model
ax.scatter(x, y, z, c='red', s=5, alpha=0.5, label="Motion Data")

# Set equal axis limits
ax.set_xlim(vertices[:, 0].min(), vertices[:, 0].max())
ax.set_ylim(vertices[:, 1].min(), vertices[:, 1].max())
ax.set_zlim(vertices[:, 2].min(), vertices[:, 2].max())

# Dark mode styling (Fixed AttributeError)
ax.set_facecolor("black")
ax.xaxis.pane.set_edgecolor("none")  # Hide X-axis pane edges
ax.yaxis.pane.set_edgecolor("none")  # Hide Y-axis pane edges
ax.zaxis.pane.set_edgecolor("none")  # Hide Z-axis pane edges

plt.title("3D Mapped Object with Motion Data", color="white")
plt.legend()
plt.show()
