import streamlit as st

# ✅ Должно быть первой командой
st.set_page_config(page_title="Трехфазный сепаратор", layout="wide")

import subprocess
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import time

st.title("🔬 Визуализация расчётов трехфазного сепаратора")

st.sidebar.header("🔧 Ввод данных")

# Ввод данных через интерфейс
inputs = {
    "dm_liquid": st.sidebar.number_input("Droplet removal size of liquid in gas phase (microns)", min_value=1.0),
    "dm_oil": st.sidebar.number_input("Droplet removal size of oil in water phase (microns)", min_value=1.0),
    "dm_water": st.sidebar.number_input("Droplet removal size of water in oil phase (microns)", min_value=1.0),
    "oil_density": st.sidebar.number_input("Oil density (lb/ft³)", min_value=1.0),
    "p": st.sidebar.number_input("Pressure (psia)", min_value=0.0),
    "t": st.sidebar.number_input("Temperature (°R)", min_value=0.0),
    "SGgas": st.sidebar.number_input("SG of gas", min_value=0.0),
    "Qg": st.sidebar.number_input("Gas Flowrate (MMscfd)", min_value=0.0),
    "SG_o": st.sidebar.number_input("SG oil", min_value=0.0),
    "SG_w": st.sidebar.number_input("SG water", min_value=0.0),
    "Qoil": st.sidebar.number_input("Oil flowrate (BOPD)", min_value=1),
    "miuoil": st.sidebar.number_input("Oil viscosity (cp)", min_value=1),
    "Qwater": st.sidebar.number_input("Water flowrate (BWPD)", min_value=1.0),
    "miuwater": st.sidebar.number_input("Viscosity of water (cp)", min_value=1.0)
}

if st.sidebar.button("🚀 Запустить расчёт"):
    with open("input_data.txt", "w") as f:
        for key, value in inputs.items():
            f.write(f"{value}\n")

    # Запуск оригинального Python-скрипта
    with st.spinner("Выполняется расчет..."):
        time.sleep(2)  # Эмуляция загрузки
        result = subprocess.run(["python3", "threephasevertical(2).py"], capture_output=True, text=True)
        st.text(result.stdout)

    st.success("✅ Расчёты завершены!")
    
    
    # 3D Визуализация цилиндра (увеличенный размер)
    length_ft = 20  # Увеличенная длина
    diameter_ft = 4  # Увеличенный диаметр
    radius_ft = diameter_ft / 2
    theta = np.linspace(0, 2 * np.pi, 40)
    z = np.linspace(0, length_ft, 40)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius_ft * np.cos(theta_grid)
    y_grid = radius_ft * np.sin(theta_grid)
    fig = go.Figure(data=[go.Surface(x=x_grid, y=y_grid, z=z_grid, colorscale='Blues')])
    fig.update_layout(
        title="3D Цилиндр (увеличенный)",
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
    
    
    # Визуализация графика Cd от Re (уменьшенный, с фоном контейнера и бело-синими подписями)
    fig, ax = plt.subplots(figsize=(4, 3))  # Уменьшенный размер
    fig.patch.set_facecolor('#0E1117')  # Фон совпадает с контейнером
    ax.set_facecolor('#0E1117')  # Фон осей
    ax.plot([1, 2, 3], [1, 4, 9], marker='o', linestyle='-', color='b', label='Пример')
    ax.set_xlabel("Re", color='white')
    ax.set_ylabel("Cd", color='white')
    ax.tick_params(colors='white')
    ax.legend(facecolor='#1B1F2A', edgecolor='white', labelcolor='white')
    st.pyplot(fig)
