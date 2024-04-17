"Web app test file"
import io
import pytest
from main import app


@pytest.fixture(name="mock_client")
def client():
    """Create a test client for the flask application"""
    app.config["TESTING"] = True
    with app.test_client() as mock_client:
        yield mock_client


def test_index(mock_client):
    """Test the index route"""
    response = mock_client.get("/")
    assert response.status_code == 200
    assert b"<!DOCTYPE html>\n<html>\n<head>\n" in response.data


def test_upload_file_no_photo(mock_client):
    """Test the /upload endpoint with no photo"""
    response = mock_client.post("/upload", data={"name": "test"})
    assert response.status_code == 200
    assert b"No photo provided" in response.data


def test_upload_file_no_name(mock_client):
    """Test the /upload endpoint with no name"""
    data = {"photo": (io.BytesIO(b"this is a test"), "test.jpg")}
    response = mock_client.post("/upload", data=data)
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
