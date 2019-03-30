from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
import os
from pymongo import MongoClient
from bson import json_util, ObjectId
import json

app = Flask(__name__)

# Headers for requests
agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
url = "https://www.medplusmart.com/product/"

# Mongo Stuff
client = MongoClient('localhost', 27017)
db = client['walmart-labs']
cart = db['card']
history = db['history']


@app.route('/medicine/<query>/', methods=['GET'])
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


@app.route("/medicine/data", methods=['POST'])
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


@app.route("/user/cart", methods=['GET'])
def getCart():
    arr = []
    for c in cart.find():
        arr.append(json.loads(json_util.dumps(c)))

    return jsonify({'data': arr})


@app.route("/user/cart", methods=['POST'])
def postCart():
    # data = {
    #     "hello": "hello"
    # }

    data = request.json['']
    cart.insert_one(data)

    return "Done Inserting"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
