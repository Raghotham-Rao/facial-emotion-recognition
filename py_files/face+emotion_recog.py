import numpy as np
import cv2
from face_recognition import FaceRecognizer
from emotion_recognition import EmotionRecognizer
from PIL import Image
from time import sleep

recognizer = FaceRecognizer()

e_recognizer = EmotionRecognizer()

'''while True:
    path = input("Enter the image name:\n")

    if path == 'q':
        break

    try:
        img = cv2.imread('../data/' + path)
        
        print("img read")
        
        face_boundaries = recognizer.getFaces(img)
        sleep(1)
        labels = []

        print("faces recognized")

        for (x, y, w, h) in face_boundaries:
            face = img[x: x + w, y: y + h]
            try:
                face = cv2.resize(face, (48, 48))
            except:
                continue
            labels.append(e_recognizer.getEmotion(np.expand_dims(face, axis=0)))
            sleep(1)

        print("boundaries obtained")

        img = recognizer.labelFaces(img, face_boundaries, labels)
        sleep(1)
        print("faces marked")

        cv2.imshow("the image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except:
        print('error loading image')
        pass'''

# cap = cv2.VideoCapture('../data/y2mate.com - Best Of Michael Scott_pioHMycjOfs_360p.mp4')
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('../data/basic_emotions2.mp4')
# cap.set(cv2.CAP_PROP_FPS, 30)

while True:
    
    ret, frame = cap.read()

    try:
        face_boundaries = recognizer.getFaces(frame)
        labels = []

        for (x, y, w, h) in face_boundaries:
            face = np.copy(frame[x: x + w, y: y + h])
            try:
                face = cv2.resize(face, (48, 48))
            except:
                continue
            labels.append(e_recognizer.getEmotion(np.expand_dims(face, axis=0)))
            
        frame = recognizer.labelFaces(frame, face_boundaries, labels)
    except :
        print('in')
        pass

    cv2.imshow("Live video", frame)
    #cv2.imshow("Live video", frame)
    #cv2.imshow("Live video", frame)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

print("done")
