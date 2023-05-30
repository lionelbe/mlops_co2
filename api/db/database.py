import os

from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = database_url = os.environ.get("DATABASE_URL")#"postgresql://calvin:co2mlops2023@localhost/co2_prediction"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    password = Column(Text)
    predictions = relationship("Prediction", back_populates="user")


class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("DbUser", back_populates="predictions")
    lib_mrq = Column(Integer)
    modele = Column(Integer)
    carburant= Column(Integer)
    hybride = Column(Integer)
    puiss_admin= Column(Float(precision=2))
    puiss_max = Column(Float(precision=2))
    typ_boite_nb_rapp = Column(Integer)
    #lib_mrq = Column(Integer)
    #cod_cbr = Column(Integer)
    #hybride = Column(Integer)
    #puiss_max = Column(Float(precision=2))
    #typ_boite_nb_rapp = Column(Integer)
    #conso_urb = Column(Float(precision=2))
    #conso_exurb = Column(Float(precision=2))
    #conso_mixte = Column(Float(precision=2))
    #masse_ordma_min = Column(Integer)
    #masse_ordma_max = Column(Integer)
    #Carrosserie = Column(Integer)
    #gamme = Column(Integer)
    co2_emissions = Column(Float(precision=2))



# Create the "predictions" table in the database, if it doesn't already exist
Base.metadata.create_all(bind=engine)