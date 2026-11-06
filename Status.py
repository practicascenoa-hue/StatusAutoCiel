import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.subheader("Estado - Peugeot")

conn = st.connection("gsheets", type=GSheetsConnection)

# URL apuntando directamente al ID de la pestaña (gid), sin fragmentos al final
sheet_url = "https://docs.google.com/spreadsheets/d/1ebc3X1sEHvKL003Tq3hSTTcVmKfgFpjIUSx53JjutPE/edit?gid=533036020"

# Leemos la hoja utilizando únicamente la URL, sin buscar por nombre
df_ayuda = conn.read(spreadsheet=sheet_url)

st.dataframe(df_ayuda, use_container_width=True, hide_index=True)
