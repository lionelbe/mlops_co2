from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from fastapi.responses import Response
import joblib
import numpy as np
from typing import Dict

from db.database import Session, DbUser, Prediction
from models import User, CarData
from utils import get_equiv_table


model = joblib.load('joblib/lr_model.joblib')

app = FastAPI(title="CO2 Emissions Prediction API",
    description="An API to predict CO2 emissions of cars based on their characteristics",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "healthcheck",
            "description": "Endpoints for health checking the API",
        },
        {
            "name": "users",
            "description": "Endpoints for creating and authenticating users",
        },
        {
            "name": "predictions",
            "description": "Endpoints for making and retrieving predictions",
        },
        {
            "name": "history",
            "description": "Endpoints for retrieving the history of all predictions made",
        },
    ],)
security = HTTPBasic()

def authenticate_user(credentials: HTTPBasicCredentials = Security(security)):
    session = Session()
    db_user = session.query(DbUser).filter_by(username=credentials.username, password=credentials.password).first()
    session.close()
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return db_user

@app.get('/status', tags=["healthcheck"], description="Check if the API is running.")
def status():
    return {'message': 'API is running!'}

@app.post('/users', tags=["users"], description="Create a new user.")
async def create_user(user: User):
    session = Session()
    db_user = DbUser(username=user.username, password=user.password)
    session.add(db_user)
    session.commit()
    session.close()
    return JSONResponse(content={"message": "User created successfully"})

@app.post('/login', tags=["users"], description="Authenticate a user.")
async def login(user: User):
    session = Session()
    db_user = session.query(DbUser).filter_by(username=user.username, password=user.password).first()
    session.close()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Invalid username or password")
    return JSONResponse(content={"message": "Login successful"})

@app.get("/equiv_table/{column}", tags=["Equivalence Table"], summary="Retrieve the equivalence table for a given column.")
def get_equiv_table_endpoint(column: str) -> Dict[str, int]:

    """
    Retrieve the equivalence table for a given column.
    
    - **lib_mrq**: The brand of the car.
    - **cod_cbr**: The fuel type of the car.
    - **hybride**: Whether the car is hybrid or not.
    - **typ_boite_nb_rapp**: The type of gearbox and number of gears of the car.
    - **Carrosserie**: The body type of the car.
    - **gamme**: The range or series of the car model.
    
    """

    equiv_table = get_equiv_table(column)
    if equiv_table is None:
        return {"error": "Invalid column name or column is not categorical"}
    return equiv_table

@app.post('/predict', tags=["predictions"], description="Make a CO2 emissions prediction for a car.")
async def predict_co2_emissions(car_data: CarData, user: DbUser = Depends(authenticate_user)):
    input_data = np.array(list(car_data.dict().values())).reshape(1,-1)

    co2_emissions = model.predict(input_data)[0]

    session = Session()
    prediction = Prediction(
        user=user,
        lib_mrq=car_data.lib_mrq,
        cod_cbr=car_data.cod_cbr,
        hybride=car_data.hybride,
        puiss_max=car_data.puiss_max,
        typ_boite_nb_rapp=car_data.typ_boite_nb_rapp,
        conso_urb=car_data.conso_urb,
        conso_exurb=car_data.conso_exurb,
        conso_mixte=car_data.conso_mixte,
        masse_ordma_min=car_data.masse_ordma_min,
        masse_ordma_max=car_data.masse_ordma_max,
        Carrosserie=car_data.Carrosserie,
        gamme=car_data.gamme,
        co2_emissions=co2_emissions
    )
    session.add(prediction)
    session.commit()
    session.close()

    return JSONResponse({'co2_emissions': co2_emissions})

@app.get("/history", tags=["history"], summary="Get the history of all CO2 emissions predictions made")
async def get_history():

    """
    Get the history of all CO2 emissions predictions made

    Returns:
        A dictionary with a "history" key and a list of all predictions made and stored in the database
    """

    session = Session()
    predictions = session.query(Prediction).all()
    session.close()
    if not predictions:
        raise HTTPException(status_code=404, detail="History is empty")
    return {"history": [prediction.__dict__ for prediction in predictions]}


@app.get("/personal_history", tags=["history"], summary="Get the history of CO2 emissions predictions made by the authenticated user")
async def get_history(user: DbUser = Depends(authenticate_user)):

    """
    Get the history of CO2 emissions predictions made by the authenticated user

    Args:
        user: the authenticated user

    Returns:
        A dictionary with a "history" key and a list of all predictions made and stored in the database by the authenticated user
    """

    session = Session()
    predictions = session.query(Prediction).filter_by(user=user).all()
    session.close()
    if not predictions:
        raise HTTPException(status_code=404, detail="No history found for this user")
    return {"history": [prediction.__dict__ for prediction in predictions]}

@app.post('/logout')
async def logout(user: DbUser = Depends(authenticate_user)):
    session = Session()
    session.delete(user)
    session.commit()
    session.close()
    return JSONResponse(content={"message": "User logged out successfully"})
