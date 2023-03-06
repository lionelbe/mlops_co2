from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import numpy as np
from database import Session, DbUser, Prediction
from fastapi.responses import Response
# Load the saved linear regression model
model = joblib.load('linear_regression_model.joblib')

class User(BaseModel):
    username: str
    password: str
# Define the input data schema
class CarData(BaseModel):
    lib_mrq: int
    lib_mod_doss: int
    cnit: int
    cod_cbr: int
    hybride: int
    puiss_admin_98: int
    puiss_max: float
    typ_boite_nb_rapp: int
    conso_urb: float
    conso_exurb: float
    conso_mixte: float
    masse_ordma_min: int
    masse_ordma_max: int
    Carrosserie: int
    gamme: int


# Create a FastAPI instance
app = FastAPI()




# Define a function to authenticate users via HTTP Basic Auth
security = HTTPBasic()


def authenticate_user(credentials: HTTPBasicCredentials = Security(security)):
    session = Session()
    db_user = session.query(DbUser).filter_by(username=credentials.username, password=credentials.password).first()
    session.close()
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return db_user

@app.post('/users')
async def create_user(user: User):
    session = Session()
    db_user = DbUser(username=user.username, password=user.password)
    session.add(db_user)
    session.commit()
    session.close()
    return JSONResponse(content={"message": "User created successfully"})


@app.post('/login')
async def login(user: User):
    session = Session()
    db_user = session.query(DbUser).filter_by(username=user.username, password=user.password).first()
    session.close()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Invalid username or password")
    return JSONResponse(content={"message": "Login successful"})


# Define the prediction endpoint
@app.post('/predict')
async def predict_co2_emissions(car_data: CarData, user: DbUser = Depends(authenticate_user)):
    # Convert the input data to a numpy array
    input_data = np.array([
    car_data.lib_mrq,
    car_data.lib_mod_doss,
    car_data.cnit,
    car_data.cod_cbr,
    car_data.hybride,
    car_data.puiss_admin_98,
    car_data.puiss_max,
    car_data.typ_boite_nb_rapp,
    car_data.conso_urb,
    car_data.conso_exurb,
    car_data.conso_mixte,
    car_data.masse_ordma_min,
    car_data.masse_ordma_max,
    car_data.Carrosserie,
    car_data.gamme
    ]).reshape(1, -1)
    # Use the model to predict CO2 emissions
    co2_emissions = model.predict(input_data)[0]

    # Store the prediction in the database
    session = Session()
    prediction = Prediction(
        user=user,
        lib_mrq=car_data.lib_mrq,
        lib_mod_doss=car_data.lib_mod_doss,
        cnit=car_data.cnit,
        cod_cbr=car_data.cod_cbr,
        hybride=car_data.hybride,
        puiss_admin_98=car_data.puiss_admin_98,
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

    # Return the prediction as JSON
    return JSONResponse({'co2_emissions': co2_emissions})

# Define the get history endpoint
@app.get("/history")
async def get_history():
    session = Session()
    predictions = session.query(Prediction).all()
    session.close()
    if not predictions:
        raise HTTPException(status_code=404, detail="History is empty")
    return {"history": [prediction.__dict__ for prediction in predictions]}


@app.get("/history2")
async def get_history(user: DbUser = Depends(authenticate_user)):
    session = Session()
    predictions = session.query(Prediction).filter_by(user=user).all()
    session.close()
    if not predictions:
        raise HTTPException(status_code=404, detail="No history found for this user")
    return {"history": [prediction.__dict__ for prediction in predictions]}

"""
# Define the get history endpoint
@app.get("/presonnal_history")
async def get_history(user: DbUser = Depends(authenticate_user)):
    session = Session()
    predictions = session.query(Prediction).all()
    session.close()
    if not predictions:
        raise HTTPException(status_code=404, detail="History is empty")
    return {"history": [prediction.__dict__ for prediction in predictions]}"""
