
import urllib2
import StringIO
import json
import re

BASE_URL = "http://wedata.net/databases/LDRFullFeed/"
DEFAULT_XPATH = {
    "enc":"",
    "xpath": "//body"
    }

def download(path):
    data = urllib2.urlopen(BASE_URL + "items.json").read()
    fp = open(path, "w")
    fp.write(data)
    fp.close()

def load(path):
    if path:
        fp = open(path)
    else:
        data = urllib2.urlopen(BASE_URL + "items.json").read()
        fp = StringIO.StringIO(data)
    result = json.load(fp)
    fp.close()
    
    return _purify(result)

def _purify(data):
    return [item["data"] for item in data]

def match(data, url):
    for item in data:
        if re.match(item["url"], url):
            return item
    return DEFAULT_XPATH


