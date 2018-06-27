#TODO: Use flask_sqlalchemy instead

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


import datetime

Base = declarative_base()
engine = create_engine('sqlite:///britecore.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
dbSession = Session()

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

    def jsonize(self):
        #yup I know this is not even a word
        return {
            'id': self.id,
            'name': self.name
        }
    
    def __repr__(self):
        return self.name


class Product_Area(Base):
    __tablename__ = 'products_areas'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

    def jsonize(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def __repr__(self):
        return self.name

class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True)
    title = Column(String(32), nullable=False)
    description = Column(String(512))
    priority = Column(Integer)
    target_date = Column(Date)
    client_id = Column(Integer, ForeignKey('clients.id'))
    product_area_id = Column(Integer, ForeignKey('products_areas.id'))
    client = relationship(Client)
    product_area = relationship(Product_Area)

    def jsonize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'target_date': self.target_date,
            'client' : self.client.jsonize(),
            'product_area' : self.product_area.jsonize()
        }

    def __repr__(self):
            return "%s" % (self.title)

