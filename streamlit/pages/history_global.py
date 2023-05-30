import streamlit as st
import requests
import json
import pandas as pd

API_URL = st.session_state["api_url"]
# API_URL = 'http://mlops-app:8000'

st.write("# Historique des prédictions d'émissions de CO2")

history_request = requests.get(API_URL+"/history")
response = json.loads(history_request.text)

# trick pour cacher l'index : ne fonctionne qu'avec st.table(res), pas st.dataframe :(
# CSS to inject contained in a string
# hide_table_row_index = """
#             <style>
#             thead tr th:first-child {display:none}
#             tbody th {display:none}
#             </style>
#             """
# Inject CSS with Markdown
# st.markdown(hide_table_row_index, unsafe_allow_html=True)

if "history" in response:
    # st.write(pd.DataFrame.from_dict(response["history"]))
    res = pd.DataFrame.from_dict(response["history"])

    get_marque = requests.get(API_URL+"/equiv_table/marque")
    json_marque = json.loads(get_marque.text)
    data_marque = {v: k for k, v in json_marque.items()}

    get_modele = requests.get(API_URL+"/equiv_table/modele")
    json_modele = json.loads(get_modele.text)
    data_modele = {v: k for k, v in json_modele.items()}

    get_boite = requests.get(API_URL+"/equiv_table/boite_v")
    json_boite = json.loads(get_boite.text)
    data_boite = {v: k for k, v in json_boite.items()}

    get_hybride = requests.get(API_URL+"/equiv_table/hybride")
    json_hybride = json.loads(get_hybride.text)
    data_hybride = {v: k for k, v in json_hybride.items()}

    # st.write(data_modele)
    # res.drop(columns=['id', 'user_id'], inplace=True)
    res = res[['marque', 'modele', 'hybride', 'boite', 'carburant', 'puiss_admin', 'puiss_max', 'co2_emissions']]

    res['marque'] = res["marque"].replace(data_marque)
    res['modele'] = res["modele"].replace(data_modele)
    res['hybride'] = res["hybride"].replace(data_hybride)
    res['boite'] = res["boite"].replace(data_boite)

    res['puiss_admin'] = res["puiss_admin"].astype(float).round(2)

    res.rename(columns={"co2_emissions": "co2", "boite" : "boite vitesse", "puiss_admin": "puiss. admin. (cv)", "puiss_max": "puiss. max."}, inplace=True)

    # st.table(res)
    st.dataframe(res)
        
else:
    st.write("Aucune prédiction pour l'instant...")