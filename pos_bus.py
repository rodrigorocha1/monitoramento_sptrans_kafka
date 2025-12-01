import streamlit as st
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
import folium

from src.servicos.ksql_api import KsqlApi


st.set_page_config(page_title="Monitor de Ônibus", layout="wide")

ksql_api = KsqlApi()

# Estado inicial
if "monitorando" not in st.session_state:
    st.session_state.monitorando = False

st.title("🚌 Monitoramento em Tempo Real – Live Tracking")

# Entrada do usuário
codigo_linha = st.text_input("Código da linha:", "4027-41")
intervalo = st.slider("Intervalo de atualização (segundos)", 1, 60, 60)

# Botão
if st.button("Iniciar monitoramento"):
    st.session_state.monitorando = True

# Se monitorando, ativa autorefresh
if st.session_state.monitorando:
    st_autorefresh(interval=intervalo * 1000, key="refresh")

    dados = ksql_api.obter_posicao_atual(codigo_linha)

    if not dados:
        st.warning("Nenhuma posição encontrada.")
        st.stop()

    # último registro
    ultimo = dados[-1]

    st.write(f"### Atualizado em: **{ultimo['ta']}**")
    st.write(f"Próxima atualização em: **{intervalo} segundos**")

    col1, col2 = st.columns([2, 1])

    # MAPA
    with col1:
        mapa = folium.Map(
            location=[ultimo["py"], ultimo["px"]],
            zoom_start=14
        )

        for item in dados:
            folium.Marker(
                [item["py"], item["px"]],
                tooltip=f"Ônibus {item['id_onibus']}",
                popup=f"{item}",
                icon=folium.Icon(color="blue", icon="bus", prefix="fa")
            ).add_to(mapa)

        st_folium(mapa, width=900, height=500)

    # TABELA
    with col2:
        st.write("### Dados dos Ônibus")
        tabela = [
            {
                "ID": d["id_onibus"],
                "Latitude": d["py"],
                "Longitude": d["px"],
                "Horário": d["ta"]
            }
            for d in dados
        ]
        st.dataframe(tabela, use_container_width=True)
