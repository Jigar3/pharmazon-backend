import io
import os
from google.oauth2 import service_account
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
credentials = service_account.Credentials. from_service_account_file('../assets/walmart.json')

client = vision.ImageAnnotatorClient(credentials=credentials)


# Instantiates a client
# client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    './image2.png')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.text_detection(image=image)
texts = response.text_annotations
print('Texts:')

for text in texts:
    print('\n"{}"'.format(text.description))

    # vertices = (['({},{})'.format(vertex.x, vertex.y)
    #             for vertex in text.bounding_poly.vertices])

    # print('bounds: {}'.format(','.join(vertices)))