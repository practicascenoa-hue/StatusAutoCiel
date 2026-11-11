import streamlit as st
import pandas as pd

st.set_page_config(page_title="Estado de Vehículos", layout="wide")

# URLs para leer las hojas de Google Sheets en formato CSV
URL_PEUGEOT = "https://docs.google.com/spreadsheets/d/1ebc3X1sEHvKL003Tq3hSTTcVmKfgFpjIUSx53JjutPE/gviz/tq?tqx=out:csv&sheet=STATUS_Peugeott"
URL_CITROEN = "https://docs.google.com/spreadsheets/d/1ebc3X1sEHvKL003Tq3hSTTcVmKfgFpjIUSx53JjutPE/gviz/tq?tqx=out:csv&sheet=STATUS_CITROEN"

@st.cache_data(ttl=60)
def cargar_datos(url):
    return pd.read_csv(url)

# Crear las pestañas para cada marca
tab_peugeot, tab_citroen = st.tabs(["🚗 Peugeot", "🚘 Citroën"])

with tab_peugeot:
    st.header("Estado - Peugeot")
    df_peugeot = cargar_datos(URL_PEUGEOT)
    st.dataframe(df_peugeot, use_container_width=True)

with tab_citroen:
    st.header("Estado - Citroën")
    df_citroen = cargar_datos(URL_CITROEN)
    st.dataframe(df_citroen, use_container_width=True)
