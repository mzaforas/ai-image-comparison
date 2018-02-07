import os
from collections import OrderedDict

from PIL import Image, ImageDraw
from google.cloud import vision
from google.cloud.vision import types, enums


def analyze_image_gcp(image_path, image_file, image_content):
    # Get GCP client
    # client = vision.ImageAnnotatorClient(project='bigdata-154709')
    client = vision.ImageAnnotatorClient()
    image = types.Image(content=image_content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    raw_labels = response.label_annotations

    # image = client.image(content=image_content)

    # Call GCP to detect labels
    # raw_labels = image.detect_labels()
    dict_labels = {label.description: label.score for label in raw_labels}
    ordered_labels = OrderedDict(sorted(dict_labels.items(), key=lambda t: t[1], reverse=True))

    # Call GCP to detect faces and transform to convenient dictionary
    # faces = image.detect_faces()
    faces = client.face_detection(image=image)
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    faces_features = [{'roll_angle': face.roll_angle,
                       'pan_angle': face.pan_angle,
                       'tilt_angle': face.tilt_angle,
                       'detection_confidence': face.detection_confidence,
                       'landmarking_confidence': face.landmarking_confidence,
                       'joy': likelihood_name[face.joy_likelihood],
                       'sorrow': likelihood_name[face.sorrow_likelihood],
                       'anger': likelihood_name[face.anger_likelihood],
                       'surprise': likelihood_name[face.surprise_likelihood],
                       'under_exposed': likelihood_name[face.under_exposed_likelihood],
                       'blurred': likelihood_name[face.blurred_likelihood],
                       'headwear': likelihood_name[face.headwear_likelihood],
                       'img': highlight_faces(image_path, image_file, face, face_id)}
                      for face_id, face in enumerate(faces.face_annotations, start=1)]

    results = {'labels': ordered_labels, 'faces': faces_features}

    return results


def highlight_faces(image_path, image_file, face, face_id):
    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)

    box = [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices]
    draw.line(box + [box[0]], width=5, fill='#00ff00')

    dirname = os.path.dirname(image_path)
    orig_filename, ext = os.path.splitext(os.path.basename(image_path))
    filename = '{}_gpc_{}{}'.format(orig_filename, face_id, ext)
    image.save(os.path.join(dirname, filename))
    return filename
