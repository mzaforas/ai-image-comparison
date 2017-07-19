import os

from PIL import Image, ImageDraw
import boto3


def analyze_image_aws(image_path, image_file, image_content):
    client = boto3.client('rekognition')

    faces = client.detect_faces(Image={'Bytes': image_content}, Attributes=['ALL']).get('FaceDetails')
    for face_id, face in enumerate(faces, start=1):
        face['img'] = highlight_faces(image_path, image_file, face, face_id)

    results = {'labels': client.detect_labels(Image={'Bytes': image_content}, MaxLabels=10),
               'faces': faces}
    return results


def highlight_faces(image_path, image_file, face, face_id):
    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)

    box = make_box(image,
                   face['BoundingBox']['Left'],
                   face['BoundingBox']['Top'],
                   face['BoundingBox']['Width'],
                   face['BoundingBox']['Height'])

    draw.line(box + [box[0]], width=5, fill='#ffff00')

    dirname = os.path.dirname(image_path)
    orig_filename, ext = os.path.splitext(os.path.basename(image_path))
    filename = '{}_aws_{}{}'.format(orig_filename, face_id, ext)
    image.save(os.path.join(dirname, filename))
    return filename


def make_box(image, left, top, box_width, box_height):
    width, height = image.size
    box = [(left * width, top * height),
           (left * width + box_width * width, top * height),
           (left * width + box_width * width, top * height + box_height * height),
           (left * width, top * height + box_height * height)]
    return box
