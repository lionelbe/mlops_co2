import streamlit as st
import requests
from st_pages import Page, show_pages, add_page_title

API_HOST='127.0.0.1'
API_PORT=8000
API_URL=f'http://{API_HOST}:{API_PORT}'
st.session_state["api_url"] = API_URL

# https://pypi.org/project/st-pages/
my_pages = []

my_pages.append(Page("pages/home.py", "Accueil", "🏠"))
my_pages.append(Page("pages/history_global.py", "Historique global", "👀"))
my_pages.append(Page("pages/predictions.py", "Predictions", "🌍"))
my_pages.append(Page("pages/history_user.py", "Historique personnel", "😎"))
my_pages.append(Page("pages/login.py", "Connexion", "🔐"))


# if "login" not in st.session_state:
#     my_pages.append(Page("pages/accueil.py", "Accueil", "🏠"))
#     my_pages.append(Page("pages/login.py", "Connexion", "👀"))
# else:
#     st.write("Bienvenue ")
#     my_pages.append(Page("pages/accueil.py", "Accueil", "🏠"))
#     my_pages.append(Page("pages/predictions.py", "Predictions", "🌍"))

show_pages(my_pages)
# hide_pages()

st.set_page_config(
    page_title="Mlops CO2",
    page_icon="🌍"
)

