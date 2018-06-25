from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/requests', methods=['GET'])
def getRequests():
    #Get requests list or create a new one

@app.route('/requests',methods=['POST'])
def createRequest():
    #Create a new request
    
@app.route('/requests/<int:request_id>', methods=['PUT','DELETE'])
def modifyRequest(request_id):
    #modify or remove an existing request
