from sqlalchemy import Column, Integer, String, Float
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)

class Analise(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    p = Column(Float)
    argila = Column(Float)
    ca = Column(Float)
    mg = Column(Float)
    k = Column(Float)
    ctc = Column(Float)
    resultado = Column(String)
