import plotly.graph_objects as go
import numpy as np

# Sample Data
np.random.seed(42)  # For consistent results
x_data = np.random.rand(100) * 10  # Random X values
y_data = np.random.rand(100) * 10  # Random Y values
z_data = np.random.rand(100) * 10  # Random Z values
color_data = np.random.rand(100)  # Random color scale

# Create the 3D scatter plot
fig = go.Figure()

fig.add_trace(go.Scatter3d(
    x=x_data,
    y=y_data,
    z=z_data,
    mode='markers',
    marker=dict(
        size=5,
        color=color_data,  # Color mapped to data
        colorscale='Viridis',  # Choose a colorscale
        opacity=0.7  # ✅ Corrected property
    )
))

# Layout settings
fig.update_layout(
    title="3D Scatter Plot",
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis'
    )
)

# Show the figure
fig.show()
