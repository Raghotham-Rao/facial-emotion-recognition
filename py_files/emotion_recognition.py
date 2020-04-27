#import os
#os.environ['KERAS_BACKEND'] = 'theano'
import numpy as np
import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers import Activation
from keras.layers.core import Dense, Flatten
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import *
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import itertools
import cv2
from keras.models import load_model
from PIL import Image


class EmotionRecognizer:

    emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

    def __init__(self):
        # load model
        self.model = load_model('../models/6-conv-91train-66val.h5')

    def getEmotion(self, face):
        prediction = self.model.predict(face)
        emotion = self.emotions[np.where(prediction == np.amax(prediction))[1][0]]
        # print(*(np.where(prediction == np.amax(prediction))), sep="\t")
        return emotion
