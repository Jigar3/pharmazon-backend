from bs4 import BeautifulSoup
import requests
agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

# page = requests.get("https://www.medplusmart.com/product/oflox", headers=agent).text

# # print(page)
# soup = BeautifulSoup(page, 'html.parser')

# med = soup.select(".wbrk")

# for m in med:
#     link = m.select("a")
#     if
#     print(link)
#     print(m.text.strip())

url = "https://www.medplusmart.com/product/OFLOX-200MG-TAB/OFLO0010"
page = requests.get(url, headers=agent).text

soup = BeautifulSoup(page, 'html.parser')

# labels = soup.select(".col-xs-4")
# values = soup.select(".col-xs-8")

# print(len(labels), len(values))

# for i in range(0, len(labels) - 2):
#     print(labels[i].text.strip().replace("\n", " "), values[i].text.strip().replace("\n", " "))

# details = soup.select(".color-blue")
# answers = soup.select(".color-blue + p")

# for i in range(0, len(answers)):
#     print(details[i].text.strip(), answers[i].text.strip())

# print(len(details), len(values))
# for detail in details:
#     print(detail.text.strip())

# for value in values:
#     print(value.text.strip())

titles = soup.select(".col-xs-12 .table-responsive")

cursor = titles[0].select(".cursor")

for c in cursor:
    x = c.text.strip().replace("\n", ",").replace(",,", ",")
    y = x.split(",")
    
    for i in range(0, len(y)):
        temp = {
            "medicine_name": y[0],
            "manufacturer": y[1],
            "form": y[2],
            "pack_size": y[3],
            "prize": y[5]
        }

        print(temp)
