from flask import Flask, jsonify, request, render_template
from database import Client, Request, Product_Area
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#TODO: the db uri should be defined in a conf file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///britecore.db'
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/clients', methods=['GET'])
def getClients():
    #Get requests list or create a new one
    requests = db.session.query(Client).all()
    return jsonify(results=[i.jsonize() for i in requests])

@app.route('/products_areas', methods=['GET'])
def getProducts():
    #Get requests list or create a new one
    requests = db.session.query(Product_Area).all()
    return jsonify(results=[i.jsonize() for i in requests])

@app.route('/requests', methods=['GET'])
def getRequests():
    #Get requests list or create a new one
    requests = db.session.query(Request).all()
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
    db.session.add(entry)
    db.session.commit()
    return 200
    
@app.route('/requests/<int:request_id>', methods=['PUT','DELETE'])
def modifyRequest(request_id):
    #modify or remove an existing request
    return "TODO!"
