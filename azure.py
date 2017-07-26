import os

from PIL import Image, ImageDraw
import cognitive_face as cf
import requests


def analyze_image_azure(image_path, image_file, image_content):
    labels = detect_labels(image_content)

    faces = detect_faces(image_path, image_file)

    return {'faces': faces, 'labels': labels}


def detect_labels(image_content):
    url = 'https://westeurope.api.cognitive.microsoft.com/vision/v1.0/tag'
    params = {'visualFeatures': 'Color,Categories'}

    headers = {'Ocp-Apim-Subscription-Key': os.environ.get('AZURE_VISION_KEY'),
               'Content-Type': 'application/octet-stream'}

    response = requests.post(url, data=image_content, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get('tags')


def detect_faces(image_path, image_file):
    cf.Key.set(os.environ.get('AZURE_FACE_KEY'))
    cf.BaseUrl.set('https://westeurope.api.cognitive.microsoft.com/face/v1.0/')

    attributes = ['age',
                  'gender',
                  'headPose',
                  'smile',
                  'facialHair',
                  'glasses',
                  'emotion',
                  'hair',
                  'makeup',
                  'occlusion',
                  'accessories',
                  'blur',
                  'exposure',
                  'noise']

    image_file.seek(0)
    faces = cf.face.detect(image_file, attributes=','.join(attributes))

    for face_id, face in enumerate(faces, start=1):
        highlight_image = highlight_faces(image_path, image_file, face, face_id)
        face['img'] = highlight_image

    return faces


def highlight_faces(image_path, image_file, face, face_id):
    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)

    face_rectangle = face['faceRectangle'] 
    box = make_box(face_rectangle['left'], face_rectangle['top'], face_rectangle['width'], face_rectangle['height'])
    draw.line(box + [box[0]], width=5, fill='#0000ff')

    dir_name = os.path.dirname(image_path)
    orig_filename, ext = os.path.splitext(os.path.basename(image_path))
    filename = '{}_azure_{}{}'.format(orig_filename, face_id, ext)
    image.save(os.path.join(dir_name, filename))
    return filename


def make_box(left, top, width, height):
    box = [(left, top),
           (left + width, top),
           (left + width, top + height),
           (left, top + height)]
    return box
