import os
import uuid

from flask import Flask, request, render_template

from aws import analyze_image_aws
from azure import analyze_image_azure
from gcp import analyze_image_gcp

app = Flask(__name__)

UPLOAD_DIR = 'static/images/'


@app.route('/', methods=['GET', 'POST'])
def index():
    params = {}
    if request.method == 'POST':
        f = request.files['file']
        _, file_extension = os.path.splitext(f.filename)
        filename = '{}{}'.format(uuid.uuid4(), file_extension)
        image_path = os.path.join(UPLOAD_DIR, filename)
        f.save(image_path)
        results = analyze_image(image_path)
        params = {'results': results, 'filename': filename}

    return render_template('index.html', **params)


def analyze_image(image_path):
    with open(image_path, 'rb') as image_file:
        image_content = image_file.read()
        results = {'aws': analyze_image_aws(image_path, image_file, image_content),
                   'gcp': analyze_image_gcp(image_path, image_file, image_content),
                   'azure': analyze_image_azure(image_path, image_file, image_content)}
        return results


if __name__ == '__main__':
    app.run()
