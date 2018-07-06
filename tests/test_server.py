from requests_manager import create_app

def test_clients(client):
    response = client.get('/clients')
    #TODO

def test_productsarea(client):
    response = client.get('/products_areas')
    #TODO

def test_getRequests(client):
    response = client.get('/requests')
    #TODO

