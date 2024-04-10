import os
from fer import FER
import cv2
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

img = cv2.imread("./testml.png")
detector = FER(mtcnn=True)
print(detector.detect_emotions(img))
#emotion, score = detector.top_emotion(img)
#print(emotion, score)
