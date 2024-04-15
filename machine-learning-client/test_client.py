from unittest.mock import patch, MagicMock
import pytest, os
from client import connect_db, get_emotion
from PIL import Image

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

def test_bad_connection():
    """Testing loop exit for connection method"""
    # pylint: disable=unused-variable
    with patch("pymongo.MongoClient"):
        connect_db(False)
