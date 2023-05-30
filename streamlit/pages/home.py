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
Cette application a été créée dans le cadre de la formation MLOps janvier 2023.
- Calvin Pierre-Joseph
- Michael Laidet
- Lionel Bérenger            
            """)

