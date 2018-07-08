from flask import Flask, jsonify, request, render_template, g, Blueprint
from requests_manager.database import db, Client, Product_Area, Request
import datetime

#Meh' don't got any inspiration for a proper prefix and has this app will probably get only one BP...
bp = Blueprint('requests', __name__, url_prefix="/")

def isNumber(value):
    """ check if a string is a proper number """
    try:
        int(value)
        return True
    except ValueError:
        return False

@bp.route('/')
def hello():
    """ home page """
    return render_template('index.html'), 200, {'ContentType':'text/html'}

@bp.route('/clients', methods=['GET'])
def getClients():
    """ Get clients list, return a JSON type response """
    print(db)
    requests = db.session.query(Client).all()
    return jsonify(results=[i.jsonize() for i in requests]), 200, {'ContentType':'application/json'}

@bp.route('/products_areas', methods=['GET'])
def getProducts():
    """ Get products_areas entries, return a JSON type response """
    requests = db.session.query(Product_Area).all()
    return jsonify(results=[i.jsonize() for i in requests]), 200, {'ContentType':'application/json'}

@bp.route('/requests', methods=['GET'])
def getRequests():
    """ Get current requests list, return a JSON type response """
    requests = db.session.query(Request).order_by(Request.priority).all()
    return jsonify(results=[i.jsonize() for i in requests]), 200, {'ContentType':'application/json'}

@bp.route('/requests',methods=['POST'])
def createRequest():
    """ Create a new request """
    data = request.form
    try:
        if "" == data.get('title'):
            raise ValueError("Title can't be empty")
        if not isNumber(data.get('target_date')):
            raise ValueError("You must specify a date")
        if not isNumber(data.get('priority')):
            raise ValueError("Priority must be a number")
        
        entry = Request(
            title = data.get('title'),
            description = data.get('description'),
            target_date = datetime.datetime.fromtimestamp(int(data.get('target_date'))),
            priority = data.get('priority'),
            client_id = data.get('client'),
            product_area_id = data.get('product_area'))
        db.session.add(entry)
        db.session.commit()
    except ValueError as error:
        return jsonify({
            'message': "OOps couldn't create new request, check your inputs!",
            'data': data,
            'error': str(error)
        }), 400, {'ContentType':'application/json'}

    return jsonify(entry.jsonize()), 200, {'ContentType':'application/json'}
    
@bp.route('/requests/<int:request_id>', methods=['PUT','DELETE'])
def modifyRequest(request_id):
    """ modify or remove an existing request """
    toUpdate = Request.query.get(request_id)
    if toUpdate is not None:

        try:
            if 'DELETE' == request.method:
                db.session.delete(toUpdate)
            else:
                data = request.form
                if "" == data.get('title'):
                    raise ValueError("title can't be empty")
                if not isNumber(data.get('priority')):
                    raise ValueError("Priority must be a number")
                toUpdate.title = data.get('title')
                toUpdate.description = data.get('description')
                toUpdate.target_date = datetime.datetime.fromtimestamp(int(data.get('target_date')))
                toUpdate.priority = data.get('priority')
                toUpdate.client_id = data.get('client_id')
                toUpdate.product_area_id = data.get('product_area_id')

            db.session.commit()
            
        except ValueError as error:
            return jsonify({'message': "OOps something gone wrong",
                            'data': data,
                            'error': str(error)
            }), 500, {'ContentType':'application/json'}
        
        return jsonify({'updated_request': request_id}), 200, {'ContentType':'application/json'}
    else:
        return jsonify({
            'message': "The request doesn't exist",
            'data': request_id
        }), 404, {'ContentType': 'application/json'}
