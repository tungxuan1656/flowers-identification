import os

from numpy.core.numeric import load
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras.applications.vgg16 import VGG16, preprocess_input
from keras.models import Model
from keras.layers import Dense, Flatten

import numpy as np
from PIL import Image


def get_model():
    model = VGG16(include_top=False, input_shape=(256, 256, 3))
    for layer in model.layers:
        layer.trainable = False
    flat1 = Flatten()(model.layers[-1].output)
    class1 = Dense(512, activation='relu')(flat1)
    output = Dense(17, activation='softmax')(class1)
    # define new model
    model = Model(inputs=model.inputs, outputs=output)
    # summarize
    return model


def load_image(path):
    img = Image.open(path)
    img = img.resize((256, 256))
    img = np.array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img


def prediction(model, image_path):
    image = load_image(image_path)
    result = model.predict(image)[0]
    return result


if __name__ == '__main__':
    model = get_model()
    model.load_weights('./17flowers_weights.h5')
    # model.summary()

    img = load_image('test.jpg')

    result = prediction(model, 'test.jpg')
    print(result)
    pass
