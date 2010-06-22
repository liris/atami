import sys
sys.path.append("..")

import unittest
import content_fetcher


class FetcherTest(unittest.TestCase):
    def testFetch(self):
        fetch = content_fetcher.regist_filter(
            {"filter.ldrfullfeed.path":"data/test.json"}, None)
        data = {"entries": [
            {"content":[{
                "type": "text/plain",
                "value": "hogehoge"}],
             "link": "http://blog.liris.org/2010/04/lxml.html"
             },
            {"content":[{
                "type": "text/plain",
                "value": "ad filter"}],
             "link": "http://blog.liris.org/2010/04/lxml.html",
             "ad_filter": 1
             },
            {"content":[{
                "type": "text/html",
                "value": "html value"}],
             "link": "http://blog.liris.org/2010/04/lxml.html"
             },
            {"summary_detail":{"value":"text value",
                               "type": "text/html"},
             "link": "http://blog.liris.org/2010/04/lxml.html"
             },
            ]}
        index, result = fetch(("myfeed", data))
        entries = result["entries"]
        self.assertNotEquals(entries[0]["full_content"]["value"],
                             entries[0]["content"][0]["value"])
        self.assertEquals(entries[1]["full_content"]["value"], "ad filter")
        self.assertNotEquals(entries[2]["full_content"]["value"], "html value")
        self.assertNotEquals(entries[3]["full_content"]["value"], "text value")
        self.assertEquals(entries[3]["summary_detail"]["value"], "text value")

    def testFetchReal(self):
        fetch = content_fetcher.regist_filter(
            {"filter.ldrfullfeed.path":"../fullfeed.json"}, None)
        data = {"entries": [
            {"content":[{
                "type": "text/plain",
                "value": "plain"}],
             "link": "http://www.publickey1.jp/blog/10/2_3.html"
             },
            ]}
        index, result = fetch(("myfeed", data))
        entries = result["entries"]
        self.assertEquals(entries[0]["default_feed"], "full_content")


if __name__ == "__main__":
    unittest.main()
