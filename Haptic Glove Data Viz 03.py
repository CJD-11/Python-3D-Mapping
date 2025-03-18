import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load dataset
data = pd.read_csv("haptic_glove_dataset.csv")

# Normalize and scale sensor data
accel_scale = 50
x = data["AccX"] * accel_scale
y = data["AccY"] * accel_scale
z = data["AccZ"] * accel_scale
time = data["Time"]

# Generate motion trail effect by fading older points
trail_opacity = np.linspace(0.2, 1, len(time))  # Older points are more transparent
color_gradient = np.linspace(0, 1, len(time))   # Gradient color mapping

fig = go.Figure()

# Add lines connecting points for "motion blur" effect
fig.add_trace(go.Scatter3d(
    x=x, y=y, z=z,
    mode='lines',
    line=dict(
        width=3
    ),
    marker=dict(
        color=color_gradient,  # Correct gradient color usage
        colorscale="plasma"
    ),
    opacity=0.7
))

# Add moving points
fig.add_trace(go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers',
    marker=dict(
        size=5,
        color=color_gradient,  # Correct gradient color usage
        colorscale="plasma",
        opacity=0.7  # Set as scalar (not array)
    )
))

fig.update_layout(
    title="3D Motion Trails (Kinetic Long Exposure)",
    scene=dict(
        xaxis_title="X Axis",
        yaxis_title="Y Axis",
        zaxis_title="Z Axis"
    )
)

fig.show()
