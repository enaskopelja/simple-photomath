import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import numpy as np
from image_processing import *

from pathlib import Path
from tqdm import tqdm
import os

NUM_CLASSES = 16
PATH = Path('C:/Users/Ena/PycharmProjects/poorPM')
DATA_PATH = Path('C://Users/Ena/PycharmProjects/shit/data')
MODEL_PATH = PATH/'model'
SAMPLE_PATH = PATH/'samples'


def shuffle(a, b):
    tmp = list(zip(a, b))
    np.random.shuffle(tmp)
    return zip(*tmp)


def import_data():
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    i = 0
    for pth in DATA_PATH.iterdir():
        if not pth.is_dir():
            continue

        print(f"processing {str(pth)[-1]}")
        data = []

        j = 0
        for imagefile in tuple(Path(pth).glob("*.jpg")):
            img = resize_and_pad(preprocess(cv2.imread(str(imagefile), cv2.IMREAD_GRAYSCALE)))
            data.append(dilate(img) if j % 7 else img)
            j += 1

        data = np.array(data)
        #data = np.tile(data, (10, 1, 1))
        #print(data.shape[0], "samples of:")
        #cv2_imshow(invert(data[len(data) - 1]))
        # append
        cutoff = int(0.7 * data.shape[0])

        x_train = np.concatenate((x_train, data[:cutoff]), axis=0)
        x_test = np.concatenate((x_test, data[cutoff:]), axis=0)
        y_train = np.append(y_train, np.repeat(10 + i, cutoff))
        y_test = np.append(y_test, np.repeat(10 + i, data.shape[0] - cutoff))

        #os.chdir(SAMPLE_PATH/f'{str(pth)[-1]}')
        #for j in range(10):
        #    cv2.imwrite(
        #        f'{str(pth)[-1]}-{j}.jpg', data[j]
        #    )

        i += 1

    x_train, y_train = shuffle(x_train, y_train)
    x_test, y_test = shuffle(x_test, y_test)

    return np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)


def data_prep(x_train, y_train, x_test, y_test):
    print("------------DATA PREP")
    # Scale images to [0, 1] range
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255

    # image shape (28, 28, 1)
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    assert x_train.shape[1:] == (28, 28, 1)
    assert x_test.shape[1:] == (28, 28, 1)
    # todo zasto ovo ne valja: assert x_train.shape == (None, 28, 28, 1)
    # todo zasto ovo ne valja: assert x_test.shape == (None, 28, 28, 1)

    # convert class vectors to binary class matrices
    num_classes = NUM_CLASSES
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    return x_train, y_train, x_test, y_test


def train_model():
    x_train, y_train, x_test, y_test = data_prep(*import_data())

    # model
    model = keras.Sequential([
            keras.Input(shape=(28, 28, 1)),
            layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.6),
            layers.Dense(NUM_CLASSES, activation="softmax"),  # NUM_CLASSES = 16
        ]
    )
    # model.summary()

    # train
    batch_size = 256
    epochs = 3

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1, shuffle=True)
    model.save(MODEL_PATH)


def predict(img):
    return keras.models.load_model(MODEL_PATH).predict(
                tf.convert_to_tensor(
                    np.array(np.expand_dims(img, 0))
                )
    )


