import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Estado de Vehículos", layout="wide")

# URLs de exportación directa
URL_PEUGEOT = "https://docs.google.com/spreadsheets/d/1ebc3X1sEHvKL003Tq3hSTTcVmKfgFpjIUSx53JjutPE/export?format=csv&gid=533036020#gid=533036020"
URL_CITROEN = "https://docs.google.com/spreadsheets/d/1ebc3X1sEHvKL003Tq3hSTTcVmKfgFpjIUSx53JjutPE/export?format=csv&gid=1779651149"

@st.cache_data(ttl=60)
def cargar_datos(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

def letra_a_indice(letra):
    indice = 0
    for c in letra:
        indice = indice * 26 + (ord(c.upper()) - ord('A')) + 1
    return indice - 1

if "marca_seleccionada" not in st.session_state:
    st.session_state.marca_seleccionada = "Peugeot"

if "canal_seleccionado" not in st.session_state:
    st.session_state.canal_seleccionado = "TODOS"

st.title("Tablero de Estado de Vehículos")

col_marca, col_canal = st.columns([1, 3])

with col_marca:
    st.subheader("MARCA")
    b1, b2 = st.columns(2)
    with b1:
        tipo_p = "primary" if st.session_state.marca_seleccionada == "Peugeot" else "secondary"
        if st.button("🚗 Peugeot", use_container_width=True, type=tipo_p):
            st.session_state.marca_seleccionada = "Peugeot"
            st.session_state.canal_seleccionado = "TODOS"
            st.rerun()
    with b2:
        tipo_c = "primary" if st.session_state.marca_seleccionada == "Citroën" else "secondary"
        if st.button("🚘 Citroën", use_container_width=True, type=tipo_c):
            st.session_state.marca_seleccionada = "Citroën"
            st.session_state.canal_seleccionado = "TODOS"
            st.rerun()

if st.session_state.marca_seleccionada == "Peugeot":
    df = cargar_datos(URL_PEUGEOT)
else:
    df = cargar_datos(URL_CITROEN)

col_canal_nombre = df.columns[letra_a_indice("E")]

total_unidades = len(df)
conteo_canales = df[col_canal_nombre].fillna("Sin especificar").astype(str).value_counts()

with col_canal:
    st.subheader(f"Canal de Venta — Total: {total_unidades} (100%)")
    
    num_botones = len(conteo_canales) + 1
    cols_botones = st.columns(num_botones)
    
    with cols_botones[0]:
        tipo_todos = "primary" if st.session_state.canal_seleccionado == "TODOS" else "secondary"
        if st.button(f"Todos\n{total_unidades} (100%)", use_container_width=True, type=tipo_todos):
            st.session_state.canal_seleccionado = "TODOS"
            st.rerun()
            
    for idx, (canal, cantidad) in enumerate(conteo_canales.items(), start=1):
        porcentaje = (cantidad / total_unidades * 100) if total_unidades > 0 else 0
        etiqueta = f"{canal}\n{cantidad} ({porcentaje:.1f}%)"
        tipo_btn = "primary" if st.session_state.canal_seleccionado == canal else "secondary"
        
        with cols_botones[idx]:
            if st.button(etiqueta, use_container_width=True, type=tipo_btn, key=f"btn_{canal}"):
                st.session_state.canal_seleccionado = canal
                st.rerun()

st.divider()

# ---------------- FILTRADO PRINCIPAL POR CANAL ----------------
df_mostrar = df.copy()

if st.session_state.canal_seleccionado != "TODOS":
    df_mostrar = df_mostrar[
        df_mostrar[col_canal_nombre].fillna("Sin especificar").astype(str) == st.session_state.canal_seleccionado
    ]

# ---------------- GRÁFICO DINÁMICO DESPLEGABLE (Columna K) ----------------
col_estado_nombre = df.columns[letra_a_indice("K")]
total_filtrado_canal = len(df_mostrar)

if total_filtrado_canal > 0:
    df_estados = df_mostrar[col_estado_nombre].fillna("Sin especificar").astype(str).value_counts().reset_index()
    df_estados.columns = ['Estado', 'Cantidad']
    
    df_estados['Porcentaje'] = (df_estados['Cantidad'] / total_filtrado_canal * 100).round(1)
    df_estados['Etiqueta'] = df_estados['Cantidad'].astype(str) + " (" + df_estados['Porcentaje'].astype(str) + "%)"
    
    # ACÁ ESTÁ EL CAMBIO: expanded=False hace que arranque oculto (cerrado)
    with st.expander(f"📊 Ver distribución de Estados — Canal: {st.session_state.canal_seleccionado}", expanded=False):
        
        fig = px.bar(
            df_estados, 
            x='Estado', 
            y='Cantidad', 
            text='Etiqueta',
            color='Estado', 
            template="plotly_white"
        )
        
        fig.update_traces(textposition='outside')
        fig.update_layout(
            showlegend=False, 
            xaxis_title="", 
            yaxis_title="Cantidad de Unidades",
            margin=dict(t=10, b=10)
        )
        
        evento_grafico = st.plotly_chart(
            fig, 
            use_container_width=True, 
            on_select="rerun", 
            key="grafico_interactivo"
        )

        if evento_grafico and len(evento_grafico.selection.get("points", [])) > 0:
            estado_seleccionado = evento_grafico.selection["points"][0]["x"]
            
            df_mostrar = df_mostrar[
                df_mostrar[col_estado_nombre].fillna("Sin especificar").astype(str) == estado_seleccionado
            ]
            
            st.info(f"Filtro activo: Mostrando solo unidades en estado **{estado_seleccionado}**. Haz clic en un espacio vacío del gráfico para quitar el filtro.")

st.divider()

# ---------------- TABLA DE DETALLES FINAL ----------------
col_a_nombre = df.columns[0]
df_mostrar["Cliente"] = df_mostrar[col_a_nombre]

letras_columnas = ["B", "G", "H", "I", "K", "L", "M", "N", "AQ"]
indices_columnas = [letra_a_indice(letra) for letra in letras_columnas]

indices_validos = [i for i in indices_columnas if i < len(df_mostrar.columns)]
columnas_finales = [df_mostrar.columns[i] for i in indices_validos]

columnas_finales_con_cliente = ["Cliente"] + columnas_finales

st.subheader(f"Detalle de Unidades — {st.session_state.marca_seleccionada} ({len(df_mostrar)} registros)")
st.dataframe(df_mostrar[columnas_finales_con_cliente], use_container_width=True, hide_index=True)
