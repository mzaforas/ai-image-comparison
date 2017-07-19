import cognitive_face as CF

KEY = '60d3074fc5e147a88dc25060a85ec964'
CF.Key.set(KEY)


#BASE_URL = 'https://westeurope.api.cognitive.microsoft.com/vision/v1.0/'
BASE_URL = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)

#img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
IMAGE_NAME = '/home/mzaforas/Descargas/img/tyrion.jpg'
with open(IMAGE_NAME, 'rb') as image_file:
    result = CF.face.detect(image_file, attributes="age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise")
    print(result)
