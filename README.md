
### NOTES : ###


Small requests manager project, using flask, SQLAlchemy and KnockoutJS


### INSTALL : ###

Dependencies : Python >= 3.5

Build and activate the venv, this part is optional but highly recommended, you only need the second command after the first time

> python3 -m venv venv
> . venv/bin/activate

Install the project in edit mode (WIP, there is an issue with how the DB is initialized which prevent the app to function properly if you are not on edit mode)

> pip install -e .

generate and populate the sqlite database :

> python requests_manager/db_mock.py

To start the server run the run.sh script from the root directory

> ./run.sh

Access the manager from

> http://localhost:5000/

Or the current live Demo with all the current tasks on it :

> http://34.253.155.194
