import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import cv2
from pathlib import Path

from image_processing import *
from DatasetGenerator import DatasetGenerator

NUM_CLASSES = 17
PATH = Path('C:/Users/Ena/PycharmProjects/simple-pm')
DATA_PATH = PATH / 'data'
MODEL_PATH = PATH / 'model'
SAMPLE_PATH = PATH / 'samples'


model = \
    keras.Sequential(
        [
            keras.Input(shape=(45, 45, 1)),

            layers.Conv2D(
                32,
                kernel_size=5,
                activation="relu",
                use_bias=True,
            ),
            layers.Conv2D(
                64,
                kernel_size=3,
                activation=None,
                use_bias=True,
            ),
            layers.MaxPool2D(
                pool_size=(2, 2),
            ),
            layers.Activation("relu"),

            layers.Flatten(),
            layers.Dense(128, activation="relu"),

            layers.Dense(64, activation=None),
            layers.Dropout(0.2),
            layers.Activation("relu"),

            layers.Dense(NUM_CLASSES, activation="softmax"),  # NUM_CLASSES = 17
        ]
    )


def import_data():
    datagen = DatasetGenerator(
        data_path=DATA_PATH,
    )
    train_ds = datagen(
        path_from_data_root='train',
        batch_size=64,
    )

    val_ds = datagen(
        path_from_data_root='val',
        batch_size=64,
    )

    test_ds = datagen(
        path_from_data_root='test',
        batch_size=1,
    )
    return train_ds, val_ds, test_ds


def train_model(
        *,
        epochs=2,
        learning_rate=1e-3,
):
    train_ds, val_ds, test_ds = import_data()

    model.compile(
        loss=tf.keras.losses.CategoricalCrossentropy(),
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        metrics=["accuracy"],
        run_eagerly=False,
    )

    model.fit(
        train_ds,
        steps_per_epoch=1000,
        epochs=epochs,
        validation_data=val_ds,
        validation_steps=100,
    )

    model.evaluate(
        test_ds,
        steps=100
    )


def save():
    model.save(MODEL_PATH)


def predict(images):
    return keras.models.load_model(MODEL_PATH/"model_v2").predict(
        tf.convert_to_tensor(images)
    )


if __name__ == '__main__':
    # train_model(epochs=3, learning_rate=2e-4)
    # model.save(MODEL_PATH / "test2")
    # train:  loss: 0.0972 - accuracy: 0.9714 - val_loss: 0.0620 - val_accuracy: 0.9842
    # test:  loss: 0.0749 - accuracy: 0.9900

    # train_model(epochs=4, learning_rate=2e-4)
    # model.save(MODEL_PATH/"test2")
    # train: loss: 0.0711 - accuracy: 0.9785 - val_loss: 0.0498 - val_accuracy: 0.9837
    # test:  loss: 0.0418 - accuracy: 0.9800

    # ---- 5. epoha:
    # train: loss: 0.0642 - accuracy: 0.9801 - val_loss: 0.0419 - val_accuracy: 0.9864
    # ---- 6. epoha:
    # train: loss: 0.0515 - accuracy: 0.9836 - val_loss: 0.0441 - val_accuracy: 0.9870
    # ---- 7. epoha:
    # train: loss: 0.0443 - accuracy: 0.9859 - val_loss: 0.0481 - val_accuracy: 0.9859
    # ---- 8. epoha:
    # train: loss: 0.0411 - accuracy: 0.9870 - val_loss: 0.0456 - val_accuracy: 0.9861
    # ---- 9. epoha:
    # train: loss: 0.0389 - accuracy: 0.9878 - val_loss: 0.0339 - val_accuracy: 0.9881
    # test: loss: 0.0017 - accuracy: 1.0000

    train_model(epochs=9, learning_rate=2e-4)
    model.save(MODEL_PATH/"test3")

    # train_model(epochs=20, learning_rate=1e-2)
