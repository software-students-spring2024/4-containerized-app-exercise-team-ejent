from unittest.mock import patch, MagicMock
import pytest, os
from client import get_emotion, connect_db, FER
#from PIL import Image

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

def test_bad_connection():
    """Testing loop exit for connection method"""
    # pylint: disable=unused-variable
    with patch("pymongo.MongoClient"):
        connect_db(False)
