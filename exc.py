import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="PolyLine Folium", layout="wide")

st.title("🗺️ Exemplo PolyLine no Streamlit")

# Coordenadas exemplo
coords = [
    (-23.619791, -46.460614),
    (-23.628900, -46.455200),
    (-23.638659, -46.450100)
]

# Criar o mapa
m = folium.Map(location=coords[0], zoom_start=13)

# Adicionar marcador inicial
folium.Marker(location=coords[0], tooltip="Início").add_to(m)

# Adicionar linha
folium.PolyLine(
    locations=coords,
    weight=5,
    opacity=0.8,
    color="blue"
).add_to(m)

# Renderizar no Streamlit
st_folium(m, width=900, height=600)
