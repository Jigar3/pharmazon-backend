import io
import os
from google.oauth2 import service_account
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

credentials = service_account.Credentials. from_service_account_file('../assets/walmart.json')


client = vision.ImageAnnotatorClient(credentials=credentials)

file_name = "../assets/all_data/doctors_name.jpg"

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

# try:
image = vision.types.Image(content=content)
response = client.text_detection(image=image)
texts = response.text_annotations

# print('Texts:')

print(texts[0].description.strip())

# except:
#     print("kat gaya")
# import requests

# subscription_key = "d7dcc3f8dbbd44dea57f3ecfb039363e"
# assert subscription_key

# vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

# text_recognition_url = vision_base_url + "read/core/asyncBatchAnalyze"

# # Set image_url to the URL of an image that you want to analyze.
# image_path = "/home/jigar/walmart-labs/pharmazon-backend/playground/image.png"
# image_data = open(image_path, "rb").read()

# headers = {'Ocp-Apim-Subscription-Key': subscription_key}
# # Note: The request parameter changed for APIv2.
# # For APIv1, it is 'handwriting': 'true'.
# params = {'mode': 'Handwritten'}
# data = {'url': image_data}
# response = requests.post(
#     text_recognition_url, headers=headers, params=params, json=data)
# # response.raise_for_status()

# print(dir(response))
# print(response.text)