import cv2
import numpy as np


def yolo_detect(img, weights='yolov4.weights', config='yolov4.cfg', thresh=0.25, nms=0.4):
    # Load darknet
    net = cv2.dnn.readNetFromDarknet('../yolov4/' + config, '../yolov4/' + weights)
    layer = net.getLayerNames()
    layer = [layer[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    # Prepare
    (H, W) = img.shape[:2]
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outs = net.forward(layer)
    boxes = list()
    confidences = list()
    class_ids = list()
    # Get result
    for output in layer_outs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > thresh:
                box = detection[0:4] * np.array([W, H, W, H])
                (center_x, center_y, width, height) = box.astype("int")
                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, thresh, nms)
    if len(indexes) > 0:
        for i in indexes.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return cv2.resize(img, (600, int(600 * H / W)))
