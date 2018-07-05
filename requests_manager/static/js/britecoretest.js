//followed learn.knockoutjs tutorial and decided to keep their naming convention for my classes

//Custom bindings
ko.bindingHandlers.enable = {
    update: function(element,valueAccessor){
        valueAccessor() ? element.removeAttribute('disabled') : element.setAttribute('disabled','disabled'); 
    }
};

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
    self.due_date = ko.observable(request.due_date.toISOString().slice(0,10));
    self.target_date = ko.computed(function(){
        return new Date(this.due_date()).getTime() / 1000;
    },this);
    //TODO : should we just get the id and retrieve the correct instance here?
    self.client = ko.observable(request.client);
    self.product_area = ko.observable(request.product_area);
    self.fullDisplay = ko.observable(false);
    self.isEdited = ko.observable(false);
};

function RequestsViewModel() {
    //not needed anymore with ES6 but I guess it is better to keep it
    const self = this;

    //TODO: I think the whole new request form part should be in his own viewModel class
    
    //PARAMETERS
    self.clients = ko.observableArray();
    self.productsAreas = ko.observableArray();
    self.requests = ko.observableArray();

    //new requests params, moveme to the new class once done
    self.toogleNewRequest = ko.observable(null);
    self.flashMessages = ko.observableArray([]);

    //WEB SERVICES

    //make an AJAX request
    //TODO: rename, ambiguous with the Request model
    //return a promise
    self.ajax = function(domain,addr,method,data){
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
        self.ajax('/','clients','GET').then((response) => {
            
            let clients = JSON.parse(response.response).results;
            for(let i = 0; i < clients.length; i++){
                self.clients.push(new Client(clients[i].id,clients[i].name));
            }
        });
    };
    //get products areas list
    self.getProductsAreas = function(){
        self.ajax('/','products_areas','GET').then((response) => {
            
            let pa = JSON.parse(response.response).results;
            for(let i = 0; i < pa.length; i++){
                self.productsAreas.push(new ProductArea(pa[i].id, pa[i].name));
            }
        });
    };
    //get existing requests
    self.getRequests = function(){
        self.ajax('/','requests','GET').then((response) => { 
            let req = JSON.parse(response.response).results;
            for(let i = 0; i < req.length; i++){
                self.createRequest(req[i]);
            }
        });
    };

    //  post/put/delete
    self.postRequest = function(form){
        let data = new FormData(form);
        data.append('target_date', new Date(data.get('due_date')).getTime()/1000);

        //reinitialize flashmessages if any
        self.flashMessages([]);

        if(self.validateForm(data) > 0) return;
        self.ajax('/','requests','POST',data).then((response) => {
            let entry = JSON.parse(response.response);
            self.createRequest(entry);
            //reset form
            self.toogleNewRequest(null);
            self.flashMessages([]);
        });
    };
    
    self.updateRequest = function(req){
        let data = new FormData();
        data.append('title',req.title());
        data.append('description',req.description());
        data.append('priority', req.priority());
        data.append('target_date', req.target_date());
        data.append('client_id', req.client().id);
        data.append('product_area_id', req.product_area().id);

        //check if everything alright before sending the request
        self.flashMessages([]);
        if(self.validateForm(data) > 0) return;
            
        self.ajax('/','requests/'+req.id,'PUT',data).then((response) => {
            self.toogleEdit(req);
        });
    };
    
    self.deleteRequest = function(req){
        self.ajax('/','requests/'+req.id,'DELETE').then((response) => {
            self.requests.destroy(req);
        });
    };

    //ACTIONS
    //create a new request from a JSON entry returned by the server
    self.createRequest = function(entry){
        entry.due_date = new Date(entry.target_date);
        self.requests.push(new Request(entry));
    };

    //validate a request form (for update or create) or display an alert if any input is invalid
    self.validateForm = function(data){
        var errorCount = 0;
        if("" === data.get('title')){
            self.flashMessages.push("Title can't be empty");
            errorCount++;
        }
        if("" === data.get('priority')) {
            self.flashMessages.push("You must set a priority");
            errorCount++;
        }
        if("" === data.get('due_date')) {
            self.flashMessages.push("You must specify a due date");
            errorCount++;
        }
        if(isNaN(data.get('priority'))) {
            self.flashMessages.push("Priority must be a number");
            errorCount++;
        }

        return errorCount;
    };


    //TODO: sorting functions
    self.sort = function(){};
    //TODO: filter function
    self.filter = function(){};
    
    //Toogle the create request form
    self.toogleCreateReq = function(el){
        if(null === self.toogleNewRequest())
            self.toogleNewRequest(true);
        else
            self.toogleNewRequest(null);
    };

    //show or hide the details of a request
    self.toogleDetails = function(req){
        let action = req.fullDisplay() ? false : true;
        req.fullDisplay(action);
    };

    //enable or disable edit mode
    self.toogleEdit = function(req){
        let action = req.isEdited() ? false : true;
        req.isEdited(action);
    };

    //Restore the old version of the request and cancel edit mode, WIP
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
