
### NOTES : ###


Small requests manager project, using flask, SQLAlchemy and Angular(2.4)


### INSTALL : ###

Dependencies : Python >= 3.5

Build and activate the venv, this part is optional but highly recommended, you only need the second command after the first time

> python3 -m venv venv
> . venv/bin/activate

Install the project in edit mode (WIP, there is an issue with how the DB is initialized which prevent the app to function properly if you are not on edit mode)

> pip install -e .

generate and populate the sqlite database :

> flask db init
> flask db upgrade
> python db_mock.py

To start flask the server run the run.sh script from the root directory

> ./run.sh

To start angular server (this require the angular ng command tool)

> cd frontend && ng serve

Access the manager from

> http://localhost:4200/

Or the current live Demo with all the current tasks on it :

> http://34.253.155.194
