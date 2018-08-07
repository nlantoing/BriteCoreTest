import json
from app import create_app

def json_of_response(response):
    """ Decode the json response from a service """
    return json.loads(response.data.decode('utf8'))

def test_landingPage(client):
    response = client.get('/')
    assert response.status_code == 200

def test_getUsers(client):
    response = client.get('/users')
    assert response.status_code == 200
    result =  json_of_response(response)['results']
    assert len(result) == 1

def test_getProjects(client):
    response = client.get('/projects')
    assert response.status_code == 200
    result =  json_of_response(response)['results']
    assert len(result) == 4

def test_getTasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    result =  json_of_response(response)['results']
    assert len(result) == 1

def test_getSingleTask(client):
    assert client.get('/tasks/999').status_code == 404
    assert client.get('/tasks/1').status_code == 200
    
def test_createTask(client):
    #empty task
    data={
        'title': None,
        'description': None,
        'priority': None,
        'target_date': None,
        'user_id': None,
        'project_id': None,
        'category_id': None}
    response = client.post('/tasks',data=data)
    assert response.status_code == 400
    
    data['title'] = "test"
    data['description'] = ''
    data['priority'] = 9000
    data['target_date'] = 100000000
    data['user_id'] = 1
    data['project_id'] = 1
    data['category_id'] = 1
    response = client.post('/tasks', data=data)
    assert response.status_code == 200

def test_editTask(client):
    data = {
        'title': "New title"
    }
    response = client.put('tasks/9999',data=data)
    assert response.status_code == 404
    response = client.put('tasks/1',data=data)
    assert response.status_code == 500
    data['description'] = ''
    data['priority'] = 9000
    data['target_date'] = 100000000
    data['user_id'] = 1
    data['project_id'] = 1
    data['category_id'] = 1
    response = client.put('tasks/1', data=data)
    assert response.status_code == 200
        
def test_deleteTask(client):
    response = client.delete('/tasks/9999')
    assert response.status_code == 404
    response = client.delete('/tasks/1')
    assert response.status_code == 200
