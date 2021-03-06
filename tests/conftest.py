import os
import tempfile
import pytest
from requests_manager import create_app, db_mock
from requests_manager.database import db

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///'+db_path,
    })

    with app.app_context():
        db_mock.init_db(app)
        
    yield app
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_runner()
