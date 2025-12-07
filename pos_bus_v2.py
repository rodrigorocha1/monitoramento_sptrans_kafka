import json
from datetime import datetime
import folium
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium

from src.servicos.ksql_api import KsqlApi
from src.controllers.dashboard_controller import DashboardController

st.set_page_config(page_title="Monitor de Ônibus", layout="wide")

ksql_api = KsqlApi()
controller = DashboardController()

# Estado inicial
if "monitorando" not in st.session_state:
    st.session_state.monitorando = False

st.title("🚌 Monitoramento em Tempo Real – Live Tracking")

# Entrada do usuário
codigo_linha = st.text_input("Código da linha:", "4027-41")
intervalo = st.slider("Intervalo de atualização (segundos)", 1, 300, 150)

# Botão
if st.button("Iniciar monitoramento"):
    st.session_state.monitorando = True

# Se monitorando, ativa autorefresh
if st.session_state.monitorando:
    st_autorefresh(interval=intervalo * 1000, key="refresh")
    print(f'Atualizei as {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}')

    dados = ksql_api.obter_posicao_atual(codigo_linha)

    if not dados:
        st.warning("Nenhuma posição encontrada.")
        st.stop()


    dados_tracado = controller.rodar_consulta_trajeto_onibus(codigo_linha=codigo_linha)

    tracado_linha = [(lat, lon) for lat, lon, cor in dados_tracado]


    cor_tracado_hex = f"#{dados_tracado[0][2]}"


    ultimo = dados[-1]

    st.write(f"### Atualizado em: **{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}**")
    st.write(f"Próxima atualização em: **{intervalo} segundos**")

    col1, col2 = st.columns([2, 1])


    with col1:
        mapa = folium.Map(
            location=[ultimo["py"], ultimo["px"]],
            zoom_start=14
        )


        folium.PolyLine(
            tracado_linha,
            weight=5,
            color=cor_tracado_hex,
            opacity=0.9
        ).add_to(mapa)

        for item in dados:
            folium.Marker(
                [item["py"], item["px"]],
                tooltip=f"Ônibus {item['id_onibus']}",
                popup=f"{item}",
                icon=folium.Icon(color="blue", icon="bus", prefix="fa")
            ).add_to(mapa)

        st_folium(mapa, width=900, height=700, returned_objects=[])


    with col2:
        st.write("### Dados dos Ônibus")
        tabela = [
            {
                "ID": d["id_onibus"],
                "Latitude": f"{d['py']}",
                "Longitude": f"{d['px']}",
                "Horário": d["ta"]
            }
            for d in dados
        ]

        st.code(json.dumps(tabela, indent=4, ensure_ascii=False), language="json")
