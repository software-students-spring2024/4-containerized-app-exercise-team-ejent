# test_main.py
import pytest
from flask import url_for
from io import BytesIO
from web_app.main import app


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