import streamlit as st
import requests
import json

API_URL = st.session_state["api_url"]
co2_result = ""

if "login" not in st.session_state:
    st.write("### 😮 Il faut être connecté pour pouvoir faire une prédiction !")
else :
    st.markdown("<div style='text-align: right;'>Vous êtes connecté en tant que "+st.session_state["login"]+"</div>", unsafe_allow_html=True)
    st.write("# Prédictions d'émissions de CO2 🚗")

    # get datas (equiv_table)
    get_marque = requests.get(API_URL+"/equiv_table/marque")
    json_marque = json.loads(get_marque.text)
    data_marque = {v: k for k, v in json_marque.items()}

    get_modele = requests.get(API_URL+"/equiv_table/modele")
    json_modele = json.loads(get_modele.text)
    data_modele = {v: k for k, v in json_modele.items()}

    get_carburant = requests.get(API_URL+"/equiv_table/carburant")
    json_carburant = json.loads(get_carburant.text)
    data_carburant = {v: k for k, v in json_carburant.items()}

    get_hybride = requests.get(API_URL+"/equiv_table/hybride")
    json_hybride = json.loads(get_hybride.text)
    data_hybride = {v: k for k, v in json_hybride.items()}

    get_boite_v = requests.get(API_URL+"/equiv_table/boite_v")
    json_boite_v = json.loads(get_boite_v.text)
    data_boite_v = {v: k for k, v in json_boite_v.items()}

    # get_Carrosserie = requests.get(API_URL+"/equiv_table/Carrosserie")
    # json_Carrosserie = json.loads(get_Carrosserie.text)
    # data_Carrosserie= {v: k for k, v in json_Carrosserie.items()}

    # get_gamme = requests.get(API_URL+"/equiv_table/gamme")
    # json_gamme = json.loads(get_gamme.text)
    # data_gamme = {v: k for k, v in json_gamme.items()}

    # form
    col1, col2 = st.columns(2)

    with st.form("predict_form"):

        with col1:
            st.write("Merci de bien vouloir renseigner les champs :")
            marque = st.selectbox("Marque", data_marque.keys(), format_func=lambda x: data_marque[x])
            modele = st.selectbox("Modele", data_modele.keys(), format_func=lambda x: data_modele[x])
            carburant = st.selectbox("Carburant", 
                                     data_carburant.keys(), 
                                     format_func=lambda x: data_carburant[x])
            boite_v = st.selectbox("Boite de vitesse", 
                                            data_boite_v.keys(), 
                                            format_func=lambda x: data_boite_v[x])
            # marque = st.selectbox("Marque", json_marque.keys())
            # carburant = st.selectbox("Carburant", json_carburant.keys())
            # boite_v = st.selectbox("Boite de vitesse", json_boite_v.keys())
        
        with col2:
            hybride = st.radio("Hybride", data_hybride, format_func=lambda x: data_hybride[x])
            # hybride = st.radio("Hybride", json_hybride)
            puiss_admin = st.text_input("Puissance administrative (CV)", 0)
            puiss_max = st.text_input("Puissance Max", 0)

        # submit bt
        submitted = st.form_submit_button("Prédiction")

        # action
        if submitted:

            car_data = { "marque": marque, "modele": modele, "carburant": carburant, "hybride": hybride,
                "puiss_admin" : float(puiss_admin), "puiss_max": float(puiss_max), "boite": boite_v
            }
            auth_user = (st.session_state["login"], st.session_state["password"])
            co2_request = requests.post(API_URL+"/predict", data=json.dumps(car_data), auth=auth_user)
            response = json.loads(co2_request.text)


            if "co2_emissions" in response:
                co2_result = response["co2_emissions"]
# resultat
if co2_result:
    st.write("### Résultat : "+str(round(co2_result,2)))


