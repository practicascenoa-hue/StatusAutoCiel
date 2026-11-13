import streamlit as st
import pandas as pd

st.set_page_config(page_title="Estado de Vehículos", layout="wide")

# URLs con &range=A:AZ para forzar la lectura completa y evitar que los filtros del Google Sheet afecten al portal
URL_PEUGEOT = "https://docs.google.com/spreadsheets/d/1ebc3X1sEHvKL003Tq3hSTTcVmKfgFpjIUSx53JjutPE/gviz/tq?tqx=out:csv&sheet=STATUS_Peugeott&range=A:AZ"
URL_CITROEN = "https://docs.google.com/spreadsheets/d/1ebc3X1sEHvKL003Tq3hSTTcVmKfgFpjIUSx53JjutPE/gviz/tq?tqx=out:csv&sheet=STATUS_CITROEN&range=A:AZ"

@st.cache_data(ttl=60)
def cargar_datos(url):
    df = pd.read_csv(url)
    # Limpiamos posibles espacios en blanco en los nombres de las columnas
    df.columns = df.columns.str.strip()
    return df

# Función auxiliar para convertir letra de Excel a índice numérico (A=0, B=1, ..., AQ=42)
def letra_a_indice(letra):
    indice = 0
    for c in letra:
        indice = indice * 26 + (ord(c.upper()) - ord('A')) + 1
    return indice - 1

# Inicializar estados de sesión para manejar los botones de forma persistente
if "marca_seleccionada" not in st.session_state:
    st.session_state.marca_seleccionada = "Peugeot"

if "canal_seleccionado" not in st.session_state:
    st.session_state.canal_seleccionado = "TODOS"

st.title("Tablero de Estado de Vehículos")

# --- SECCIÓN SUPERIOR: MARCA (Izquierda) Y CANAL DE VENTA (Derecha) ---
col_marca, col_canal = st.columns([1, 3])

with col_marca:
    st.subheader("MARCA")
    b1, b2 = st.columns(2)
    with b1:
        tipo_p = "primary" if st.session_state.marca_seleccionada == "Peugeot" else "secondary"
        if st.button("🚗 Peugeot", use_container_width=True, type=tipo_p):
            st.session_state.marca_seleccionada = "Peugeot"
            st.session_state.canal_seleccionado = "TODOS" # Reiniciar filtro al cambiar marca
            st.rerun()
    with b2:
        tipo_c = "primary" if st.session_state.marca_seleccionada == "Citroën" else "secondary"
        if st.button("🚘 Citroën", use_container_width=True, type=tipo_c):
            st.session_state.marca_seleccionada = "Citroën"
            st.session_state.canal_seleccionado = "TODOS" # Reiniciar filtro al cambiar marca
            st.rerun()

# Cargar datos según la marca seleccionada
if st.session_state.marca_seleccionada == "Peugeot":
    df = cargar_datos(URL_PEUGEOT)
else:
    df = cargar_datos(URL_CITROEN)

# Obtener nombre real de la Columna E (índice 4) para el Canal de Venta
col_canal_nombre = df.columns[letra_a_indice("E")]

# Calcular totales y porcentajes por Canal de Venta (sobre el total completo)
total_unidades = len(df)
conteo_canales = df[col_canal_nombre].fillna("Sin especificar").astype(str).value_counts()

with col_canal:
    st.subheader(f"Canal de Venta — Total: {total_unidades} (100%)")
    
    # Botón para ver el 100% + un botón por cada valor único de la columna E
    num_botones = len(conteo_canales) + 1
    cols_botones = st.columns(num_botones)
    
    # Botón Total (100%)
    with cols_botones[0]:
        tipo_todos = "primary" if st.session_state.canal_seleccionado == "TODOS" else "secondary"
        if st.button(f"Todos\n{total_unidades} (100%)", use_container_width=True, type=tipo_todos):
            st.session_state.canal_seleccionado = "TODOS"
            st.rerun()
            
    # Botones dinámicos por cada estado/canal de la Columna E
    for idx, (canal, cantidad) in enumerate(conteo_canales.items(), start=1):
        porcentaje = (cantidad / total_unidades * 100) if total_unidades > 0 else 0
        etiqueta = f"{canal}\n{cantidad} ({porcentaje:.1f}%)"
        tipo_btn = "primary" if st.session_state.canal_seleccionado == canal else "secondary"
        
        with cols_botones[idx]:
            if st.button(etiqueta, use_container_width=True, type=tipo_btn, key=f"btn_{canal}"):
                st.session_state.canal_seleccionado = canal
                st.rerun()

st.divider()

# --- FILTRADO Y TABLA FINAL ---
df_mostrar = df.copy()

if st.session_state.canal_seleccionado != "TODOS":
    df_mostrar = df_mostrar[
        df_mostrar[col_canal_nombre].fillna("Sin especificar").astype(str) == st.session_state.canal_seleccionado
    ]

# Extraemos la Columna A (índice 0) y le asignamos el nombre "Cliente"
col_a_nombre = df.columns[0]
df_mostrar["Cliente"] = df_mostrar[col_a_nombre]

# Selección de las columnas solicitadas: B, G, H, I, K, L, M, N, AQ
letras_columnas = ["B", "G", "H", "I", "K", "L", "M", "N", "AQ"]
indices_columnas = [letra_a_indice(letra) for letra in letras_columnas]

# Validamos que el DataFrame tenga suficientes columnas
indices_validos = [i for i in indices_columnas if i < len(df_mostrar.columns)]
columnas_finales = [df_mostrar.columns[i] for i in indices_validos]

# Reordenamos para que "Cliente" quede primera y luego las demás columnas seleccionadas
columnas_finales_con_cliente = ["Cliente"] + columnas_finales

st.subheader(f"Detalle de Unidades — {st.session_state.marca_seleccionada} ({len(df_mostrar)} registros)")
st.dataframe(df_mostrar[columnas_finales_con_cliente], use_container_width=True, hide_index=True)
