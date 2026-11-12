import streamlit as st
import pandas as pd

st.set_page_config(page_title="Estado de Vehículos", layout="wide")

# URLs para leer las hojas de Google Sheets en formato CSV
URL_PEUGEOT = "https://docs.google.com/spreadsheets/d/1ebc3X1sEHvKL003Tq3hSTTcVmKfgFpjIUSx53JjutPE/gviz/tq?tqx=out:csv&sheet=STATUS_Peugeott"
URL_CITROEN = "https://docs.google.com/spreadsheets/d/1ebc3X1sEHvKL003Tq3hSTTcVmKfgFpjIUSx53JjutPE/gviz/tq?tqx=out:csv&sheet=STATUS_CITROEN"

@st.cache_data(ttl=60)
def cargar_datos(url):
    df = pd.read_csv(url)
    # Limpiamos posibles espacios en blanco en los nombres de las columnas
    df.columns = df.columns.str.strip()
    return df

def renderizar_tablero(df, marca):
    # Mapeo seguro por posición de columna (D=3, F=5, G=6, J=9, AP=41)
    col_canal = df.columns[3]          # Columna D: Canal Vta.
    col_modelo = df.columns[5]         # Columna F: Modelo
    col_color = df.columns[6]          # Columna G: Color
    col_estado = df.columns[9]         # Columna J: Estado
    col_estado_unidad = df.columns[41] # Columna AP: Estado de la unidad

    st.subheader("Filtros de Búsqueda")
    
    # 5 columnas horizontales para los desplegables
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        opciones_canal = sorted(df[col_canal].dropna().astype(str).unique())
        sel_canal = st.multiselect("Canal Vta.", opciones_canal, placeholder="Todos", key=f"{marca}_canal")

    with c2:
        opciones_modelo = sorted(df[col_modelo].dropna().astype(str).unique())
        sel_modelo = st.multiselect("Modelo", opciones_modelo, placeholder="Todos", key=f"{marca}_modelo")

    with c3:
        opciones_color = sorted(df[col_color].dropna().astype(str).unique())
        sel_color = st.multiselect("Color", opciones_color, placeholder="Todos", key=f"{marca}_color")

    with c4:
        opciones_estado = sorted(df[col_estado].dropna().astype(str).unique())
        sel_estado = st.multiselect("Estado", opciones_estado, placeholder="Todos", key=f"{marca}_estado")

    with c5:
        opciones_est_unidad = sorted(df[col_estado_unidad].dropna().astype(str).unique())
        sel_est_unidad = st.multiselect("Estado de la unidad", opciones_est_unidad, placeholder="Todos", key=f"{marca}_est_unidad")

    # Aplicar filtros dinámicos
    df_filtrado = df.copy()

    if sel_canal:
        df_filtrado = df_filtrado[df_filtrado[col_canal].astype(str).isin(sel_canal)]
    if sel_modelo:
        df_filtrado = df_filtrado[df_filtrado[col_modelo].astype(str).isin(sel_modelo)]
    if sel_color:
        df_filtrado = df_filtrado[df_filtrado[col_color].astype(str).isin(sel_color)]
    if sel_estado:
        df_filtrado = df_filtrado[df_filtrado[col_estado].astype(str).isin(sel_estado)]
    if sel_est_unidad:
        df_filtrado = df_filtrado[df_filtrado[col_estado_unidad].astype(str).isin(sel_est_unidad)]

    st.divider()

    # Métrica rápida del resultado filtrado
    st.metric(label=f"Total Unidades {marca}", value=len(df_filtrado))

    # Tabla principal
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

# Crear las pestañas para cada marca
tab_peugeot, tab_citroen = st.tabs(["🚗 Peugeot", "🚘 Citroën"])

with tab_peugeot:
    st.header("Estado - Peugeot")
    df_peugeot = cargar_datos(URL_PEUGEOT)
    renderizar_tablero(df_peugeot, "Peugeot")

with tab_citroen:
    st.header("Estado - Citroën")
    df_citroen = cargar_datos(URL_CITROEN)
    renderizar_tablero(df_citroen, "Citroën")
