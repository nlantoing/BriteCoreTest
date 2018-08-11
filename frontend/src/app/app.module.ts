import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {HttpClientModule} from '@angular/common/http';

import { AppComponent } from './app.component';
import {TasksApiService} from './tasks/tasks-api.service';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
      BrowserModule,
      HttpClientModule
  ],
  providers: [TasksApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
