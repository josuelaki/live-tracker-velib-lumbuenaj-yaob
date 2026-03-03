import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Vélib Tracker", layout="wide")
st.title("LiveTracker Vélib - Paris")

API_URL = "http://127.0.0.1:8000/stations"

st.write("Récupération des données depuis l'API...")

try:
    reponse = requests.get(API_URL)
    
    if reponse.status_code == 200:
        donnees = reponse.json()
        
        if donnees:
            df = pd.DataFrame(donnees)
            
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("La base de données est vide")
    else:
        st.error(f"Erreur API : {reponse.status_code}")

except requests.exceptions.ConnectionError:
    st.error("Impossible de se connecter à l'API.")