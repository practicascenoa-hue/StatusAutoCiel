import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 1. Título en tu portal
st.subheader("Procedimiento de Seguimiento y Contención")

# 2. Establecer la conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. URL exacta que me pasaste
sheet_url = "https://docs.google.com/spreadsheets/d/1ebc3X1sEHvKL003Tq3hSTTcVmKfgFpjIUSx53JjutPE/edit?gid=533036020#gid=533036020"

# 4. Leer los datos de la hoja "Ayuda"
# Leemos las primeras 5 columnas (Pasos, link, usuario, contraseña)
df_ayuda = conn.read(
    spreadsheet=sheet_url, 
    worksheet="Ayuda", 
    usecols=[0, 1, 2, 3, 4]
)

# 5. Limpiar valores nulos y proyectar la tabla
df_ayuda = df_ayuda.dropna(subset=["Pasos"]) # Filtra filas vacías
st.dataframe(df_ayuda, use_container_width=True, hide_index=True)
