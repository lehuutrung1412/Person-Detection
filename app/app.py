from flask import Flask, render_template, request, jsonify
from detect import *
from yolo_python import yolo_detect

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html', name_model='HOG with SVM and Yolov4')


@app.route("/upload", methods=['POST'])
def upload():
    # name_model = str(request.referrer).split('/')[-1]
    if request.method == 'POST':
        if 'file' not in request.files:
            print('File was not found!')
        else:
            print('File was found!')
            # Receive image
            img = request.files.get('file')
            # img_ext = img.filename.split('.')[-1].upper()
            # print(img_ext)
            img = img.read()
            numpy_img = np.frombuffer(img, np.uint8)
            img = cv2.imdecode(numpy_img, cv2.IMREAD_COLOR)
            # print(img.shape[0], img.shape[1])
            # Process image
            # if name_model == "yolo":
            #     img_yolo = yolo_detect(img)
            # else:
            img_hog = detect(img, 'models_well.dat',
                            score=0.4, thresh=0.45, img_w=300, img_h=150, downscale=1.5, step_size=(6, 6))
            img_yolo = yolo_detect(img)
            # Send image hog
            img_base64_hog = convert_img_base64(img_hog)
            # Send image yolo
            img_base64_yolo = convert_img_base64(img_yolo)

            return jsonify({'img_hog': str(img_base64_hog), 'img_yolo': str(img_base64_yolo)})
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
