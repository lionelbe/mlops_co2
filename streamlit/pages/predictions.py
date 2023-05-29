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
    get_lib_mrq = requests.get(API_URL+"/equiv_table/lib_mrq")
    json_lib_mrq = json.loads(get_lib_mrq.text)
    data_lib_mrq = {v: k for k, v in json_lib_mrq.items()}

    get_cod_cbr = requests.get(API_URL+"/equiv_table/cod_cbr")
    json_cod_cbr = json.loads(get_cod_cbr.text)
    data_cod_cbr = {v: k for k, v in json_cod_cbr.items()}

    get_hybride = requests.get(API_URL+"/equiv_table/hybride")
    json_hybride = json.loads(get_hybride.text)
    data_hybride = {v: k for k, v in json_hybride.items()}

    get_typ_boite_nb_rapp = requests.get(API_URL+"/equiv_table/typ_boite_nb_rapp")
    json_typ_boite_nb_rap = json.loads(get_typ_boite_nb_rapp.text)
    data_typ_boite_nb_rap = {v: k for k, v in json_typ_boite_nb_rap.items()}

    get_Carrosserie = requests.get(API_URL+"/equiv_table/Carrosserie")
    json_Carrosserie = json.loads(get_Carrosserie.text)
    data_Carrosserie= {v: k for k, v in json_Carrosserie.items()}

    get_gamme = requests.get(API_URL+"/equiv_table/gamme")
    json_gamme = json.loads(get_gamme.text)
    data_gamme = {v: k for k, v in json_gamme.items()}

    # form
    col1, col2 = st.columns(2)

    with st.form("predict_form"):

        with col1:
            st.write("Merci de bien vouloir renseigner les champs")
            lib_mrq = st.selectbox("Marque", data_lib_mrq.keys(), format_func=lambda x: data_lib_mrq[x])
            cod_cbr = st.selectbox("Carburant", data_cod_cbr.keys(), format_func=lambda x: data_cod_cbr[x])
            hybride = st.radio("Hybride", data_hybride, format_func=lambda x: data_hybride[x])
            puiss_max = st.text_input("Puissance Max", 0)
            typ_boite_nb_rapp = st.selectbox("Nb rapports boite de vitesse", 
                                            data_typ_boite_nb_rap.keys(), 
                                            format_func=lambda x: data_typ_boite_nb_rap[x])
        
        with col2:
            Carrosserie = st.selectbox("Carrosserie", data_Carrosserie.keys(), format_func=lambda x: data_Carrosserie[x])
            gamme = st.selectbox("Carrosserie", data_gamme.keys(), format_func=lambda x: data_gamme[x])
            conso_urb = st.text_input("Consommation urbaine", 0)
            conso_exurb = st.text_input("Conso extra urbaine", 0)
            conso_mixte = st.text_input("Conso mixte", 0)
            masse_ordma_min = st.text_input("Masse min", 0)
            masse_ordma_max = st.text_input("Masse max", 0)

        # submit bt
        submitted = st.form_submit_button("Prédiction")

        # action
        if submitted:
            car_data = { "lib_mrq": lib_mrq, "cod_cbr": cod_cbr, "hybride": hybride,
                "puiss_max": puiss_max, "typ_boite_nb_rapp": typ_boite_nb_rapp,
                "conso_urb": conso_urb, "conso_exurb": conso_exurb,
                "conso_mixte": conso_mixte,
                "masse_ordma_min": masse_ordma_min,
                "masse_ordma_max": masse_ordma_max,
                "Carrosserie": Carrosserie,
                "gamme": gamme
            }

            auth_user = (st.session_state["login"], st.session_state["password"])
            co2_request = requests.post(API_URL+"/predict", data=json.dumps(car_data), auth=auth_user)
            response = json.loads(co2_request.text)
            if "co2_emissions" in response:
                co2_result = response["co2_emissions"]
# resultat
if co2_result:
    st.write("### Résultat : "+str(round(co2_result,2)))


