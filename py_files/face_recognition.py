import numpy as np
import matplotlib.pyplot as plt
import cv2
# from time import sleep

# reading an image
class FaceRecognizer:

    def __init__(self):
        # creating a reference to cascade
        self.cascade = cv2.CascadeClassifier('../haar_cascade/haar_cascade_frontalface.xml')

    def getFaces(self, img):
        # converting the image to gray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    

        # recognising the faces in the image
        faces = self.cascade.detectMultiScale(gray, 1.2, minNeighbors= 2, minSize= (30, 30))

        return faces

    def labelFaces(self, img, faces, labels):
        # drawing a rectangle around the faces
        for (x, y, w, h), label in zip(faces, labels):
            # drawing the rectangle
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (153, 102, 0), 2)
            img = cv2.rectangle(img, (x, y + h), (x + w, y + h + 20), (0, 0, 0), -1)
            # labelling the face
            img = cv2.putText(img, label, (x, y + h + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 153, 102), thickness=1)
        
        return img

# img = cv2.imread('../data/expns9.jpeg')

# recognizer = FaceRecognizer()

# faces = recognizer.getFaces(img)

# cv2.imshow("Original Image", img)

# img = recognizer.labelFaces(img, faces, ["Face" for i in range(len(faces))])

# cv2.imshow("Faces Recognized", img)

# cv2.waitKey(0)
# # sleep(15)
# cv2.destroyAllWindows()
