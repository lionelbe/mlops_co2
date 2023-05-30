# CO2 Emission Prediction API
This project provides an API for predicting CO2 emissions of vehicles based on their features. The prediction model has been trained on a dataset of vehicle characteristics and their corresponding CO2 emissions. The API is built using FastAPI, and the database is implemented using SQLite with SQLAlchemy. The server is run with Uvicorn.

## Data Source
The dataset used to train the CO2 emission prediction model was obtained from the French government's open data website, Data.gouv. The dataset contains information on CO2 emissions and pollutants from vehicles sold in France from 2001 to 2015:

https://www.data.gouv.fr/fr/datasets/emissions-de-co2-et-de-polluants-des-vehicules-commercialises-en-france/

## Install & Run
You can use the API by installing each component individually, but it's easier to do it with Docker !

Clone the project repository to your local machine (at least api & streamlit folders).

**WITH DOCKER**

Go in api folder.<br/>
Run `docker-compose up --build`<br/>
Go to `http://127.0.0.1:8000/docs/` to see the API.

Go in streamlit folder.<br/>
Run `docker-compose up --build`<br/>
Go to `http://127.0.0.1:8501/` to run the frontend application.

**WITHOUT DOCKER**

Go in api folder.<br/>
Create your virtual environment : virtualenv `.mlopsco2_api`<br/>
Activate it : source `.mlopsco2_api/bin/activate`<br/>
Install requirements : `pip install -r requirements.txt`<br/>
Run the api : `uvicorn api:app --reload`

Go in streamlit folder.<br/>
Create your virtual environment : virtualenv `.mlopsco2_streamlit`<br/>
Activate it : source `.mlopsco2_streamlit/bin/activate`<br/>
Install requirements : `pip install -r requirements.txt`<br/>
Run the api : `streamlit run frontend.py`

## Usage

The Frontend is running on http://localhost:8501.<br/>
The API is running on http://localhost:8000.<br/>
You can access the API documentation at http://localhost:8000/docs.

### Make your prediction : 
To make a prediction, a POST request is sent via the **/predict** endpoint with the following parameters:

```JSON
{
    "marque": ...,                      # Integer: Brand identifier
    "modele": ...,                      # Car Model
    "carburant": ...,                   # Fuel type 
    "hybride": ...,                     # Hybrid vehicle
    "puiss_max": ...,                   # Power Rating (CV)
    "puiss_max": ...,                   # Maximum power in kW
    "boite_v": ...,                     # Gearbox type and number of gears
}
```

The API will then return a predicted CO2 emission value.

### Create an account : 
To create a new user account, send a POST request to the **/users** endpoint with a JSON payload containing username and password fields.

### Log in : 
To log in to an existing account, send a POST request to the **/login** endpoint with a JSON payload containing username and password fields.

### Get your history : 
To view the prediction history for a logged-in user, send a GET request to the /history endpoint while logged in. The endpoint will return a JSON array of all the user's prediction history.

## Database
The API uses a database to store user accounts and prediction history. The database is implemented using SQLAlchemy, and the schema is defined in models.py.

## Group Member

Calvin Pierre-Joseph<br>
Michael Laidet<br>
Lionel Bérenger<br>
