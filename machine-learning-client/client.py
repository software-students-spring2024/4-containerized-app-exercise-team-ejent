import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
from fer import FER
import cv2


def get_emotion(image):
    detector = FER(mtcnn=True)
    emotions = detector.detect_emotions(image)
    i = 1
    res = ""
    for box in emotions:
        max_emotion = max(box['emotions'], key=lambda x: box['emotions'][x])
        res += (f"Person {i} seems to be feeling {max_emotion}\n")
        i += 1
    return res

#im = cv2.imread('./test1.png')
#print(get_emotion(im))
"""
machine-learning-client % python client.py
Person 1 is feeling happy
Person 2 is feeling happy
Person 3 is feeling sad
"""
