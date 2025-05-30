import streamlit as st

home_page = st.Page("home.py", title="Home", icon="🏠", default=True)
sim1_page = st.Page("sim1.py", title="Simulador Principal", icon="👩🏽‍💻") 

pg = st.navigation([home_page, sim1_page])
st.set_page_config(layout="wide", page_title="🎲 Simulador Casa de Apostas")
pg.run()
