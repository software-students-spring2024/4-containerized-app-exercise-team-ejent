import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
from fer import FER
import cv2, pymongo, time


def get_emotion(image):
    """
    Method for detecting emotions in an image containing humans, using the fer library. Works with images containing multiple faces.
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
        return f"Error in detecting emotions: {str(e)}"

def connect_db():
    """
    Method for connecting to the MongoDB Atlas database.
    """
    client = pymongo.MongoClient(os.environ['MONGO_URI'])
    db = client["emotionDB"]
    collection = db["emotions"]
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
                        #"title" or name? , need a way to id image
                        "emotion": emotion_message,
                        "processed": True,
                    }
                },
            )
        time.sleep(1)
    client.close()

if __name__ == "__main__":
    # Test the get_emotion method for now
    im = cv2.imread('./test0.png')
    print(get_emotion(im))
