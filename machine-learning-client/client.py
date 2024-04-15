"""
Machine learning client for detecting emotions in images.
This client connects to a MongoDB Atlas database, retrieves images.
It then processes the images to detect emotions for target faces, and updates db with the results.
OS: to set environment variable for ffmpeg
Time: to sleep for a second
Pymongo: to connect to MongoDB
FER: to detect emotions in images
...
"""
import os
import time
import pymongo
from fer import FER

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

def get_emotion(image):
    """
    Method for detecting emotions in an image containing humans, 
    using the fer library. Works with images containing multiple faces.
    """
    # edit to return just label
    try:
        detector = FER(mtcnn=True)
        emotions = detector.detect_emotions(image)
        i = 1
        res = ""
        for box in emotions:
            max_emotion = max(box['emotions'], key=lambda x: box['emotions'][x])
            res += (f"Person {i} seems to be feeling {max_emotion}\n")
            i += 1
        return res
    except Exception as e:
        return f"ERROR: Couldn't detect a face for emotion. {e}"

def connect_db(option):
    """
    Method for connecting to the MongoDB client.
    """
    client = pymongo.MongoClient("mongodb://mongodb:27017/")
    db = client["emotion_detection"]
    collection = db["emotion_images"]
    while option:
        while not collection.find_one():
            pass
        emotion_message = get_emotion(collection.find_one()["image"])
        if collection.find_one():
            collection.update_one(
                {
                    "_id": collection.find_one()["_id"]},  
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
    #im = cv2.imread('./test0.png')
    connect_db(True)
