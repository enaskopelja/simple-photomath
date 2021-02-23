from keras.preprocessing.image import ImageDataGenerator
from image_processing import gaussian_blur, preprocess
import numpy as np


def preprocessing_function(img):
    img = img.astype(np.uint8)
    preprocessed = preprocess(img)
    return np.expand_dims(preprocessed.astype(np.float32), axis=-1)


DATAGENPARAMS = {
    "rescale": 1. / 255,
    "preprocessing_function": preprocessing_function,
}


class DatasetGenerator:
    def __init__(
            self,
            *,
            datagenparams=None,
            data_path,
    ):
        self.data_path = data_path

        if datagenparams is None:
            self.datagenparams = DATAGENPARAMS

        self.datagen = None

    def __call__(
            self,
            *,
            batch_size: int = 1,
            path_from_data_root: str = '',
    ):
        datagen = ImageDataGenerator(
            **self.datagenparams,
            dtype=np.uint8
        )

        return datagen.flow_from_directory(
            self.data_path / path_from_data_root,
            target_size=(45, 45),
            class_mode='categorical',
            color_mode='grayscale',
            batch_size=batch_size,
        )
