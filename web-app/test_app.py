"""
pytest: write tests for our code
io: work with file-like objects
"""
from io import BytesIO
from app import app as flask_app
from flask import url_for
import pytest

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_index(client):
    response = client.get(url_for('index'))
    assert response.status_code == 200

def test_upload_file_no_file(client):
    response = client.post(url_for('upload_file'))
    assert response.status_code == 200
    assert response.get_json() == {'message': 'No file uploaded'}

def test_upload_file_with_file(client):
    data = {
        'photo': (BytesIO(b'my file contents'), 'test.jpg')
    }
    response = client.post(url_for('upload_file'), content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert 'message' in response.get_json()
    assert 'results' in response.get_json()
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get(url_for('index'))
    assert response.status_code == 200

def test_upload_file_no_file(client):
    response = client.post(url_for('upload_file'))
    assert response.status_code == 200
    assert response.get_json() == {'message': 'No file uploaded'}

def test_upload_file_with_file(client):
    data = {
        'photo': (BytesIO(b'my file contents'), 'test.jpg')
    }
    response = client.post(url_for('upload_file'), content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    assert 'message' in response.get_json()
    assert 'results' in response.get_json()