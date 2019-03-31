from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
import os
import io
from pymongo import MongoClient
from bson import json_util, ObjectId
import json
from PIL import Image
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision import types

app = Flask(__name__)

# Headers for requests
agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
url = "https://www.medplusmart.com/product/"

# Mongo Stuff
client = MongoClient('localhost', 27017)
db = client['walmart-labs']
cart = db['card']
history = db['history']

# Cloud Vision
credentials = service_account.Credentials. from_service_account_file('../assets/walmart.json')
client = vision.ImageAnnotatorClient(credentials=credentials)


@app.route('/api/medicine/<query>/', methods=['GET'])
def getMedicineList(query):
    page = requests.get(url + query, headers=agent).text
    soup = BeautifulSoup(page, 'html.parser')

    meds = soup.select(".wbrk")
    price = soup.select(".cursor td:nth-of-type(3)")

    count = -1
    medList = []
    for med in meds:
        count += 1
        link = med.select("a")
        if(len(link) != 0):
            link = link[0].attrs['href']
        else:
            link = ""

        if(link == "" or med.text == ""):
            pass
        else:
            temp = {
                "name": med.text.strip(),
                "link": link.strip(),
                "price": price[count].text.strip().replace("\t", "")
            }

            medList.append(temp)

    return jsonify({'medList': medList})


@app.route("/api/medicine/data", methods=['POST'])
def getIndividualMedicineData():
    url = "https://www.medplusmart.com" + request.json['url']
    page = requests.get(url, headers=agent).text

    soup = BeautifulSoup(page, 'html.parser')

    labels = soup.select(".col-xs-4")
    values = soup.select(".col-xs-8")

    data = {}

    medicine_details = {}
    medicine_information = {}
    medicine_alternatives = []

    for i in range(0, len(labels) - 2):
        medicine_details[labels[i].text.strip().replace("\n", " ").replace("\t", "")] = values[i].text.strip().replace("\n", " ").replace("\t", "")

    details = soup.select(".color-blue")
    answers = soup.select(".color-blue + p")

    for i in range(0, len(answers)):
        medicine_information[details[i].text.strip()] = answers[i].text.strip()

    titles = soup.select(".col-xs-12 .table-responsive")
    cursor = titles[0].select(".cursor")

    for c in cursor:
        alt_data = c.text.strip().replace("\n", ",").replace(",,", ",").split(",")

        for i in range(0, len(alt_data)):
            temp = {
                "medicine_name": alt_data[0],
                "manufacturer": alt_data[1],
                "form": alt_data[2],
                "pack_size": alt_data[3],
                "prize": alt_data[5]
            }
            if(alt_data[5] == "INR"):
                continue

        medicine_alternatives.append(temp)

    data = {
        "medicine_details": medicine_details,
        "medicine_information": medicine_information,
        "name": request.json['url'].split("/")[2],
        "medicine_alternatives": medicine_alternatives
    }

    return jsonify(data)


@app.route("/api/user/cart", methods=['GET'])
def getCart():
    arr = []
    for c in cart.find():
        arr.append(json.loads(json_util.dumps(c)))

    arr2 = []
    for c in history.find():
        arr2.append(json.loads(json_util.dumps(c)))

    return jsonify({'data': arr, 'data2': arr2})


@app.route("/api/user/cart", methods=['POST'])
def postCart():
    data = {
        "hello": "hello"
    }

    # data = request.json['']
    cart.insert_one(data)

    return "Done Inserting"


@app.route("/api/user/cart", methods=['DELETE'])
def buy():
    arr = []
    for c in cart.find():
        # print(json.loads(json_util.dumps(c)))
        data_dict = json.loads(json_util.dumps(c))
        del data_dict["_id"]
        print(data_dict)
        history.insert_one(data_dict)

    # print(arr)
    cart.drop()
    # history.insert_many(arr)

    return "Done Bro"


@app.route("/api/prescription/upload", methods=['POST'])
def uploadPrescription():
    file = request.files['file']
    file.save(os.path.join('../assets/uploaded_prescription/', file.filename))
    imageObject = Image.open("../assets/uploaded_prescription/" + file.filename)

    data_to_return = {}

    doctors_name = imageObject.crop((10, 100, 1000, 500))
    registration_number = imageObject.crop((1100, 150, 1900, 300))
    email = imageObject.crop((1500, 410, 2150, 500))
    doctors_sig = imageObject.crop((10, 2700, 1000, 3000))
    stamp = imageObject.crop((1100, 2000, 1900, 2500))

    prsp1 = imageObject.crop((100, 910, 1400, 1170))
    prsp2 = imageObject.crop((100, 1170, 1400, 1410))
    prsp3 = imageObject.crop((100, 1410, 1400, 1620))
    prsp4 = imageObject.crop((100, 1620, 1400, 1830))
    prsp5 = imageObject.crop((100, 1830, 1400, 2070))

    dosage1 = imageObject.crop((1400, 910, 2100, 1170))
    dosage2 = imageObject.crop((1400, 1170, 2100, 1410))
    dosage3 = imageObject.crop((1400, 1410, 2100, 1620))
    dosage4 = imageObject.crop((1400, 1620, 2100, 1830))
    dosage5 = imageObject.crop((1400, 1830, 2100, 2070))

    doctors_name.save("../assets/all_data/doctors_name.jpg")
    registration_number.save("../assets/all_data/registration_number.jpg")
    email.save("../assets/all_data/email.jpg")
    doctors_sig.save("../assets/all_data/doctors_sig.jpg")
    stamp.save("../assets/all_data/stamp.jpg")

    prsp1.save("../assets/all_data/prsp1.jpg")
    prsp2.save("../assets/all_data/prsp2.jpg")
    prsp3.save("../assets/all_data/prsp3.jpg")
    prsp4.save("../assets/all_data/prsp4.jpg")
    prsp5.save("../assets/all_data/prsp5.jpg")

    dosage1.save("../assets/all_data/dosage1.jpg")
    dosage2.save("../assets/all_data/dosage2.jpg")
    dosage3.save("../assets/all_data/dosage3.jpg")
    dosage4.save("../assets/all_data/dosage4.jpg")
    dosage5.save("../assets/all_data/dosage5.jpg")

    names_arr = ["doctors_name.jpg", "registration_number.jpg", "email.jpg", "doctors_sig.jpg", "stamp.jpg",
                 "prsp1.jpg", "prsp2.jpg", "prsp3.jpg", "prsp4.jpg", "prsp5.jpg", "dosage1.jpg", "dosage2.jpg",
                 "dosage3.jpg", "dosage4.jpg", "dosage5.jpg"]

    for name in names_arr:
        file_name = "../assets/all_data/" + name
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        if(len(texts) != 0):
            print(name, texts[0].description)
        else:
            print(name, "")

    return "Uploaded File"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
