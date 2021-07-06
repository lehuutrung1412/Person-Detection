import cv2
import base64
from PIL import Image
import io


def convert_img_base64(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img.astype("uint8"))
    raw_bytes = io.BytesIO()
    img.save(raw_bytes, "JPEG")
    raw_bytes.seek(0)
    return base64.b64encode(raw_bytes.read())


def sliding_window(image, step_size, window_size):
    for y in range(0, image.shape[0], step_size[1]):
        for x in range(0, image.shape[1], step_size[0]):
            yield x, y, image[y:y + window_size[1], x:x + window_size[0]]


def bb_intersection(box_a, box_b):
    x_a = max(box_a[0], box_b[0])
    y_a = max(box_a[1], box_b[1])
    x_b = min(box_a[2], box_b[2])
    y_b = min(box_a[3], box_b[3])
    t1 = x_b - x_a + 1
    t2 = y_b - y_a + 1
    if t1 <= 0 or t2 <= 0:
        intersection_area = 0
    else:
        intersection_area = (x_b - x_a + 1) * (y_b - y_a + 1)
    return intersection_area


def bb_intersection_over_union(box_a, box_b):
    intersection_area = bb_intersection(box_a, box_b)
    box_a_area = (box_a[2] - box_a[0] + 1) * (box_a[3] - box_a[1] + 1)
    box_b_area = (box_b[2] - box_b[0] + 1) * (box_b[3] - box_b[1] + 1)
    iou = intersection_area / (box_a_area + box_b_area - intersection_area)
    return iou


def pyramid(image, downscale=1.5, min_size=(30, 30)):
    yield image
    while True:
        w = int(image.shape[1] / downscale)
        h = int(image.shape[0] / downscale)
        image = cv2.resize(image, (w, h))
        if image.shape[0] < min_size[1] or image.shape[1] < min_size[0]:
            break
        yield image
