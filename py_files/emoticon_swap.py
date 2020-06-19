import numpy as np
import cv2
from face_recognition import FaceRecognizer
from emotion_recognition import EmotionRecognizer
from PIL import Image
from time import sleep
import matplotlib.pyplot as plt
import io


class FaceEmoSwap:

    def __init__(self):
        self.recognizer = FaceRecognizer()
        self.e_recognizer = EmotionRecognizer()
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']


    def recognize_within_image(self, filepath, showgraphs=True):
        img = cv2.imread(filepath)
        
        print("img read")
        
        face_boundaries = self.recognizer.getFaces(img)
        sleep(1)
        labels = []
        predictions = []

        print("faces recognized")

        for (x, y, w, h) in face_boundaries:
            face = img[x: x + w, y: y + h]
            try:
                face = cv2.resize(face, (48, 48))
            except:
                continue
            prediction = self.e_recognizer.getEmotions(np.expand_dims(face, axis=0))
            predictions.append(prediction)
            labels.append(self.getEmotion(prediction))
            sleep(1)

        print("boundaries obtained")

        img = self.swap_with_emoticon(img, face_boundaries, labels)
        cv2.imshow("image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def recognize_within_video(self, filepath="", live_cam=False):
        source = filepath
        refresh_rate = 25
        if(live_cam):
            source = 0
            refresh_rate = 1
        cap = cv2.VideoCapture(source)

        while True:
    
            ret, frame = cap.read()

            try:
                face_boundaries = self.recognizer.getFaces(frame)
                labels = []
                predictions = []

                for (x, y, w, h) in face_boundaries:
                    face = np.copy(frame[x: x + w, y: y + h])

                    try:
                        face = cv2.resize(face, (48, 48))
                    except:
                        continue

                    prediction = self.e_recognizer.getEmotions(np.expand_dims(face, axis=0))
                    predictions.append(prediction)
                    labels.append(self.getEmotion(prediction))

                frame = self.swap_with_emoticon(frame, face_boundaries, labels)
                
            except :
                print('in')
                pass
        
            cv2.imshow("Live video", frame)
        	
            if cv2.waitKey(refresh_rate) & 0xFF == ord('q'): 
                    break
        
        cv2.destroyAllWindows()
        cap.release()
        
        return 'done'


    def getEmotion(self, prediction):
        emotion = self.emotions[np.where(prediction == np.amax(prediction))[1][0]]
        return emotion

    
    def swap_with_emoticon(self, img, faces, labels):
        i = 0
        for (x, y, w, h), label in zip(faces, labels):
            emoticon = cv2.imread("../emoticons/" + label + ".png")
            emoticon_width = w if w > h else h
            emoticon = cv2.resize(emoticon, (emoticon_width, emoticon_width))
            try:
                img[y: y + emoticon_width, x: x + emoticon_width, : ] = emoticon
            except:
                pass
            i += 1
        
        return img

fes = FaceEmoSwap()
# fes.recognize_within_image(filepath="../data/9faces.jpg")
# fes.recognize_within_video(filepath="../data/y2mate.com - Best Of Michael Scott_pioHMycjOfs_360p.mp4")
fes.recognize_within_video(live_cam=True)