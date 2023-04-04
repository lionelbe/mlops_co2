from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define the SQLite database connection
engine = create_engine('sqlite:///predictions.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define the Prediction class, which maps to the "predictions" table in the database
class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    predictions = relationship("Prediction", back_populates="user")


class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("DbUser", back_populates="predictions")
    lib_mrq = Column(Integer)
    cod_cbr = Column(Integer)
    hybride = Column(Integer)
    puiss_max = Column(Float)
    typ_boite_nb_rapp = Column(Integer)
    conso_urb = Column(Float)
    conso_exurb = Column(Float)
    conso_mixte = Column(Float)
    masse_ordma_min = Column(Integer)
    masse_ordma_max = Column(Integer)
    Carrosserie = Column(Integer)
    gamme = Column(Integer)
    co2_emissions = Column(Float)


# Create the "predictions" table in the database, if it doesn't already exist
Base.metadata.create_all(engine)