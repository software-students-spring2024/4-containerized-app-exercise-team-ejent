"""
Machine learning client for detecting emotions in images.
This client connects to a MongoDB Atlas database, retrieves images.
It then processes the images to detect emotions for target faces, and updates db with the results.

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
        return f"ERROR: \n{str(e)}"

def connect_db():
    """
    Method for connecting to the MongoDB client.
    """
    client = pymongo.MongoClient("mongodb://mongodb:27017/")
    db = client["emotion_detection"]
    collection = db["emotion_images"]
    while True:
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
    # Test the get_emotion method for now, CV2 maybe not necessary
    #im = cv2.imread('./test0.png')
    #print(get_emotion(im))
    connect_db()
