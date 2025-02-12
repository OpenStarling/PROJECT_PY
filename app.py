import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Page settings
st.set_page_config(page_title="Three-Phase Separator", layout="wide")

st.title("Separator Sizing & 3D Visualization")

st.sidebar.header("🔹 Select Equation")

# Dictionary with different equation presets
equation_presets = {
    "Three Phase Horizontal": {
        "dm_liquid": 100.0,
        "dm_oil": 200.0,
        "dm_water": 500.0,
        "oil_density": 54.67,
        "p": 1000.0,
        "t": 600.0,
        "SGgas": 0.55,
        "orientation": "horizontal"
    },
    "Three Phase Vertical": {
        "dm_liquid": 120.0,
        "dm_oil": 220.0,
        "dm_water": 520.0,
        "oil_density": 55.0,
        "p": 950.0,
        "t": 620.0,
        "SGgas": 0.58,
        "orientation": "vertical"
    }
}

# Dropdown for equation selection
selected_equation = st.sidebar.selectbox("🔸 Choose Separator Type", list(equation_presets.keys()))

# Load default values based on selection
default_values = equation_presets[selected_equation]
orientation = default_values["orientation"]

# Sidebar input fields
st.sidebar.subheader("🔧 Input Parameters")
inputs = {
    "dm_liquid": st.sidebar.number_input(
        "💧 Droplet removal size (liquid in gas phase, microns)", min_value=1.0, value=default_values["dm_liquid"]
    ),
    "dm_oil": st.sidebar.number_input(
        "🛢 Droplet removal size (oil in water phase, microns)", min_value=1.0, value=default_values["dm_oil"]
    ),
    "dm_water": st.sidebar.number_input(
        "💦 Droplet removal size (water in oil phase, microns)", min_value=1.0, value=default_values["dm_water"]
    ),
    "oil_density": st.sidebar.number_input(
        "⚖ Oil density (lb/ft³)", min_value=1.0, value=default_values["oil_density"]
    ),
    "p": st.sidebar.number_input(
        "⏲ Pressure (psia)", min_value=0.0, value=default_values["p"]
    ),
    "t": st.sidebar.number_input(
        "🌡 Temperature (°R)", min_value=0.0, value=default_values["t"]
    ),
    "SGgas": st.sidebar.number_input(
        "🌬 Specific Gravity of Gas", min_value=0.0, value=default_values["SGgas"]
    )
}

# Button to trigger calculation
if st.sidebar.button("🚀 Start Calculation"):
    st.success("✅ Calculations Completed!")

    # Cylinder dimensions
    length_ft = 20  # Length of separator
    diameter_ft = 8  # Diameter of separator
    radius_ft = diameter_ft / 2

    # Generate Cylinder Mesh
    theta = np.linspace(0, 2 * np.pi, 50)
    z = np.linspace(0, length_ft, 50)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius_ft * np.cos(theta_grid)
    y_grid = radius_ft * np.sin(theta_grid)

    # Create Plotly figure
    fig = go.Figure()

    if orientation == "horizontal":
        fig.add_trace(go.Surface(x=z_grid, y=x_grid, z=y_grid, colorscale='Blues'))
        fig.update_layout(
            title="3D Horizontal Separator",
            scene=dict(
                xaxis_title='X (ft)',
                yaxis_title='Y (ft)',
                zaxis_title='Z (ft)'
            )
        )
    else:
        fig.add_trace(go.Surface(x=x_grid, y=y_grid, z=z_grid, colorscale='Blues'))
        fig.update_layout(
            title="3D Vertical Separator",
            scene=dict(
                xaxis_title='X (ft)',
                yaxis_title='Y (ft)',
                zaxis_title='Z (ft)'
            )
        )

    st.plotly_chart(fig, use_container_width=True)
