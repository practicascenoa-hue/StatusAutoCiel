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

# ---------------- FILA 1: SECCIÓN MARCA ----------------
st.subheader("MARCA")
# Usamos columnas pequeñas a la izquierda para los botones, y dejamos el resto vacío
col_b1, col_b2, espacio_vacio = st.columns([1, 1, 4]) 

with col_b1:
    tipo_p = "primary" if st.session_state.marca_seleccionada == "Peugeot" else "secondary"
    if st.button("🚗 Peugeot", use_container_width=True, type=tipo_p):
        st.session_state.marca_seleccionada = "Peugeot"
        st.session_state.canal_seleccionado = "TODOS"
        st.rerun()

with col_b2:
    tipo_c = "primary" if st.session_state.marca_seleccionada == "Citroën" else "secondary"
    if st.button("🚘 Citroën", use_container_width=True, type=tipo_c):
        st.session_state.marca_seleccionada = "Citroën"
        st.session_state.canal_seleccionado = "TODOS"
        st.rerun()


# --- CARGA DE DATOS ---
if st.session_state.marca_seleccionada == "Peugeot":
    df = cargar_datos(URL_PEUGEOT)
else:
    df = cargar_datos(URL_CITROEN)

col_canal_nombre = df.columns[letra_a_indice("E")]
total_unidades = len(df)
conteo_canales = df[col_canal_nombre].fillna("Sin especificar").astype(str).value_counts()

st.write("") # Un pequeño espacio en blanco para separar

# ---------------- FILA 2: SECCIÓN CANAL DE VENTA ----------------
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
