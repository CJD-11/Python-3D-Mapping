import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial import Delaunay

# Load dataset
dataset_path = "haptic_glove_dataset.csv"  # Update path as needed
data = pd.read_csv(dataset_path)

# Normalize acceleration values for visualization
accel_scale = 10
x = data["AccX"] * accel_scale
y = data["AccY"] * accel_scale
z = data["AccZ"] * accel_scale
time = data["Time"]

# Identify haptic feedback points
haptic_active = data["Haptic"] == 1

# Generate wireframe connections using Delaunay triangulation
points = np.vstack((x, y, z)).T
tri = Delaunay(points)

### Static 3D Visualization ###
fig_static = plt.figure(figsize=(8, 6))
ax_static = fig_static.add_subplot(111, projection='3d')

# Plot points
ax_static.scatter(x, y, z, c=time, cmap="viridis", s=5)
ax_static.scatter(x[haptic_active], y[haptic_active], z[haptic_active], c='r', s=20, label="Haptic Feedback")

# Draw wireframe
for simplex in tri.simplices:
    ax_static.plot(x[simplex], y[simplex], z[simplex], 'k-', alpha=0.5)

ax_static.set_xlabel("AccX")
ax_static.set_ylabel("AccY")
ax_static.set_zlabel("AccZ")
ax_static.set_title("Static 3D Sensor Data with Wireframe")
ax_static.legend()
plt.show()

### Animated 3D Visualization ###
fig_animated = plt.figure(figsize=(8, 6))
ax_animated = fig_animated.add_subplot(111, projection='3d')


def update(frame):
    ax_animated.clear()

    # Plot partial data up to the current frame
    ax_animated.scatter(x[:frame], y[:frame], z[:frame], c=time[:frame], cmap="viridis", s=5)
    ax_animated.scatter(x[haptic_active][:frame], y[haptic_active][:frame], z[haptic_active][:frame], c='r', s=20)

    # Draw wireframe progressively
    for simplex in tri.simplices[:frame]:
        ax_animated.plot(x[simplex], y[simplex], z[simplex], 'k-', alpha=0.5)

    ax_animated.set_xlabel("AccX")
    ax_animated.set_ylabel("AccY")
    ax_animated.set_zlabel("AccZ")
    ax_animated.set_title(f"3D Sensor Data Over Time (Frame {frame})")


ani = animation.FuncAnimation(fig_animated, update, frames=len(time), interval=50)
plt.show()
