from distutils.command.install_egg_info import safe_name
from unittest import result
from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os , time , sys

#APIキーの取得
key = "91efa4b95903c5c74ca553e6783d5538"
secret = "c8b2f7b712b2616e"
wait_time = 1

#保存フォルダの指定
animal_name = sys.argv[1]
savedir = "./" + animal_name

flickr = FlickrAPI(key,secret,format="parsed-json")
result = flickr.photos.search(
    text = animal_name,
    per_page = 400,
    media = "photos",
    sort = "relevance",
    extras = "url_q, license",
    )

photos = result["photos"]

for i, photo in enumerate(photos["photo"]):
    url_q = photo["url_q"]
    filepath = "images" + "/" + savedir + "/" + photo["id"] + ".jpg"
    if os.path.exists(filepath):
        continue
    urlretrieve(url_q, filepath)
    time.sleep(wait_time)

