# CO2 Emission Prediction API
This project provides an API for predicting CO2 emissions of vehicles based on their features. The prediction model has been trained on a dataset of vehicle characteristics and their corresponding CO2 emissions. The API is built using FastAPI, and the database is implemented using SQLite with SQLAlchemy. The server is run with Uvicorn.

## Data Source
The dataset used to train the CO2 emission prediction model was obtained from the French government's open data website, Data.gouv. The dataset contains information on CO2 emissions and pollutants from vehicles sold in France from 2001 to 2015:

https://www.data.gouv.fr/fr/datasets/emissions-de-co2-et-de-polluants-des-vehicules-commercialises-en-france/

## Requirements
To use the API, the following dependencies must be installed:

* FastAPI
* Joblib
* NumPy
* Pydantic
* SQLAlchemy
* Uvicorn

These dependencies can be installed using pip:

```
pip install fastapi joblib numpy pydantic sqlalchemy uvicorn
```
**OR**
```
pip install -r requirements.txt
```

## Usage
To use the API, follow these steps:

Clone the project repository to your local machine.

In the root directory of the project, run the following command to start the FastAPI app with Uvicorn:

```
uvicorn api/api:app --reload
```
The API is now running on http://localhost:8000. You can access the API documentation at http://localhost:8000/docs.

### Make your prediction : 
To make a prediction, send a POST request to the **/predict** endpoint with the following parameters:

```JSON
{
    "lib_mrq": 1,                       # Integer: Brand identifier (there are 12 different brands)
    "cod_cbr": 1,                       # Integer: Fuel type (there are 5 different types of fuel)
    "hybride": 0,                       # Integer: Hybrid vehicle (0 or 1)
    "puiss_max": 95.0,                  # Float: Maximum power in kW
    "typ_boite_nb_rapp": 5,             # Integer: Gearbox type and number of gears
    "conso_urb": 7.2,                   # Float: Urban consumption in L/100km
    "conso_exurb": 4.5,                 # Float: Extra-urban consumption in L/100km
    "conso_mixte": 5.5,                 # Float: Mixed consumption in L/100km
    "masse_ordma_min": 1100,            # Integer: Minimum unladen weight in kg
    "masse_ordma_max": 1200,            # Integer: Maximum unladen weight in kg
    "Carrosserie": 1,                   # Integer: Body type
    "gamme": 1                          # Integer: Vehicle category
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
The API uses a SQLite database to store user accounts and prediction history. The database is implemented using SQLAlchemy, and the schema is defined in models.py.

# Group Member

Calvin Pierre-Joseph<br>
Michael Laidet<br>
Lionel Bérenger<br>
