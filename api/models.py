from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    password: str

class CarData(BaseModel):
    marque: int = Field(..., description="Brand identifier")
    modele: int
    carburant: int = Field(..., description="")
    hybride: int = Field(..., description="")
    puiss_admin: float = Field(..., description="")
    puiss_max: float = Field(..., description="")
    boite: int = Field(..., description="")
    """lib_mrq: int = Field(..., description="Brand identifier (there are 12 different brands)")
    cod_cbr: int = Field(..., description="Fuel type (there are 5 different types of fuel)")
    hybride: int = Field(..., description="Hybrid vehicle (0 or 1)")
    puiss_max: float = Field(..., description="Maximum power in kW")
    typ_boite_nb_rapp: int = Field(..., description="Gearbox type and number of gears")
    conso_urb: float = Field(..., description="Urban consumption in L/100km")
    conso_exurb: float = Field(..., description="Extra-urban consumption in L/100km")
    conso_mixte: float = Field(..., description="Mixed consumption in L/100km")
    masse_ordma_min: int = Field(..., description="Minimum unladen weight in kg")
    masse_ordma_max: int = Field(..., description="Maximum unladen weight in kg")
    Carrosserie: int = Field(..., description="Body type")
    gamme: int = Field(..., description="Vehicle category")"""