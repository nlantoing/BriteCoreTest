//followed learn.knockoutjs tutorial and decided to keep their naming convention for my classes

//Client model
function Client(id, name) {
    const self = this;
    self.id = id;
    self.name = name;
};

//ProductArea model
function ProductArea(id, name) {
    const self = this;
    self.id = id;
    self.name = name;
};

//Request representation
function Request(request) {
    const self = this;
    self.title = request.title;
    self.description = request.description;
    self.priority = request.priority;
    self.target_date = request.target_date;
    //TODO : should we just get the id and retrieve the correct instance here?
    self.client = request.client;
    self.product_area = request.productArea;
};

function RequestsViewModel() {
    //not needed anymore with ES6 but I guess it is better to keep it
    const self = this;

    //PARAMETERS
    self.clients = ko.observableArray();
    self.productsAreas = ko.observableArray();
    self.requests = ko.observableArray();

    //WEB SERVICES

    //make an AJAX request
    //return a promise
    self.request = function(domain,addr,method){
        return new Promise((action,reject) => {
            let req = new XMLHttpRequest();
            req.open(method, domain+addr);
            req.onreadystatechange = () => {
                if (req.readyState === XMLHttpRequest.DONE) {
                    if(req.status === 200){
                        action(req);
                    }
                }
            };
            req.send();
        });
    };
    
    //  get
    //get clients list
    self.getClients = function(){
        self.request('/','clients','GET').then((response) => {
            
            let clients = JSON.parse(response.response).results;
            for(let i = 0; i < clients.length; i++){
                self.clients.push(new Client(clients[i].id,clients[i].name));
            }
        });
    };
    //get products areas list
    self.getProductsAreas = function(){
        self.request('/','products_areas','GET').then((response) => {
            
            let pa = JSON.parse(response.response).results;
            for(let i = 0; i < pa.length; i++){
                self.productsAreas.push(new ProductArea(pa[i].id, pa[i].name));
            }
        });
    };
    //finally get existing requests
    self.getRequests = function(){
        self.request('/','requests','GET').then((response) => { 
            let req = JSON.parse(response.response).results;
            for(let i = 0; i < req.length; i++){
                self.requests.push(new Request(req[i]));
            }
        });
    };

    //  post/put/delete
    self.createRequest = function(){};
    self.updateRequest = function(){};
    self.deleteRequest = function(){};

    //ACTIONS
    self.sort = function(){};
    self.addRequest = function(){};
    self.removeRequest = function(){};

    //INIT
    self.getClients();
    self.getProductsAreas();
    self.getRequests();
};

window.addEventListener("load", function(e) { 
    ko.applyBindings(new RequestsViewModel(), document.getElementById("content"));
});
