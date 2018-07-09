### NOTES : ###


Small requests manager project, using flask, SQLAlchemy and KnockoutJS


### INSTALL : ###

Dependencies : Python >= 3.6

> pip install .

generate and populate the sqlite database :

> python requests_manager/db_mock.py

To start the server run the run.sh script from the root directory

> ./run.sh


#### WORK IN PROGRESS : ####

* Use alembic to allow data migration and remove the db_mock.py script
* Allow to Add/edit/remove Clients and Products_Areas
* Konami code! Because why not
* Better css as it is super ugly right now
* Sort and filter options
* Warnings and highlight requests which are overtime or close to it
* Add MOAR unit testing!
* Deploy a live version with that current TODO list
