from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

    def __repr__(self):
        return "<Client(name='%s')>" % (self.name)


class Product_Area(Base):
    __tablename__ = 'products_areas'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

    def __repr__(self):
        return "<Product_Area(name='%s')>" % (self.name)

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

engine = create_engine('sqlite:///britecore.db', echo=True)
Base.metadata.create_all(engine)
