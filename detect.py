from PIL import Image
import numpy as np
import joblib
from utils import *
from skimage.feature import hog
from imutils.object_detection import non_max_suppression


def detect(image, model='model.dat', img_w=350, img_h=0, size=(64, 128), step_size=(9, 9), downscale=2, score=1, thresh=0):
    # If this is a path of image
    if type(image) == str:
        image = cv2.imread(image)
    if img_h == 0:
        img_h = int(image.shape[0] * img_w / image.shape[1])
    res_img = image.copy()
    image = cv2.resize(image, (img_w, img_h))
    # List to store the detections
    detections = []
    # The current scale of the image
    model = joblib.load('../models/' + model)
    scale = 0
    for im_scaled in pyramid(image, downscale=downscale, min_size=size):
        for (x, y, window) in sliding_window(im_scaled, step_size, size):
            if window.shape[0] != size[1] or window.shape[1] != size[0]:
                continue
            window_img = Image.fromarray(window.astype("uint8"))
            window = window_img.convert('LA')
            fd = hog(window, orientations=9, pixels_per_cell=(8, 8), visualize=False, cells_per_block=(3, 3))
            fd = fd.reshape(1, -1)
            pred = model.predict(fd)
            if pred == 1:
                if model.decision_function(fd) > score:
                    detections.append(
                        (int(x * (downscale ** scale)), int(y * (downscale ** scale)), model.decision_function(fd),
                         int(size[0] * (downscale ** scale)),
                         int(size[1] * (downscale ** scale))))
                    # detections.append([x, y, model.decision_function(fd), size[0], size[1]])
        scale += 1
    rects = np.array([[x, y, x + w, y + h] for (x, y, _, w, h) in detections])
    sc = [score[0] for (x, y, score, w, h) in detections]
    # print ("sc: ", sc)
    sc = np.array(sc)
    pick = non_max_suppression(rects, probs=sc, overlapThresh=thresh)
    im_w = res_img.shape[1]
    im_h = res_img.shape[0]
    for (x1, y1, x2, y2) in pick:
        xmin = int(x1 * im_w / img_w)
        ymin = int(y1 * im_h / img_h)
        xmax = int(x2 * im_w / img_w)
        ymax = int(y2 * im_h / img_h)
        cv2.rectangle(res_img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        # cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # cv2.putText(image, 'Person', (x1-2, y1-2), 1, 0.75, (121, 12, 34), 1)
    return cv2.resize(res_img, (600, int(600*im_h/im_w)))



