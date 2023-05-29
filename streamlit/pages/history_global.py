import streamlit as st
import requests
import json
import pandas as pd

API_URL = st.session_state["api_url"]

st.write("# Historique des prédictions d'émissions de CO2")

history_request = requests.get(API_URL+"/history")
response = json.loads(history_request.text)
if "history" in response:
    st.write(pd.DataFrame.from_dict(response["history"]))