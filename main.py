import requests
from bs4 import BeautifulSoup
import os
import concurrent.futures


def download(images, search):
    for item in images:
        url = str(item).split("url")[1].split("\"")[2]
        print(url)
        try:
            img_bytes = requests.get(url, timeout=2).content
            img_name = url.split('/')[-1]
            with open('./out/' + search+'/' + img_name, 'wb') as img_file:
                img_file.write(img_bytes)
                print("done")
        except:
            print("failed")


def search():
    search = input("search: ")
    search = search.replace(" ", "_")
    params = {"text": search}
    if not os.path.isdir(search):
        os.mkdir('./out/'+search)
    headers = {
        'Accept-Language': 'en-US,en;q=0.5'
    }

    r = requests.get("https://yandex.com/images/search", headers=headers, params=params)
    print(r.url)
    soup = BeautifulSoup(r.text, "html.parser")
    images = []
    for j in range(1, 4):
        for i in range(j-1*5, j*5):
            images.append(soup.find_all("div", {
                'class': 'serp-item serp-item_type_search serp-item_group_search serp-item_pos_' + str(
                    i) + ' serp-item_scale_yes justifier__item i-bem'}))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(lambda images: download(images, search), images)


search()
