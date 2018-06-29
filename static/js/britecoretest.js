//followed learn.knockoutjs tutorial and decided to keep their naming convention for my classes

//Custom bindings
ko.bindingHandlers.enable = {
    update: function(element,valueAccessor){
        let shouldEnable = valueAccessor();
        valueAccessor() ? element.removeAttribute('disabled') : element.setAttribute('disabled','disabled'); 
    }
}

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
    self.title = ko.observable(request.title);
    self.description = ko.observable(request.description);
    self.priority = ko.observable(request.priority);
    self.target_date = ko.observable(request.target_date);
    //TODO : should we just get the id and retrieve the correct instance here?
    self.client = ko.observable(request.client);
    self.product_area = ko.observable(request.product_area);
    self.fullDisplay = ko.observable(false);
    self.isEdited = ko.observable(false);
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
    self.request = function(domain,addr,method,data){
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
        let data = new FormData(form);
        //TODO: do the validator
        self.request('/','requests','POST',data).then((response) => {
            let entry = JSON.parse(response.response);
            self.requests.push(new Request(entry));
            //reset form
            self.newRequest.title(null);
            self.newRequest.description(null);
            self.newRequest.priority(null);
        });
    };
    
    self.updateRequest = function(req){
        let data = new FormData();
        data.append('title',req.title());
        data.append('description',req.description());
        data.append('priority', req.priority());
        //data.append('target_date', req.target_date());
        data.append('target_date', Math.round(new Date().getTime() / 1000));
        data.append('client_id', req.client().id);
        data.append('product_area_id', req.product_area().id);

        //TODO: do the validator
        //TODO : use the Request object instead of the form?
        self.request('/','requests/'+req.id,'PUT',data).then((response) => {
            self.toogleEdit(req);
        });
    };
    
    self.deleteRequest = function(req){
        self.request('/','requests/'+req.id,'DELETE').then((response) => {
            self.requests.destroy(req);
        });
    };

    //ACTIONS
    self.sort = function(){};
    self.toogleDetails = function(req){
        let action = req.fullDisplay() ? false : true;
        req.fullDisplay(action);
    };

    self.toogleEdit = function(req){
        let action = req.isEdited() ? false : true;
        req.isEdited(action);
    };

    self.cancelEdit = function(req){
        //TODO: should restore old request state before
        self.toogleEdit(req);
    };
    
    //INIT
    self.getClients();
    self.getProductsAreas();
    self.getRequests();
};

window.addEventListener("load", function(e) { 
    ko.applyBindings(new RequestsViewModel(), document.getElementById("content"));
});
