import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {API_URL} from '../env';
import {Task} from './task.model';
import {Subscription} from 'rxjs/Subscription';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';

@Injectable()
export class TasksApiService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }

  // GET tasks
    public getTasks(): Observable<Task[]> {
	let tasks = this.http
	    .get<Task[]>(`${API_URL}/tasks`);
	return tasks;
    }
}
