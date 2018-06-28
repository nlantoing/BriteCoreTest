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
    self.id = request.id;
    self.title = request.title;
    self.description = request.description;
    self.priority = request.priority;
    self.target_date = request.target_date;
    //TODO : should we just get the id and retrieve the correct instance here?
    self.client = request.client;
    self.product_area = request.product_area;
};

function RequestsViewModel() {
    //not needed anymore with ES6 but I guess it is better to keep it
    const self = this;

    //PARAMETERS
    self.clients = ko.observableArray();
    self.productsAreas = ko.observableArray();
    self.requests = ko.observableArray();
    self.newRequest = {
        'title': ko.observable(),
        'description': ko.observable(),
        'priority': ko.observable(),
        'due_date': ko.observable(),
        'client_id': ko.observable(),
        'product_area_id': ko.observable()
    };
    self.target_date = ko.computed(function(){
        return new Date(this.newRequest.due_date()).getTime() / 1000;
    },this);

    //WEB SERVICES

    //make an AJAX request
    //return a promise
    self.request = function(domain,addr,method,form){
        return new Promise((action,reject) => {
            let req = new XMLHttpRequest();
            let data = new FormData(form);

            req.open(method, domain+addr);
            req.onreadystatechange = () => {
                if (req.readyState === XMLHttpRequest.DONE) {
                    if(req.status === 200){
                        action(req);
                    }
                }
            };
            req.send(data);
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
    self.postRequest = function(form){
        //TODO: do the validator
        //convert data to a dictionary before passing it to the request
        self.request('/','requests','POST',form).then((response) => {
            let entry = JSON.parse(response.response);
            self.requests.push(new Request(entry));
        });
    };
    
    self.updateRequest = function(){};
    self.deleteRequest = function(req){
        self.request('/','requests/'+req.id,'DELETE').then((response) => {
            self.requests.destroy(req);
        });
    };

    //ACTIONS
    self.sort = function(){};
    self.addRequest = function(){};

    //INIT
    self.getClients();
    self.getProductsAreas();
    self.getRequests();
};

window.addEventListener("load", function(e) { 
    ko.applyBindings(new RequestsViewModel(), document.getElementById("content"));
});
