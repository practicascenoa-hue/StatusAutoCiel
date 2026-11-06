import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.subheader("Estado - Peugeot")

conn = st.connection("gsheets", type=GSheetsConnection)
sheet_url = "https://docs.google.com/spreadsheets/d/1ebc3X1sEHvKL003Tq3hSTTcVmKfgFpjIUSx53JjutPE/edit?gid=533036020#gid=533036020"

# Leemos la nueva hoja (asegúrate de que el nombre sea exactamente igual en tu Excel, respetando espacios y la doble T)
df_ayuda = conn.read(
    spreadsheet=sheet_url, 
    worksheet="STATUS Peugeott"
)

st.dataframe(df_ayuda, use_container_width=True, hide_index=True)
