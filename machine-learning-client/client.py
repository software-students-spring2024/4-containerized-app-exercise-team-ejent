"""
Machine learning client for detecting emotions in images.
This client connects to a MongoDB Atlas database, retrieves images.
"""
import base64
from PIL import Image
import io
from deepface import DeepFace
import time
import pymongo
import numpy as np
# pylint: disable=all
def get_emotion(image):
    """
    Method for detecting emotions in an image containing humans,
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
