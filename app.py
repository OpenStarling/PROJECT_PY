import streamlit as st
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import time

# Page settings
st.set_page_config(page_title="Three-Phase Separator", layout="wide")

st.title("Separator sizing & 3D visualisation")

st.sidebar.header(" Input Data")

# Input data through the interface
inputs = {
    "dm_liquid": st.sidebar.number_input("Droplet removal size of liquid in gas phase (microns)", min_value=1.0),
    "dm_oil": st.sidebar.number_input("Droplet removal size of oil in water phase (microns)", min_value=1.0),
    "dm_water": st.sidebar.number_input("Droplet removal size of water in oil phase (microns)", min_value=1.0),
    "oil_density": st.sidebar.number_input("Oil density (lb/ft³)", min_value=1.0),
    "p": st.sidebar.number_input("Pressure (psia)", min_value=0.0),
    "t": st.sidebar.number_input("Temperature (°R)", min_value=0.0),
    "SGgas": st.sidebar.number_input("Specific Gravity of Gas", min_value=0.0),
    "Qg": st.sidebar.number_input("Gas Flowrate (MMscfd)", min_value=0.0),
    "SG_o": st.sidebar.number_input("Specific Gravity of Oil", min_value=0.0),
    "SG_w": st.sidebar.number_input("Specific Gravity of Water", min_value=0.0),
    "Qoil": st.sidebar.number_input("Oil Flowrate (BOPD)", min_value=1),
    "miuoil": st.sidebar.number_input("Oil Viscosity (cp)", min_value=1),
    "Qwater": st.sidebar.number_input("Water Flowrate (BWPD)", min_value=1.0),
    "miuwater": st.sidebar.number_input("Water Viscosity (cp)", min_value=1.0)
}

if st.sidebar.button("🚀 Start Calculation"):
    with open("input_data.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{value}\n")

    # Run the original Python script
    with st.spinner("Calculating..."):
        time.sleep(2)  # Simulating processing time
        result = subprocess.run(["python3", "threephasevertical(2).py"], capture_output=True, text=True)
        st.text(result.stdout)

    st.success("✅ Calculations Completed!")
    
    # 3D Visualization of Cylinder (Increased Size)
    length_ft = 20  # Increased length
    diameter_ft = 4  # Increased diameter
    radius_ft = diameter_ft / 2
    theta = np.linspace(0, 2 * np.pi, 40)
    z = np.linspace(0, length_ft, 40)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius_ft * np.cos(theta_grid)
    y_grid = radius_ft * np.sin(theta_grid)
    fig = go.Figure(data=[go.Surface(x=x_grid, y=y_grid, z=z_grid, colorscale='Blues')])
    fig.update_layout(
        title="3D Cylinder (Enlarged)",
        title_font_color="white",
        scene=dict(
            xaxis_title='X (ft)',
            yaxis_title='Y (ft)',
            zaxis_title='Z (ft)',
            xaxis=dict(backgroundcolor='#0E1117', color='white'),
            yaxis=dict(backgroundcolor='#0E1117', color='white'),
            zaxis=dict(backgroundcolor='#0E1117', color='white')
        ),
        paper_bgcolor='#0E1117',
        font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True)

