import folium
import streamlit as st
from streamlit_folium import st_folium

from src.controllers.dashboard_controller import DashboardController

c = DashboardController()
dados = c.rodar_consulta_trajeto_onibus(codigo_linha='4027-41')

st.set_page_config(page_title="Mapa PolyLine", layout="wide")
st.title("🗺️ PolyLine com Folium")

polyline_points = [(lat, lon) for lat, lon, cor in dados]

# Pegar a cor da linha (todas iguais)
cor_hex = f"#{dados[0][2]}"

# Centralizar no primeiro ponto
map_center = polyline_points[0]

# Criar mapa
m = folium.Map(location=map_center, zoom_start=15)

# Converter para lista somente de (lat, lon)
polyline_points = [(lat, lon) for lat, lon, cor in dados]

# Pegar a cor da linha (todas iguais)


# Centralizar no primeiro ponto
map_center = polyline_points[0]

# Criar mapa
m = folium.Map(location=map_center, zoom_start=15)

# Adicionar polyline
folium.PolyLine(
    polyline_points,
    weight=5,
    color=cor_hex,
    opacity=0.9
).add_to(m)

# Mostrar no Streamlit
st_folium(m, width=900, height=900, returned_objects=[])
