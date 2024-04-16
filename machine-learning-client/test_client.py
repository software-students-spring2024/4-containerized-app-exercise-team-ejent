"""
This module contains tests for the client module.
"""
from unittest.mock import patch
# import time
from client import connect_db, run_connection
# from client import connect_db, get_emotion, run_connection, DeepFace
# from PIL import Image
# from pymongo import MongoClient
# import pytest

def test_bad_connection():
    """Testing loop exit for connection method"""
    # pylint: disable=unused-variable
    with patch("pymongo.MongoClient"):
        connect_db(False)


def test_connect_option_true():
    """When the flag for running is true"""
    with patch("client.connect_db") as mock_connection:
        run_connection(True)
        mock_connection.assert_called_once_with(True)
