import cv2
import numpy as np
from image_processing import *
from model import predict
from evaluate import evaluate
import os
from pathlib import Path

PATH = Path('.')
IMAGE_PATH = PATH/'images'
SAMPLE_PATH = PATH/'samples'/'from-inference'

labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '+', '-', '/', 'x']


def main():
    # read and process image
    os.chdir(IMAGE_PATH)
    img = resize(cv2.imread('img.jpg', cv2.IMREAD_GRAYSCALE))
    #show(img, 'original image')

    preprocessed = preprocess(img)
    objects, annotated = find_objects(preprocessed)
    #show(annotated, 'annotated image')

    # extract objects
    objects_processed = []
    for o in objects:
        if len(o) < 10 and len(o[0]) < 10:
            continue
        objects_processed.append(resize_and_pad(o, width=16, height=16))

    # classsify objects
    equation = []
    for o in objects_processed:
        #show(o, 'object')
        prediction = np.argmax(
                predict(
                    np.expand_dims(o.astype("float32") / 255, -1)
                )
            )

        os.chdir(SAMPLE_PATH)
        cv2.imwrite(f'{labels[int(prediction)]}-{np.random.randint(20000, size=1)[0]}.jpg', o)

        equation.append(prediction)

    return evaluate(equation)


