import tensorflow.keras as keras
from tensorflow.keras.models import load_model


class EmotionRecognizer:

    emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

    def __init__(self, model_path):
        # load model
        self.model = load_model(model_path)

    def getEmotions(self, face):
        prediction = self.model.predict(face)
        return prediction
