import os
import pytest
from PIL import Image
from main import app as flask_app
from pymongo import MongoClient
import base64

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def test_image_file():
    img = Image.new('RGB', (60, 30), color = (73, 109, 137))
    img.save('test_image.png')
    yield 'test_image.png'
    os.remove('test_image.png')

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_upload_without_name(client, test_image_file):
    data = {
        'photo': (open(test_image_file, 'rb'), test_image_file),
    }
    response = client.post('/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 400  # Expect a 400 status code when no name is provided
    json_data = response.get_json()
    assert json_data['message'] == 'No file or name provided'

def test_upload_with_invalid_file_type(client):
    with open('test_file.txt', 'w') as f:  # Create the file before running the test
        f.write('This is a test file.')
    data = {
        'photo': (open('test_file.txt', 'rb'), 'test_file.txt'),
        'name': 'test_image'
    }
    response = client.post('/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['message'] == 'Invalid file type'
    os.remove('test_file.txt')  # Remove the file after running the test
def test_upload_valid_file(client, test_image_file):
    data = {
        'photo': (open(test_image_file, 'rb'), test_image_file),
        'name': 'test_image'
    }
    response = client.post('/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == 'Image uploaded and processing started.'

