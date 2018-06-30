#TODO: move app config (db, app etc) elsewhere
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import datetime

app = Flask(__name__)
app.config.from_envvar('CONF')
db = SQLAlchemy(app)

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32),unique=True, nullable=False)
    requests = db.relationship('Request', backref='client', lazy=True)

    def jsonize(self):
        #yup I know this is not even a word
        return {
            'id': self.id,
            'name': self.name
        }
    
    def __repr__(self):
        return self.name


class Product_Area(db.Model):
    __tablename__ = 'products_areas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    requests = db.relationship('Request', backref='product_area', lazy=True)

    def jsonize(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def __repr__(self):
        return self.name

class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(512))
    priority = db.Column(db.Integer)
    target_date = db.Column(db.Date)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    product_area_id = db.Column(db.Integer, db.ForeignKey('products_areas.id'), nullable=False)
    
    def jsonize(self):
        #Should not happen but happened a few times anyway, TODO: fixme!
        if self.client is None:
            self.client = Client(name='Broken')
        if self.product_area is None:
            self.product_area = Product_Area(name='Broken')
        
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

