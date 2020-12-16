import numpy as np
import cv2


def show(img, title):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def threshold(img):
    blur = cv2.GaussianBlur(img, (5, 5), 0)

    _, img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img


def invert(img):
    return 255 - img


def opening_transform(img, kernel=np.ones((2, 2), np.uint8)):
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)


def closing_transform(img, kernel=np.ones((2, 2), np.uint8)):
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)


def dilate(img, kernel=np.ones((2, 2), np.uint8)):
    return cv2.dilate(img, kernel, iterations=1)


def preprocess(img, iter=3):
    #approximate background
    dilated = dilate(opening_transform(img), np.ones((5, 5), np.uint8))
    blur_bg = dilated
    for i in range(iter):
        blur_bg = cv2.GaussianBlur(blur_bg, (5, 5), 0)

    #remove background
    rm_bg = cv2.absdiff(img, blur_bg)

    return opening_transform(threshold(rm_bg))


def find_objects(img):
    contours, _ = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    objects = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(imgRGB, (x, y), (x + w, y + h), (0, 0, 255), 2)
        objects.append((img[y:y + h, x:x + w], x))  # later sort by x
        cv2.drawContours(imgRGB, contour, -1, (255, 0, 0), 2)

    objects.sort(key=lambda o: o[1])

    return [o[0] for o in objects], imgRGB


def resize_and_pad(img, width=20, height=20):
    w, h = img.shape

    pad_left = int((28 - width) / 2)
    pad_top = int((28 - height) / 2)

    if w > h:
        left = int((w - h) / 2)
        r = cv2.copyMakeBorder(img, 0, 0, left, w - h - left, 0)
    elif w < h:
        top = int((h - w) / 2)
        r = cv2.copyMakeBorder(img, top, h - w - top, 0, 0, 0)
    else:
        r = img

    tmp = np.zeros((28, 28))
    tmp[pad_left:28-pad_left, pad_top:28-pad_top] = cv2.resize(r, (width, height))
    return tmp


def resize(img, max_dim=400):
    w, h = img.shape
    if w > h:
        return cv2.resize(img, (int(h * max_dim/w), max_dim))
    else:
        return cv2.resize(img, (max_dim, int(w * max_dim/h)))

