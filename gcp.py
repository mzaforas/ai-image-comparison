import os
from collections import OrderedDict

from PIL import Image, ImageDraw
from google.cloud import vision


def analyze_image_gcp(image_path, image_file, image_content):
    # Get GCP client
    client = vision.Client()
    image = client.image(content=image_content)

    # Call GCP to detect labels
    raw_labels = image.detect_labels()
    dict_labels = {label.description: label.score for label in raw_labels}
    ordered_labels = OrderedDict(sorted(dict_labels.items(), key=lambda t: t[1], reverse=True))

    # Call GCP to detect faces and transform to convenient dictionary
    faces = image.detect_faces()

    faces_features = [{'roll_angle': face.angles.roll,
                       'pan_angle': face.angles.pan,
                       'tilt_angle': face.angles.tilt,
                       'detection_confidence': face.detection_confidence,
                       'landmarking_confidence': face.landmarking_confidence,
                       'joy': face.joy,
                       'sorrow': face.sorrow,
                       'anger': face.anger,
                       'surprise': face.surprise,
                       'under_exposed': face.image_properties.underexposed,
                       'blurred': face.image_properties.blurred,
                       'headwear': face.headwear,
                       'img': highlight_faces(image_path, image_file, face, face_id)}
                      for face_id, face in enumerate(faces, start=1)]

    results = {'labels': ordered_labels, 'faces': faces_features}

    return results


def highlight_faces(image_path, image_file, face, face_id):
    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)

    box = [(bound.x_coordinate, bound.y_coordinate) for bound in face.bounds.vertices]
    draw.line(box + [box[0]], width=5, fill='#00ff00')

    dirname = os.path.dirname(image_path)
    orig_filename, ext = os.path.splitext(os.path.basename(image_path))
    filename = '{}_gpc_{}{}'.format(orig_filename, face_id, ext)
    image.save(os.path.join(dirname, filename))
    return filename
