from flask import Flask, jsonify, request, render_template
from database import Client, Request, Product_Area, db, app

import datetime

#TODO: urgh ugly removeme!
app = app
#app = Flask(__name__)
#app.config.from_envvar('CONF')


@app.route('/')
def hello():
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
    data = request.form
    entry = Request(
        title = data.get('title'),
        description = data.get('description'),
        target_date = datetime.datetime.fromtimestamp(int(data.get('target_date'))),
        priority = data.get('priority'),
        client_id = data.get('client'),
        product_area_id = data.get('product_area'))
    db.session.add(entry)
    db.session.commit()
    return jsonify(entry.jsonize())
    
@app.route('/requests/<int:request_id>', methods=['PUT','DELETE'])
def modifyRequest(request_id):
    #modify or remove an existing request
    toUpdate = Request.query.get(request_id)
    #TODO : return an error if it doesn't exist
    if toUpdate is not None:
        if 'DELETE' == request.method:
            db.session.delete(toUpdate)
        else:
            data = request.form
            toUpdate.title = data.get('title')
            toUpdate.description = data.get('description')
            toUpdate.target_date = datetime.datetime.fromtimestamp(int(data.get('target_date')))
            toUpdate.priority = data.get('priority')
            toUpdate.client_id = data.get('client_id')
            toUpdate.product_area_id = data.get('product_area_id')

    db.session.commit()
    #TODO: return httpcode if ajax request
    return render_template('index.html')
