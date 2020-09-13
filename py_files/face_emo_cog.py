import numpy as np
import cv2
from face_recognition import FaceRecognizer
from emotion_recognition import EmotionRecognizer
from PIL import Image
from time import sleep
import matplotlib.pyplot as plt
import io


class FaceEmoCog:

    def __init__(self, config):
        self.recognizer = FaceRecognizer(config)
        self.e_recognizer = EmotionRecognizer(config["path_to_recognizer"])    
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']


    def recognize_within_image(self, filepath, showgraphs=True):
        # try:
        img = cv2.imread(filepath)
        
        print("img read")
        
        face_boundaries = self.recognizer.getFaces(img)
        sleep(1)
        labels = []
        predictions = []

        print("faces recognized")

        for (x, y, w, h) in face_boundaries:
            face = img[y: y + h, x: x + w]
            try:
                face = cv2.resize(face, (48, 48))
            except:
                continue
            prediction = self.e_recognizer.getEmotions(np.expand_dims(face, axis=0))
            predictions.append(prediction)
            labels.append(self.getEmotion(prediction))
            sleep(1)

        print("boundaries obtained")

        img = self.recognizer.labelFaces(img, face_boundaries, labels)
        img = Image.fromarray(img, mode='RGB')
        graph = self.getGraph(predictions)
        cv2.imshow("Emotion chart", graph)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return img


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
                    face = np.copy(frame[y: y + h, x: x + w])
                    try:
                        face = cv2.resize(face, (48, 48))
                    except:
                        continue
                    # labels.append(self.e_recognizer.getEmotion(np.expand_dims(face, axis=0)))
                    prediction = self.e_recognizer.getEmotions(np.expand_dims(face, axis=0))
                    predictions.append(prediction)
                    labels.append(self.getEmotion(prediction))

                frame = self.recognizer.labelFaces(frame, face_boundaries, labels)
                
            except :
                print('in')
                pass
        
            cv2.imshow("Live video", frame)
            try:
                cv2.imshow("Emotion Chart", self.getGraph(predictions))
            except:
                pass
        	
            if cv2.waitKey(refresh_rate) & 0xFF == ord('q'): 
                    break
        
        cv2.destroyAllWindows()
        cap.release()
        
        return 'done'


    def getEmotion(self, prediction):
        emotion = self.emotions[np.where(prediction == np.amax(prediction))[1][0]]
        return emotion


    def getGraph(self, predictions):
        try:
            plt.cla()
            plt.bar(self.emotions, predictions[0].tolist()[0], color="#0066ff")
            plt.ylim(0, 1)
            plt.title('Emotion Chart', fontdict={'fontsize': '20'})
            plt.xlabel('Emotion Classes', fontdict={'fontsize': '20'})
            plt.ylabel('Value', fontdict={'fontsize': '20'})
            # # plt.show()
            # plt.cla()
            # plt.figure(figsize=(10, 10))
            # faces = len(predictions)
            # cols = 2
            # rows = faces // 2 if faces % 2 == 0 else (faces + 1) // 2
            # fig, ax = plt.subplots(faces // 2 + 1, 2, sharex=True)
            # face = 0
            # for i in range(rows):
            #     for j in range(cols):
            #         ax[i, j].bar(self.emotions, predictions[face].tolist()[0], color="#0066ff")
            #         face += 1
            # print(faces)
            # for i in range(faces // 2 + 1):
            #     if i % 2 == 0:
            #         ax[i, 0].bar(self.emotions, predictions[i].tolist()[0], color="#0066ff")
            #     else:
            #         ax[i, 1].bar(self.emotions, predictions[i].tolist()[0], color="#7436ff")
            # plt.show()
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            graph = np.array(Image.open(buf))
            buf.close()
            return graph
        except:
            return None
