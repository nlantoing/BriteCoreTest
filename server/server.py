from flask import Flask, jsonify, request
from database import Client, Request, Product_Area, Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

#TODO: moveme, also db engine should be defined in a cnnf file
engine = create_engine('sqlite:///britecore.db')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/clients', methods=['GET'])
def getClients():
    #Get requests list or create a new one
    requests = session.query(Client).all()
    return jsonify(results=[i.jsonize() for i in requests])

@app.route('/products_areas', methods=['GET'])
def getProducts():
    #Get requests list or create a new one
    requests = session.query(Product_Area).all()
    return jsonify(results=[i.jsonize() for i in requests])

@app.route('/requests', methods=['GET'])
def getRequests():
    #Get requests list or create a new one
    requests = session.query(Request).all()
    return jsonify(results=[i.jsonize() for i in requests])

@app.route('/requests',methods=['POST'])
def createRequest():
    #Create a new request
    entry = Request(
        title = request.data.title,
        description = request.data.description,
        target_date = datetime.datetime.now(),
        priority = request.data.priority,
        client_id = request.data.client_id,
        product_area_id = request.data.product_area_id)
    session.add(entry)
    session.commit()
    return 200
    
@app.route('/requests/<int:request_id>', methods=['PUT','DELETE'])
def modifyRequest(request_id):
    #modify or remove an existing request
    return "TODO!"
