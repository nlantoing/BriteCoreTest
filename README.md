




NOTES:

REST web services
SQlite3 database (lite relational database) 

    
python 3


  //start the server
  ./run.sh

INSTALL

//dependencies
pip install .
or
pip install Flask SQLAlchemy flask_sqlalchemy pytest
//create the virtualenv
python3 -m venv venv
  //activate it
  . venv/bin/activate
//generate and populate the sqlite database :
python db_mock.py