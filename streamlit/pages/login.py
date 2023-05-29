import streamlit as st
import requests
import json

API_URL = st.session_state["api_url"]

if "login" in st.session_state:

    # st.write("Vous etes connecté en tant que "+st.session_state["login"])
    st.markdown("<div style='text-align: right;'>Vous êtes connecté en tant que "+st.session_state["login"]+"</div>", unsafe_allow_html=True)
    with st.form("login_form"):
       submitted = st.form_submit_button("Se déconnecter")
       if submitted:
        #    logout_request = requests.post(API_URL+"/logout", 
        #                                   data=json.dumps({ "username": st.session_state["login"],
        #                                                     "password": st.session_state["password"]}))
        #    response = json.loads(logout_request.text)
        # ne fonctionne pas, renvoie un code 401
        #    st.write(logout_request)
        #    if "message" in response:
        #        st.write(response["message"])
           del st.session_state["login"]
           del st.session_state["password"]
        #    components.html("<script langage='javascript'>location.reload();</script>")
           st.experimental_rerun()

else:
    st.write("### Connexion")
    with st.form("login_form"):
        login = st.text_input("Login")
        password = st.text_input("Password", type="password")
        login_submit = st.form_submit_button("Se connecter")

    if login_submit:
        login_request = requests.post(API_URL+"/login", data=json.dumps({ "username": login, "password": password}))
        response = json.loads(login_request.text)
        if "detail" in response:
            st.write(response["detail"])
        if "message" in response:
            if response["message"] == "Login successful":
                st.session_state["login"] = login
                st.session_state["password"] = password
                st.write(response["message"])
                # components.html("<script langage='javascript'>location.reload();</script>")
                st.experimental_rerun()



st.write("### Création d'un compte utilisateur")

with st.form("create_form"):
    usr_login = st.text_input("Login")
    usr_password = st.text_input("Password", type="password")
    create_submit = st.form_submit_button("créer le compte")

    if create_submit:
       
        create_request = requests.post(API_URL+"/users", 
                                       data=json.dumps({ "username": usr_login,
                                                         "password": usr_password}))
        response = json.loads(create_request.text)

        if "detail" in response:
            st.write(response["detail"])
        if "message" in response:
            if response["message"] == "User created successfully":
                st.write("Utilisateur "+usr_login+" créé !")