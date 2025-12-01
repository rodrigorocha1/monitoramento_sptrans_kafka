import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import time
import math

st.set_page_config(page_title="Simulador Ônibus Folium", layout="wide")

st.title("🚌 Simulação de posição de ônibus usando Folium")

# Rota (exemplo São Paulo)
ROUTE = [
    (-23.550520, -46.633308),
    (-23.551000, -46.630000),
    (-23.552000, -46.625000),
    (-23.553500, -46.620000),
    (-23.555000, -46.615000),
    (-23.556500, -46.610000),
    (-23.558000, -46.605000),
    (-23.559500, -46.600000),
    (-23.561000, -46.595000)
]

# -----------------------------------------------
# Funções auxiliares
# -----------------------------------------------

def inicializar(n):
    st.session_state.positions = []
    for i in range(n):
        idx = (i / n) * (len(ROUTE) - 1)
        st.session_state.positions.append({"idx": idx})

def idx_to_latlon(idx):
    if idx >= len(ROUTE) - 1:
        idx = idx % (len(ROUTE) - 1)
    low = int(idx)
    high = low + 1
    frac = idx - low
    lat1, lon1 = ROUTE[low]
    lat2, lon2 = ROUTE[high]
    return (
        lat1 + (lat2 - lat1) * frac,
        lon1 + (lon2 - lon1) * frac
    )

def simular(speed):
    for p in st.session_state.positions:
        p["idx"] += speed
        if p["idx"] >= len(ROUTE) - 1:
            p["idx"] = p["idx"] % (len(ROUTE) - 1)

# -----------------------------------------------
# Sidebar
# -----------------------------------------------
with st.sidebar:
    st.header("Controles")

    num = st.slider("Número de ônibus", 1, 20, 5)
    speed = st.slider("Velocidade", 0.01, 0.3, 0.05)

    if "positions" not in st.session_state:
        inicializar(num)

    if st.button("Reset"):
        inicializar(num)
        st.rerun()

    step = st.button("Step")
    animate = st.checkbox("Animar automaticamente")
    passos = st.number_input("Passos da animação", 1, 500, 100)

# -----------------------------------------------
# Ações
# -----------------------------------------------
if step:
    simular(speed)
    st.rerun()

if animate:
    for _ in range(passos):
        simular(speed)
        time.sleep(0.3)
        st.rerun()

# -----------------------------------------------
# Construir mapa Folium
# -----------------------------------------------
lat0, lon0 = ROUTE[0]
m = folium.Map(location=[lat0, lon0], zoom_start=14)

# rota
folium.PolyLine(ROUTE, color="blue", weight=4).add_to(m)

# marcadores dos ônibus
dados = []
for i, p in enumerate(st.session_state.positions):
    lat, lon = idx_to_latlon(p["idx"])
    dados.append({"bus": f"Ônibus {i+1}", "lat": lat, "lon": lon})

    folium.Marker(
        [lat, lon],
        tooltip=f"Ônibus {i+1}",
        icon=folium.Icon(color="red", icon="bus", prefix="fa")
    ).add_to(m)

st_folium(m, width=900, height=550)

st.subheader("Posições dos ônibus")
st.write(pd.DataFrame(dados))
