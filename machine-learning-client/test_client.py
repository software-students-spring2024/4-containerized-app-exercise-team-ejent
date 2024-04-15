from unittest.mock import patch
import mongomock
import base64
import io, cv2, os, pytest
from client import connect_db, get_emotion, run_connection, DeepFace
from PIL import Image
from pymongo import MongoClient
import pytest
import time


def test_bad_connection():
    """Testing loop exit for connection method"""
    #pylint: disable=unused-variable
    with patch("pymongo.MongoClient"):
        connect_db(False)

def test_connect_option_true():
    """When the flag for running is true"""
    with patch("client.connect_db") as mock_connection:
        run_connection(True)
        mock_connection.assert_called_once_with(True)


def test_connect_option_false():
    """run_connection method:false"""
    with patch("client.connect_db") as mock_connection:
        run_connection(False)
        mock_connection.assert_called_once_with(False)


# def test_get_emotion_invalid_input():
#     with open("test1.png", "rb") as file:
#         image = file.read()
#         assert get_emotion("test")[:33] == "ERROR: cannot identify image file"
#         assert get_emotion(image)[:33] == "ERROR: cannot identify image file"

# def test_get_emotion_success():
#     """Testing connection"""
#     # pylint: disable=unused-variable
#     with patch("pymongo.MongoClient") as mock_client:
#         with patch("pymongo.collection.Collection") as mock_collection:
#             mock_collection.find_one.return_value = {
#                 "_id": "",
#                 "photo": base64.b64encode(cv2.imread("test1.png")).decode("utf-8"),
#             }
#             connect_db(False)

# def test_get_emotion_with_image():
#     """Testing get_emotion method"""
#     with open(".machine/test0.png", "rb") as file:
#         image = file.read()
#         #print(get_emotion(base64.b64encode(image).decode("utf-8")))



