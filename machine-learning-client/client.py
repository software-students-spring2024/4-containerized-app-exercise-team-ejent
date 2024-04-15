"""
Machine learning client for detecting emotions in images.
This client connects to a MongoDB Atlas database, retrieves images.
It then processes the images to detect emotions for target faces, and updates db with the results.
Time: sleep for a second
Pymongo: connect to MongoDB
Deepface: to detect emotions in images
Numpy: numerical operations
...
"""
import base64
from PIL import Image
import io
from deepface import DeepFace
import time
import pymongo
import numpy as np
    
def get_emotion(image):
    """
    Method for detecting emotions in an image containing humans, 
    using the deepface library. Works with images containing multiple faces.
    """
    try:
        bin_data = base64.b64decode(image)
        im = Image.open(io.BytesIO(bin_data))
        image_np = np.array(im)
        obj = DeepFace.analyze(image_np, actions=['emotion'])
        emotions = obj[0]['emotion']
        return emotions
    except Exception as e:
        return f"ERROR: Couldn't detect a face for emotion. {e}"


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
        if temp.find_one():
            temp.update_one(
                {
                    "_id": temp.find_one()["_id"]},  
                {
                    "$set": {
                        "emotion": emotion_message,
                        "is_processed": True,
                    }
                },
            )
        #print("REACHED HERE!")
        time.sleep(1)
    client.close()


if __name__ == "__main__":
     #im = cv2.imread('./test0.png')
    connect_db(True)
