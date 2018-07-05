import os
import tempfile
import requests_manager
import pytest

@pytest.fixture
def client():
    db_fd, requests_manager.app.config['DATABASE'] = tempfile.mkstemp()
    requests_manager.app.config['TESTING'] = True
    client = requests_manager.app.test_client()

    with requests_manager.app.app_context():
        requests_manager.init_db()

        yield client

        os.close(db_fd)
        os.unlink(requests_manager.app.config['DATABASE'])

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data
