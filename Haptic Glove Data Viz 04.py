import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import make_interp_spline

# Load dataset
data = pd.read_csv("haptic_glove_dataset.csv")

# Normalize and scale sensor data
accel_scale = 50
x = data["AccX"] * accel_scale
y = data["AccY"] * accel_scale
z = data["AccZ"] * accel_scale
time = data["Time"]

# Interpolation for smooth curves
t_new = np.linspace(time.min(), time.max(), 5 * len(time))  # More points for smoothness
x_smooth = make_interp_spline(time, x, k=3)(t_new)
y_smooth = make_interp_spline(time, y, k=3)(t_new)
z_smooth = make_interp_spline(time, z, k=3)(t_new)

# Generate dynamic line properties
num_points = len(t_new)
opacity_values = np.linspace(0.3, 1, num_points)  # Trail fade effect
width_values = np.linspace(1, 6, num_points)  # Dynamic thickness
color_values = np.linspace(0, 1, num_points).tolist()  # Convert NumPy array to list

# Create figure
fig = go.Figure()

# Add motion trail segments for dynamic width effect
for i in range(1, num_points):
    fig.add_trace(go.Scatter3d(
        x=[x_smooth[i - 1], x_smooth[i]],
        y=[y_smooth[i - 1], y_smooth[i]],
        z=[z_smooth[i - 1], z_smooth[i]],
        mode="lines",
        line=dict(
            color=color_values[i],  # Gradient color
            colorscale="plasma",
            width=width_values[i]  # Dynamic thickness
        ),
        opacity=opacity_values[i]  # Apply opacity per trace
    ))

# Add motion points (without per-marker opacity to avoid error)
fig.add_trace(go.Scatter3d(
    x=x_smooth, y=y_smooth, z=z_smooth,
    mode="markers",
    marker=dict(
        size=4,
        color=color_values,  # Time-based coloring
        colorscale="plasma"
    ),
    opacity=0.8  # Fixed opacity to avoid NumPy array issue
))

# Dark theme
fig.update_layout(
    template="plotly_dark",
    title="3D Motion Trails (Smooth Kinetic Blur)",
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        bgcolor="black"
    ),
    margin=dict(l=0, r=0, t=50, b=0)
)

fig.show()
