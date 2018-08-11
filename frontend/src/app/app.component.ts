import {Component, OnInit, OnDestroy} from '@angular/core';
import {Subscription} from 'rxjs/Subscription';
import {TasksApiService} from './tasks/tasks-api.service';
import {Task} from './tasks/task.model';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit, OnDestroy {
    title = 'frontend';
    tasksListSubs: Subscription;
    tasksList: Task[];

    constructor(private tasksApi: TasksApiService){
    }

    ngOnInit(){
	this.tasksListSubs = this.tasksApi
	    .getTasks()
	    .subscribe(res => {
		this.tasksList = res;
	    },console.error);
    }

    ngOnDestroy(){
	this.tasksListSubs.unsubscribe();
    }
}
