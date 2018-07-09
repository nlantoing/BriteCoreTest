import json
from requests_manager import create_app

def json_of_response(response):
    """ Decode the json response from a service """
    return json.loads(response.data.decode('utf8'))

def test_landingPage(client):
    response = client.get('/')
    assert response.status_code == 200

def test_getClients(client):
    response = client.get('/clients')
    assert response.status_code == 200
    result =  json_of_response(response)['results']
    assert len(result) == 5

def test_getProductsarea(client):
    response = client.get('/products_areas')
    assert response.status_code == 200
    result =  json_of_response(response)['results']
    assert len(result) == 4

def test_getRequests(client):
    response = client.get('/requests')
    assert response.status_code == 200
    result =  json_of_response(response)['results']
    assert len(result) == 1

def test_getSingleRequest(client):
    assert client.get('/requests/999').status_code == 404
    assert client.get('/requests/1').status_code == 200
    
def test_createRequest(client):
    #empty request
    data={
        'title': None,
        'description': None,
        'priority': None,
        'target_date': None,
        'client': None,
        'product_area': None}
    response = client.post('/requests',data=data)
    assert response.status_code == 400
    
    data['title'] = "test"
    data['description'] = ''
    data['priority'] = 9000
    data['target_date'] = 100000000
    data['client'] = 1
    data['product_area'] = 1
    response = client.post('/requests', data=data)
    assert response.status_code == 200

def test_editRequest(client):
    data = {
        'title': "New title"
    }
    response = client.put('requests/9999',data=data)
    assert response.status_code == 404
    response = client.put('requests/1',data=data)
    assert response.status_code == 500
    data['description'] = ''
    data['priority'] = 9000
    data['target_date'] = 100000000
    data['client_id'] = 1
    data['product_area_id'] = 1
    response = client.put('requests/1', data=data)
    assert response.status_code == 200
    #TODO: add a webservice to get single requests, can't believe I forgot this one
    
def test_deleteRequest(client):
    response = client.delete('/requests/9999')
    assert response.status_code == 404
    response = client.delete('/requests/1')
    assert response.status_code == 200
