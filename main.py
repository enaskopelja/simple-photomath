import cv2
import numpy as np
from image_processing import *
from model import predict
from evaluate import evaluate
import os
from pathlib import Path

PATH = Path('.')
IMAGE_PATH = PATH/'images'
SAMPLE_PATH = 'C:/Users/Ena/PycharmProjects/simple-pm/samples/from-inference'

labels = ['(', ')', '+', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', '/', 'x']


def main():
    # read and process image
    os.chdir(IMAGE_PATH)
    img = resize(cv2.imread('tst2.png', cv2.IMREAD_GRAYSCALE))
    # show(img, 'original image')

    preprocessed = preprocess(img)
    objects, annotated = find_objects(preprocessed)
    # show(annotated, 'annotated image')

    # extract objects
    objects_processed = []
    for o in objects:
        if len(o) < 10 and len(o[0]) < 10:
            continue

        resized_obj = resize_obj(o, width=45, height=45)

        for_eval = np.expand_dims(
            np.array(resized_obj, dtype=np.float32),
            axis=-1
        )

        objects_processed.append(
            for_eval/255.
        )

    # classsify objects
    # for o in objects_processed:
    #     show(o, 'object')
        # prediction = np.argmax(
        #         predict(
        #             o)
        #         )
        #     )
        # os.chdir(SAMPLE_PATH)
        # cv2.imwrite(f'{labels[int(prediction)]}-{np.random.randint(20000, size=1)[0]}.jpg', o)
        #
        # equation.append(prediction)

    preds = predict(np.array(objects_processed, dtype=np.float32))

    equation = [int(np.argmax(pred)) for pred in preds]
    return evaluate(equation)


if __name__ == '__main__':
    print(main())

