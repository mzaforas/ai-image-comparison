import boto3
import pprint

rekognition = boto3.client('rekognition')

BUCKET = 'iniciativa-big-data'
IMAGE_NAME = 'tyrion2.jpg'

# Using S3

# Detect faces
# response = rekognition.detect_faces(Image={"S3Object": {"Bucket": BUCKET, "Name": IMAGE_NAME}}, Attributes=['ALL'])
# pprint.pprint(response)
#
# # Detect labels
# response = rekognition.detect_labels(Image={"S3Object": {"Bucket": BUCKET, "Name": IMAGE_NAME}})
# pprint.pprint(response)

# Not using S3

with open(IMAGE_NAME, 'rb') as image:
    response = rekognition.detect_labels(Image={'Bytes': image.read()})

pprint.pprint(response)
