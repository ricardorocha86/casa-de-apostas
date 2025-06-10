import streamlit as st

home_page = st.Page("home.py", title="Home", icon="🏠", default=True)
sim1_page = st.Page("sim1.py", title="Simulador Principal", icon="👩🏽‍💻")  
voce_aposta_page = st.Page("voce_aposta.py", title="Você Aposta", icon="🎲")
calculadora_odds_page = st.Page("calculadora_odds.py", title="Calculadora de Odds", icon="📚")

pg = st.navigation([home_page, calculadora_odds_page, sim1_page, voce_aposta_page ])
st.set_page_config(layout="wide", page_title="🎲 Simulador Casa de Apostas")
pg.run()
