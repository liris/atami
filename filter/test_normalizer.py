import sys
sys.path.append("..")

import unittest
import normalizer

class NormalizerTest(unittest.TestCase):
    def testNormalize(self):
        normalize = normalizer.regist_filter(None, None)
        data = {"entries": [
            {"content":[{
                "type": "text/plain",
                "value": "hogehoge"}],
             "link": "http://blog.liris.org/2010/04/lxml.html",
             "updated": u"today",
             "published": u"yesterday"
             },
            {"summary_detail":{
                "type": "text/plain",
                "value": "ad filter"},
             "link": "http://blog.liris.org/2010/04/lxml.html",
             "updated": u"today",
             "ad_filter": 1
             },
            {
             "link": "http://blog.liris.org/2010/04/lxml.html",
             "published": u"yesterday"
             },
            {
             "link": "http://blog.liris.org/2010/04/lxml.html"
             },
            ]}
        index, result = normalize((1, data))
        el = result["entries"]
        self.assertEquals(el[0]["content"][0],
                          {"type": "text/plain", "value": "hogehoge"})
        self.assertEquals(type(el[0]["published"]), str)
        self.assertEquals(type(el[0]["updated"]), str)
        self.assertEquals(el[0]["published"], "yesterday")
        self.assertEquals(el[0]["updated"], "today")

        self.assertEquals(el[1]["content"][0],
                          {"type": "text/plain", "value": "ad filter"})
        self.assertEquals(type(el[1]["published"]), str)
        self.assertEquals(type(el[1]["updated"]), str)
        self.assertNotEquals(el[1]["published"], "yesterday")
        self.assertEquals(el[1]["published"], "today")
        self.assertEquals(el[1]["updated"], "today")

        self.assertEquals(el[2]["content"][0],
                          {"type": "text/html", "value": ""})
        self.assertEquals(type(el[2]["published"]), str)
        self.assertEquals(type(el[2]["updated"]), str)
        self.assertNotEquals(el[2]["published"], el[2]["updated"])
        self.assertEquals(el[2]["published"], "yesterday")
        self.assertNotEquals(el[2]["updated"], "")

        self.assertEquals(type(el[3]["published"]), str)
        self.assertEquals(type(el[3]["updated"]), str)
        self.assertEquals(el[3]["published"], el[3]["updated"])
        self.assertNotEquals(el[2]["published"], "")


if __name__ == "__main__":
    unittest.main()
