import base64
import io
import pytest
from flask import Flask
from main import app
from werkzeug.datastructures import FileStorage
#update
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


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


# def test_upload_file_with_photo(client):
#     """Test the /upload endpoint with a photo"""
#     data = {"name": "test", "photo": (io.BytesIO(b"this is a test image"), "test.jpg")}
#     response = client.post("/upload", data=data, content_type="multipart/form-data")
#     assert response.status_code == 200
#     assert b"<!DOCTYPE html>\n<html>\n<head>\n" in response.data


# def test_result(client):
#     """Test the /result endpoint with no processed document"""
#     response = client.get("/result")
#     assert response.status_code == 200
