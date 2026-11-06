import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.subheader("Estado - Peugeot")

conn = st.connection("gsheets", type=GSheetsConnection)

# URL limpia (sin los parámetros ?gid=...)
sheet_url = "https://docs.google.com/spreadsheets/d/1ebc3X1sEHvKL003Tq3hSTTcVmKfgFpjIUSx53JjutPE/edit"

df_ayuda = conn.read(
    spreadsheet=sheet_url, 
    worksheet="STATUS Peugeott"
)

st.dataframe(df_ayuda, use_container_width=True, hide_index=True)
