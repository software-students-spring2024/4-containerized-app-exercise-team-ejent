# pylint: disable=all
"""
Machine learning client for detecting emotions in images.
This client connects to a MongoDB Atlas database, retrieves images.
"""
import io
import pytest
from main import app

@pytest.fixture
def client():
    """Client"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# pylint: disable=redefined-outer-name
def test_index(client):
    """Test the index route"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<!DOCTYPE html>\n<html>\n<head>\n" in response.data

def test_upload_file_no_photo(client):
    """Test the /upload endpoint with no photo"""
    response = client.post("/upload", data={"name": "test"})
    assert response.status_code == 200
    assert b"No photo provided" in response.data

def test_upload_file_no_name(client):
    """Test the /upload endpoint with no name"""
    data = {"photo": (io.BytesIO(b"this is a test"), "test.jpg")}
    response = client.post("/upload", data=data)
    assert response.status_code == 200
    assert b"No name provided" in response.data
