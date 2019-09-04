import requests
from PIL import Image
from bs4 import BeautifulSoup
from io import BytesIO
import os


def search():
    search = input("search: ")
    params = {"text": search}
    if not os.path.isdir(search.replace(" ", "_")):
        os.mkdir(search.replace(" ", "_"))
    headers = {
        'Accept-Language': 'en-US,en;q=0.5'
    }
    r = requests.get("https://yandex.com/images/search", headers=headers, params=params)
    print(r.headers)
    print(r.url)
    f = open("search.html", "w")
    f.write(r.text)
    soup = BeautifulSoup(r.text, "html.parser")
    for i in range(50):
        images = soup.find_all("div", {
            'class': 'serp-item serp-item_type_search serp-item_group_search serp-item_pos_' + str(
                i) + ' serp-item_scale_yes justifier__item i-bem'})
        for item in images:
            print(item)
            url = str(item).split("url")[1].split("\"")[2]
            try:
                img = requests.get(url, timeout=2)
                image = Image.open(BytesIO(img.content))
                image.save("./" +search.replace(" ", "_") + "/" + str(i), image.format)
            except:
                print("failed")


search()
