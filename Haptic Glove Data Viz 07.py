import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.spatial import ConvexHull, Delaunay

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

# Compute the Convex Hull (outermost shape)
hull = ConvexHull(points)

# Compute Delaunay triangulation (for structured interior points)
tri = Delaunay(points)

# **Create figure**
fig = go.Figure()

# **Outer Surface - Highly Detailed Mesh**
fig.add_trace(go.Mesh3d(
    x=x, y=y, z=z,
    i=hull.simplices[:, 0],
    j=hull.simplices[:, 1],
    k=hull.simplices[:, 2],
    opacity=0.55,  # Transparent but visible
    intensity=np.linspace(0, 1, len(x)),
    colorscale=[(0, "midnightblue"), (0.4, "purple"), (1, "hotpink")],  # More glow effect
    showscale=False
))

# **Interior - Webbed Structure Using Delaunay Triangulation**
for simplex in tri.simplices:
    fig.add_trace(go.Scatter3d(
        x=points[simplex, 0],
        y=points[simplex, 1],
        z=points[simplex, 2],
        mode='lines',
        line=dict(color='rgba(255,255,255,0.1)', width=0.5)  # Subtle inner webbing
    ))

# **Fine Dust-Like Internal Particles**
fig.add_trace(go.Scatter3d(
    x=x[::5], y=y[::5], z=z[::5],  # More internal points
    mode='markers',
    marker=dict(
        size=2.5,
        color="white",
        opacity=0.15  # Subtle visibility
    )
))

# **Styling Updates for a Dark Sci-Fi Look**
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
