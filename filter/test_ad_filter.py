import unittest
import ad_filter

class AdFilterTest(unittest.TestCase):
    def testFilter(self):
        afilter = ad_filter.regist_filter(None, None)
        data = {
            "feed": {},
            "entries": [
                {"title": "ok title"},
                {"title": "AD: ad title"},
                {"title": "PR: pr title"},
                {"title": "oAD: k title2"},
                {"title": "oPR: k title2"},
                ],
            }
        index, feed = afilter(("myfeed", data))
        entries = feed["entries"]
        self.assertEquals(entries[0][ad_filter.AD_FILTER_KEY], 0)
        self.assertEquals(entries[1][ad_filter.AD_FILTER_KEY], 1)
        self.assertEquals(entries[2][ad_filter.AD_FILTER_KEY], 1)
        self.assertEquals(entries[3][ad_filter.AD_FILTER_KEY], 0)
        self.assertEquals(entries[4][ad_filter.AD_FILTER_KEY], 0)

if __name__ == "__main__":
    unittest.main()
