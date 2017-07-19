import os

from PIL import Image, ImageDraw
import cognitive_face as cf
import requests


def analyze_image_azure(image_path, image_file, image_content):
    return {'faces': detect_faces(image_path, image_file, image_content),
            'labels': detect_labels(image_path, image_file, image_content)}


def detect_labels(image_path, image_file, image_content):
    url = 'https://westeurope.api.cognitive.microsoft.com/vision/v1.0/tag'
    params = {'visualFeatures': 'Color,Categories'}

    headers = {'Ocp-Apim-Subscription-Key': os.environ.get('AZURE_VISION_KEY'),
               'Content-Type': 'application/octet-stream'}

    response = requests.post(url, data=image_content, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get('tags')


def detect_faces(image_path, image_file, image_content):
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

    dirname = os.path.dirname(image_path)
    orig_filename, ext = os.path.splitext(os.path.basename(image_path))
    filename = '{}_azure_{}{}'.format(orig_filename, face_id, ext)
    image.save(os.path.join(dirname, filename))
    return filename


def make_box(left, top, width, height):
    box = [(left, top),
           (left + width, top),
           (left + width, top + height),
           (left, top + height)]
    return box
#
# {'faces': [{'faceRectangle': {'top': 239, 'left': 596, 'width': 281, 'height': 281}, ''
#     faceAttributes': {'occlusion': {'mouthOccluded': False, 'eyeOccluded': False, 'foreheadOccluded': False}, '
#                                                                                                    ''noise': {'value': 0.18, 'noiseLevel': 'low'},'
#  'gender': 'male',
# 'emotion': {'surprise': 0.001, 'disgust': 0.004, 'contempt': 0.013, 'anger': 0.83, 'happiness': 0.0, 'sadness': 0.004, 'neutral': 0.148, 'fear': 0.001},
#             'glasses': 'NoGlasses',
#             'makeup': {'eyeMakeup': True, 'lipMakeup': False},
#             'hair': {'invisible': False, 'hairColor': [{'confidence': 0.97, 'color': 'other'},
#                                                        {'confidence': 0.61, 'color': 'blond'},
#                                                        {'confidence': 0.45, 'color': 'black'}, {
#                                                            'confidence': 0.24, 'color': 'gray'},
#                                                        {'confidence': 0.24, 'color': 'brown'},
#                                                        {'confidence': 0.2, 'color': 'red'}],
#                      'bald': 0.01}, 'age': 43.0, 'smile': 0.0,
#
#             'exposure': {'exposureLevel': 'goodExposure', 'value': 0.38},
#             'facialHair': {'beard': 0.0, 'sideburns': 0.2, 'moustache': 0.0},
#             'blur': {'blurLevel': 'low', 'value': 0.12},
#             'accessories': [],
#             'headPose': {'roll': 4.4, 'yaw': -0.6, 'pitch': 0.0}}, 'faceId': '852e3b58-6a0d-4db5-a87b-372d83a84cc9'}]}