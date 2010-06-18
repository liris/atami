
import gevent
import ldrfullfeed
import ad_filter
import urllib2
import types
from lxml import etree, html

FETCH_TYPES = ["text/plain", "text/html", "text/text"]
                    
def fetch_full(url, get_xitem, default_value):
    default_feed = "original"
    new_url = url
    encoding = "utf-8"
    try:
        obj = urllib2.urlopen(url)
        new_url = obj.url
        xitem = get_xitem(new_url)
        if not xitem.get("default", False):
            default_feed = "full_content"
        encoding = xitem["enc"]
        if not encoding:
            encoding = "utf-8"
        data = obj.read().decode(encoding)
        root = html.fromstring(data)
        elems = root.xpath(xitem["xpath"])
    except Exception, e:
        print e
        try:
            print "ERR: Fetch full feed. xpath(%s) encoding(%s) new_url(%s)" % (xitem["xpath"], encoding, new_url)
        except:
            pass
        elems = None
    
    if not elems:
        return {"value": default_value,
                "type": "text/text"}, default_feed, new_url
    else:
        return {"value": etree.tounicode(elems[0]),
                "type": "text/html"}, default_feed, new_url

def merge(entry, url, get_xitem, default_value):
    result = fetch_full(url, get_xitem, default_value)
    entry["full_content"], entry["default_feed"], entry["link"] = result

def get_content(entry):
    content = entry.get("content")
    if not content:
        content = {"type": "text/text",
                   "value": entry.get("summary", "")}
        entry["content"] = [content]
        return content
    
    return content[0]

def regist_filter(global_config, options):
    data = ldrfullfeed.load(global_config["filter.ldrfullfeed.path"])
    def fetch(context):
        index, feed = context
        if global_config.get("verbose"):
            print "fetching content for %d" % index
        jobs = []
        for entry in feed["entries"]:
            content = get_content(entry)
            if entry.get("full_content"):
                pass
            elif entry.get(ad_filter.AD_FILTER_KEY) or content["type"] not in FETCH_TYPES:
                entry["full_content"] =  {"type": content["type"],
                                         "value": content["value"]}
            else:
                url = entry["link"]
                def get_xitem(fetch_url):
                    return ldrfullfeed.match(data, fetch_url)
                
                jobs.append(gevent.spawn(merge, entry, url, get_xitem, content["value"]))
        gevent.joinall(jobs)
        
        if global_config.get("verbose"):
            print "fetched content for %d" % index
            
        return context

    return fetch
