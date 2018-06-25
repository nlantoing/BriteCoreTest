from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Client, Request, Product_Area, Base

engine = create_engine('sqlite:///britecore.db')
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
session = Session()

session.add_all([
    Client(name='Client A'),
    Client(name='Client B'),
    Client(name='Client C'),
    Client(name='Client D'),
    Client(name='Client E')])

session.commit()

session.add_all([
    Product_Area(name='Policies'),
    Product_Area(name='Billing'),
    Product_Area(name='Claims'),
    Product_Area(name='Reports')])

session.commit()
