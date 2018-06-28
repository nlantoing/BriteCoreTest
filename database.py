#TODO: move app config (db, app etc) elsewhere
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

#TODO: the db uri should be defined in a conf file
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///britecore.db'
db = SQLAlchemy(app)

class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32),unique=True, nullable=False)

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
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    product_area_id = db.Column(db.Integer, db.ForeignKey('products_areas.id'))
    client = db.relationship(Client)
    product_area = db.relationship(Product_Area)

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

