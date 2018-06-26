from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Client, Request, Product_Area, Base

import datetime

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

session.add(Request(
    title="Test request",
    description="Just populate the request table with one query to ease development",
    target_date = datetime.datetime.now(),
    priority=1,
    client_id=1,
    product_area_id=1))
session.commit()
