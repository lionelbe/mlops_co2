import streamlit as st
import os

API_HOST='127.0.0.1'
API_PORT=8000

if "DOCKER_APP" in os.environ:
    API_HOST=os.environ['DOCKER_APP']

API_URL=f'http://{API_HOST}:{API_PORT}'
st.session_state["api_url"] = API_URL

st.set_page_config(
    page_title="Mlops CO2",
    page_icon="🌍"
)

st.write("# Bienvenue 👋")

st.markdown("""
Cette application permet de faire des prédictions d'émission CO2 en fonction des caractéristiques d'un véhicule, et de consulter l'historique (personnel ou global) des prédictions.
\nIl est possible  de créer un utilisateur via l'application, c'est même nécessaire pour faire des prédictions et pour l'historique personnel.

L'application tourne dans un container Docker.
Elle est l'interface frontend d'une API FastAPI qui tourne d'un autre conteneur, et qui communique avec une Base de données PostgreSQL.
            """)
st.image('img/graphique.jpg')

st.markdown("""
Cette application a été créée dans le cadre de la formation Datascientest / MLOps janvier 2023 par
- Calvin Pierre-Joseph
- Michael Laidet
- Lionel Bérenger            
            """)
