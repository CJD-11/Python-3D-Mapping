import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.spatial import ConvexHull

# Load dataset
file_path = "haptic_glove_dataset.csv"
data = pd.read_csv(file_path)

# Normalize and scale sensor data
accel_scale = 50
x = data["AccX"] * accel_scale
y = data["AccY"] * accel_scale
z = data["AccZ"] * accel_scale

# Stack points into an array
points = np.column_stack((x, y, z))

# Compute the Convex Hull (outermost shell)
hull = ConvexHull(points)

# Create figure
fig = go.Figure()

# **Outer transparent shell**
fig.add_trace(go.Mesh3d(
    x=x, y=y, z=z,
    i=hull.simplices[:, 0],
    j=hull.simplices[:, 1],
    k=hull.simplices[:, 2],
    opacity=0.5,  # Semi-transparent for depth
    intensity=np.linspace(0, 1, len(x)),  # Gradient effect
    colorscale="magma",
    showscale=False
))

# **Minimal interior points (simple depth)**
fig.add_trace(go.Scatter3d(
    x=x[::10], y=y[::10], z=z[::10],  # Reduce density of inside points
    mode='markers',
    marker=dict(
        size=2,
        color="white",
        opacity=0.08  # Faint but visible
    )
))

# **Styling updates**
fig.update_layout(
    template="plotly_dark",
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False)
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    paper_bgcolor="black"
)

fig.show()
