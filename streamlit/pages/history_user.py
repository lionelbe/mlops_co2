import streamlit as st
import requests
import json
import pandas as pd

API_URL = st.session_state["api_url"]

if "login" not in st.session_state:
    st.write("### 😮 Vous devez être connecté pour voir votre historique !")
else :
    st.markdown("<div style='text-align: right;'>Vous êtes connecté en tant que "+st.session_state["login"]+"</div>", unsafe_allow_html=True)
    st.write("# Mes prédictions d'émissions de CO2")

    auth_user = (st.session_state["login"], st.session_state["password"])
    history_request = requests.get(API_URL+"/personal_history", auth=auth_user)
    
    response = json.loads(history_request.text)
    if "history" in response:
        st.write(pd.DataFrame.from_dict(response["history"]))