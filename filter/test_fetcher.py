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
            ]}
        index, result = fetch(("myfeed", data))
        entries = result["entries"]
        self.assertNotEquals(entries[0]["full_content"]["value"],
                             entries[0]["content"][0]["value"])
        self.assertEquals(entries[1]["full_content"]["value"], "ad filter")
        self.assertNotEquals(entries[2]["full_content"]["value"], "html value")



if __name__ == "__main__":
    unittest.main()
