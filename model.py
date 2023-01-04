from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Float, Integer

engine = create_engine('sqlite:///db.sqlite')
Base = declarative_base()


class LostItem(Base):
    __tablename__ = "LostItem"

    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    type_objet = Column(String, nullable=True)
    date_restitution = Column(String, nullable=True)

class TemperatureHeure(Base):
    __tablename__ = "TemperatureHeure"

    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=True)
    temperature = Column(String, nullable=True)


class Temperature(Base):
    __tablename__ = "Temperature"
    
    date = Column(String,  primary_key=True)
    temperature = Column(Integer, nullable=True)


Base.metadata.create_all(engine)



