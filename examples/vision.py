from google.cloud import vision
import pprint

client = vision.Client()

BUCKET = 'iniciativa-big-data'
IMAGE_NAME = 'examples/tyrion.jpg'

# Using Storage
# image = client.image(source_uri='gs://{}/{}'.format(BUCKET, IMAGE_NAME))

# Not using Storage
with open(IMAGE_NAME, 'rb') as image_file:
    image = client.image(content=image_file.read())

# Detect faces
response = image.detect_faces()
for face in response:
    pprint.pprint({
        'roll_angle': face.angles.roll,
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
    })


# Detect labels
response = image.detect_labels()
for label in response:
    print(label.description, label.score)
