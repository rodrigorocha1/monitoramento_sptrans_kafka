import folium
import streamlit as st
from streamlit_folium import st_folium

from src.controllers.dashboard_controller import DashboardController


class Dashboard:
    st.set_page_config(page_title="Monitor de Ônibus", layout="wide")
    st.title("🚌 Monitoramento em Tempo Real – Live Tracking")

    def __init__(self):
        self.__controler = DashboardController()

        # GUARDA as coordenadas entre reruns
        if "coords" not in st.session_state:
            st.session_state.coords = None

    def gerar_inputs(self):
        codigo_linha = st.text_input("Código da linha:", "4027-41")
        intervalo = st.slider(
            "Intervalo de atualização da posição (manual)",
            1, 300, 150
        )
        return codigo_linha, intervalo

    def gerar_dados(self, codigo_linha: str, intervalo: int):
        if st.button("Iniciar monitoramento"):
            dados = self.__controler.rodar_consulta_trajeto_onibus(codigo_linha=codigo_linha)
            tracado_linha = [(lat, lon) for lat, lon, cor in dados]
            cor_tracao_linha_hex = f"#{dados[0][2]}"
            centro_mapa = tracado_linha[0]
            mapa = folium.Map(location=centro_mapa, zoom_start=15)
            folium.PolyLine(
                tracado_linha,
                weight=5,
                color=cor_tracao_linha_hex,
                opacity=0.9
            ).add_to(mapa)


            st_folium(mapa, width=900, height=900, returned_objects=[])

    def rodar_dashboard(self):
        codigo_linha, intervalo = self.gerar_inputs()
        self.gerar_dados(codigo_linha, intervalo)
