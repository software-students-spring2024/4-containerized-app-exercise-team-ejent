"""
Machine learning client for detecting emotions in images.
This client connects to a MongoDB Atlas database, retrieves images.
It then processes the images to detect emotions for target faces, and updates db with the results.
Time: sleep for a second
Pymongo: connect to MongoDB
Deepface: to detect emotions in images
Numpy: numerical operations
"""

import base64
import io
import time
from PIL import Image
from deepface import DeepFace
import pymongo
import numpy as np


# pylint: disable=broad-exception-caught
def get_emotion(image):
    """
    Method for detecting emotions in an image containing humans,
    using the deepface library. Works with multiple face, returns sentiment for majority.
    """
    try:
        bin_data = base64.b64decode(image)
        im = Image.open(io.BytesIO(bin_data))
        image_np = np.array(im)
        obj = DeepFace.analyze(image_np, actions=["emotion"], enforce_detection=False)
        emotions = obj[0]["emotion"]
        return emotions
    except Exception as e:
        return f"ERROR: {e}"


def run_connection(option):
    "arranged for utility"
    connect_db(option)


# pylint: disable=inconsistent-return-statements
def connect_db(option):
    """
    Method for connecting to the MongoDB client.
    """
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["emotion_detection"]
    temp = db["temp_store"]

    while option:
        while temp.find_one() is None:
            pass
        x = temp.find_one()
        emotion_message = get_emotion(x["photo"])
        if not emotion_message:
            return "No emotions found"
        if temp.find_one():
            temp.update_one(
                {"_id": temp.find_one()["_id"]},
                {
                    "$set": {
                        "emotion": emotion_message,
                        "is_processed": True,
                    }
                },
            )
        time.sleep(1)
    client.close()


if __name__ == "__main__":
    run_connection(True)
