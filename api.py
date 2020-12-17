from flask import Flask, request
from flask_cors import CORS

import os
import base64
from main import main as calculate
from pathlib import Path

app = Flask(__name__)
APP_ROOT = Path('.')
CORS(app)


@app.route("/api/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        save_to = APP_ROOT / 'images'

        if not Path.is_dir(save_to):
            Path.mkdir(save_to)

        img = request.files["image"]
        if img.filename == '':
            print('No selected file')
            return "No selected file"

        destination = "/".join([str(save_to.absolute()), "img.jpg"])
        img.save(destination)
        return "200"


@app.route("/api/webcam", methods=['POST'])
def webcam():
    if request.method == 'POST':
        data = request.form.get('image')
        _, img = data.split(',')

        os.chdir(os.path.join(APP_ROOT, 'images'))
        with open('img.jpg', 'wb') as f:
            f.write(base64.b64decode(img))
        return "200"


@app.route("/api", methods=['GET'])
def solution():
    return {"solution": f'{calculate()}'}


if __name__ == "__main__":
    app.run(port=5000, debug=True)