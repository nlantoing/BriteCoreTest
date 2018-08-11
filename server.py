from flask import Flask, jsonify, request, render_template, g, Blueprint
from database import db, Project, Category, User, Task
import datetime

#Meh' don't got any inspiration for a proper prefix and has this app will probably get only one BP...
bp = Blueprint('requests', __name__, url_prefix="/")

def isNumber(value):
    """ check if a string is a proper number """
    if value is None:
        return False
    try:
        int(value)
        return True
    except ValueError:
        return False

@bp.route('/')
def hello():
    """ home page """
    return render_template('index.html'), 200, {'ContentType':'text/html'}

# GET

@bp.route('/users', methods=['GET'])
def getUsers():
    """ Get users list, return a JSON type response """
    users = db.session.query(User).all()
    return jsonify(results=[i.jsonize() for i in users]), 200, {'ContentType':'application/json'}

@bp.route('/projects', methods=['GET'])
def getProducts():
    """ Get projects list, return a JSON type response """
    projects = db.session.query(Project).all()
    return jsonify(results=[i.jsonize() for i in projects]), 200, {'ContentType':'application/json'}

@bp.route('/categories', methods=['GET'])
def getCategories():
    """ Get projects list, return a JSON type response """
    categories = db.session.query(Category).all()
    return jsonify(results=[i.jsonize() for i in categories]), 200, {'ContentType':'application/json'}

@bp.route('/tasks', methods=['GET'])
def getTasks():
    """ Get current tasks list, return a JSON type response """
    tasks = db.session.query(Task).order_by(Task.priority).all()
    return jsonify([i.jsonize() for i in tasks]), 200, {'ContentType':'application/json'}

@bp.route('/tasks/<int:task_id>',methods=['GET'])
def getSingleTask(task_id):
    """ Get a single task """
    task = Task.query.get(task_id)
    if task is not None:
        return jsonify(results=task.jsonize()), 200, {'ContentType': 'application/json'}
    else:
        return jsonify({
            'message': "This task doesn't exist!",
            'data': task_id
        }), 404, {'ContentType':'application/json'}

# POST

@bp.route('/tasks',methods=['POST'])
def createTask():
    """ Create a new task """
    data = request.form
    try:
        if "" == data.get('title'):
            raise ValueError("Title can't be empty")
        if not isNumber(data.get('target_date')):
            raise ValueError("You must specify a date")
        if not isNumber(data.get('priority')):
            raise ValueError("Priority must be a number")

        entry = Task(
            title = data.get('title'),
            description = data.get('description'),
            target_date = datetime.datetime.fromtimestamp(int(data.get('target_date'))),
            priority = data.get('priority'),
            user_id = data.get('user_id'),
            project_id = data.get('project_id'),
            category_id = data.get('category_id'))
        db.session.add(entry)
        db.session.commit()
    except ValueError as error:
        return jsonify({
            'message': "OOps couldn't create new task, check your inputs!",
            'data': data,
            'error': str(error)
        }), 400, {'ContentType':'application/json'}

    return jsonify(entry.jsonize()), 200, {'ContentType':'application/json'}

# DELETE

@bp.route('/tasks/<int:task_id>', methods=['PUT','DELETE'])
def modifyTask(task_id):
    """ modify or remove an existing task """
    toUpdate = Task.query.get(task_id)
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
                toUpdate.user_id = data.get('user_id')
                toUpdate.project_id = data.get('project_id')
                toUpdate.category_id = data.get('category_id')

            db.session.commit()
            
        except ValueError as error:
            return jsonify({'message': "OOps something gone wrong",
                            'data': data,
                            'error': str(error)
            }), 500, {'ContentType':'application/json'}
        
        return jsonify({'updated_task': task_id}), 200, {'ContentType':'application/json'}
    else:
        return jsonify({
            'message': "The task doesn't exist",
            'data': task_id
        }), 404, {'ContentType': 'application/json'}
