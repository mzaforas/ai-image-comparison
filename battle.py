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
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' in request.files:
        f = request.files['file']
        _, file_extension = os.path.splitext(f.filename)
        filename = '{}{}'.format(uuid.uuid4(), file_extension)
        image_path = os.path.join(UPLOAD_DIR, filename)
        f.save(image_path)
    else:
        filename = ''
    return filename


@app.route('/analyze/<platform>/<image_name>', methods=['GET'])
def analyze(platform, image_name):
    image_path = os.path.join(UPLOAD_DIR, image_name)

    with open(image_path, 'rb') as image_file:
        image_content = image_file.read()
        if platform == 'aws':
            results = analyze_image_aws(image_path, image_file, image_content)
        elif platform == 'gcp':
            results = analyze_image_gcp(image_path, image_file, image_content)
        elif platform == 'azure':
            results = analyze_image_azure(image_path, image_file, image_content)
        else:
            results = {}

    return render_template('{}.html'.format(platform), results=results)


def save_image():
    f = request.files['file']
    _, file_extension = os.path.splitext(f.filename)
    filename = '{}{}'.format(uuid.uuid4(), file_extension)
    image_path = os.path.join(UPLOAD_DIR, filename)
    f.save(image_path)
    return filename


###################
# NO AJAX version #
###################


@app.route('/noajax', methods=['GET', 'POST'])
def index_no_ajax():
    params = {}
    if request.method == 'POST':
        filename = save_image()
        results = analyze_image(filename)
        params = {'results': results, 'filename': filename}

    return render_template('index_no_ajax.html', **params)


def analyze_image(filename):
    image_path = os.path.join(UPLOAD_DIR, filename)
    with open(image_path, 'rb') as image_file:
        image_content = image_file.read()
        results = {'aws': analyze_image_aws(image_path, image_file, image_content),
                   'gcp': analyze_image_gcp(image_path, image_file, image_content),
                   'azure': analyze_image_azure(image_path, image_file, image_content)}
        return results


if __name__ == '__main__':
    app.run()
