import json
import requests

def shorten_url(url):
    short_link_api = "http://mrw.so/api.php?format=json&url={}".format(url)
    short_link =  json.loads(requests.get(short_link_api).text)
    return short_link["url"]
