from bs4 import BeautifulSoup
import requests

agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
url = "https://www.medplusmart.com/product/"

def getMedList(query):
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

    return medList
