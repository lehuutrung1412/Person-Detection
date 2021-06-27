from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import cv2
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('ko co file')
        else:
            print('co file')
            # Receive image
            img = request.files.get('file')
            img_ext = img.filename.split('.')[-1].upper()
            print(img_ext)
            img = img.read()
            numpy_img = np.frombuffer(img, np.uint8)
            img = cv2.imdecode(numpy_img, cv2.IMREAD_COLOR)
            print(img.shape[0], img.shape[1])
            plt.imshow(img)
            plt.show()
            # Send image
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img.astype("uint8"))
            raw_bytes = io.BytesIO()
            img.save(raw_bytes, "JPEG")
            raw_bytes.seek(0)
            img_base64 = base64.b64encode(raw_bytes.read())
            return jsonify({'status': str(img_base64)})

            # return send_file(img, attachment_filename='logo.png', mimetype='image/png')
        # return 'oke'
    return 'not post'


if __name__ == "__main__":
    app.run()

