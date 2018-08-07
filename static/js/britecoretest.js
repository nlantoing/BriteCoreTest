//followed learn.knockoutjs tutorial and decided to keep their naming convention for my classes

//Custom bindings
ko.bindingHandlers.enable = {
    update: function(element,valueAccessor){
        valueAccessor() ? element.removeAttribute('disabled') : element.setAttribute('disabled','disabled'); 
    }
};

//User model
function User(id, name) {
    const self = this;
    self.id = id;
    self.name = name;
};

//Project model
function Project(id, name) {
    const self = this;
    self.id = id;
    self.name = name;
};

//Category model
function Category(id, name) {
    const self = this;
    self.id = id;
    self.name = name;
};


//Task representation
function Task(task) {
    const self = this;
    self.id = task.id;
    self.title = ko.observable(task.title);
    self.description = ko.observable(task.description);
    self.priority = ko.observable(task.priority);
    self.due_date = ko.observable(task.due_date.toISOString().slice(0,10));
    self.target_date = ko.computed(function(){
        return new Date(this.due_date()).getTime() / 1000;
    },this);
    //TODO : should we just get the id and retrieve the correct instance here?
    self.user_id = ko.observable(task.user_id);
    self.project_id = ko.observable(task.project_id);
    self.category_id = ko.observable(task.category_id);
    self.fullDisplay = ko.observable(false);
    self.isEdited = ko.observable(false);
};

function TasksViewModel() {
    //not needed anymore with ES6 but I guess it is better to keep it
    const self = this;

    //TODO: I think the whole new task form part should be in his own viewModel class
    
    //PARAMETERS
    self.users = ko.observableArray();
    self.projects = ko.observableArray();
    self.categories = ko.observableArray();
    self.tasks = ko.observableArray();

    //new tasks params, moveme to the new class once done
    self.toogleNewTask = ko.observable(null);
    self.flashMessages = ko.observableArray([]);

    //WEB SERVICES

    //make an AJAX request
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
    //get users list
    self.getUsers = function(){
        self.ajax('/','users','GET').then((response) => {
            
            let users = JSON.parse(response.response).results;
            for(let i = 0; i < users.length; i++){
                self.users.push(new User(users[i].id,users[i].name));
            }
        });
    };
    //get products areas list
    self.getProjects = function(){
        self.ajax('/','projects','GET').then((response) => {
            
            let pa = JSON.parse(response.response).results;
            for(let i = 0; i < pa.length; i++){
                self.projects.push(new Project(pa[i].id, pa[i].name));
            }
        });
    };
    //get categories list
    self.getCategories = function(){
        self.ajax('/','categories','GET').then((response) => {
            
            let pa = JSON.parse(response.response).results;
            for(let i = 0; i < pa.length; i++){
                self.categories.push(new Category(pa[i].id, pa[i].name));
            }
        });
    };
    //get existing tasks
    self.getTasks = function(){
        self.ajax('/','tasks','GET').then((response) => { 
            let req = JSON.parse(response.response).results;
            for(let i = 0; i < req.length; i++){
                self.createTask(req[i]);
            }
        });
    };

    //  post/put/delete
    self.postTask = function(form){
        let data = new FormData(form);
        data.append('target_date', new Date(data.get('due_date')).getTime()/1000);

        //reinitialize flashmessages if any
        self.flashMessages([]);

        if(self.validateForm(data) > 0) return;
        self.ajax('/','tasks','POST',data).then((response) => {
            let entry = JSON.parse(response.response);
            self.createTask(entry);
            //reset form
            self.toogleNewTask(null);
            self.flashMessages([]);
        });
    };
    
    self.updateTask = function(req){
        let data = new FormData();
        data.append('title',req.title());
        data.append('description',req.description());
        data.append('priority', req.priority());
        data.append('target_date', req.target_date());
        data.append('user_id', req.user_id);
        data.append('project_id', req.product_area_id);
	data.append('category_id', req.category_id);

        //check if everything alright before sending the task
        self.flashMessages([]);
        if(self.validateForm(data) > 0) return;
            
        self.ajax('/','tasks/'+req.id,'PUT',data).then((response) => {
            self.toogleEdit(req);
        });
    };
    
    self.deleteTask = function(req){
        self.ajax('/','tasks/'+req.id,'DELETE').then((response) => {
            self.tasks.destroy(req);
        });
    };

    //ACTIONS
    //create a new task from a JSON entry returned by the server
    self.createTask = function(entry){
        entry.due_date = new Date(entry.target_date);
        self.tasks.push(new Task(entry));
    };

    //validate a task form (for update or create) or display an alert if any input is invalid
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
	if(new Date(data.get('due_date')) < new Date()){
	    self.flashMessage.push("You have specified a due date prior to the current one, it will fill developers mailbox with warning and turn them more grumpy than usual (yes they can) so we prevented you to submit that task, contact the administrator and face the consequencies!");
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
    
    //Toogle the create task form
    self.toogleCreateReq = function(el){
        if(null === self.toogleNewTask())
            self.toogleNewTask(true);
        else
            self.toogleNewTask(null);
    };

    //show or hide the details of a task
    self.toogleDetails = function(req){
        let action = req.fullDisplay() ? false : true;
        req.fullDisplay(action);
    };

    //enable or disable edit mode
    self.toogleEdit = function(req){
        let action = req.isEdited() ? false : true;
        req.isEdited(action);
    };

    //Restore the old version of the task and cancel edit mode, WIP
    self.cancelEdit = function(req){
        //TODO: should restore old task state before
        self.toogleEdit(req);
    };
    
    //INIT
    self.getUsers();
    self.getProjects();
    self.getCategories();
    self.getTasks();
};

window.addEventListener("load", function(e) { 
    ko.applyBindings(new TasksViewModel(), document.getElementById("content"));
});
