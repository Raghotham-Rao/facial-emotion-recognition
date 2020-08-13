import numpy as np
import cv2

# interacting with the webcam
cap = cv2.VideoCapture('../data/y2mate.com - Best Of Michael Scott_pioHMycjOfs_360p.mp4')

# creating the cascade reference
cascade = cv2.CascadeClassifier('../haar_cascade/haar_cascade_frontalface.xml')

# showing the video
while True:

    # getting the frame
    ret, frame = cap.read()

    # converting to a gray frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detecting the faces using the cascade
    faces = cascade.detectMultiScale(gray, 1.2, minNeighbors= 5, minSize= (20, 20))

    # marking the faces on the video
    for (x, y, w, h) in faces:
        # drawing the rectangle
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (153, 102, 0), 2)
        # labelling the face
        frame = cv2.putText(frame, "Face", (x, y + h + 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 153, 102), thickness=2)

    cv2.imshow("Live video", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()