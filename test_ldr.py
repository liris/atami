import unittest
import time
import ldrfullfeed

class LdrTest(unittest.TestCase):
    def setUp(self):
        self.data = ldrfullfeed.load("fullfeed.json")
        
    def testMatch(self):
        item = ldrfullfeed.match(self.data, "http://no.match.url/")
        self.assertEqual(item["xpath"], "//body")
        start = time.time()
        item = ldrfullfeed.match(self.data, "http://douganoyoake.blog18.fc2.com/items")
        print "SEARCH TIME: " + str((time.time() - start)*1000) + " msec"
        self.assertEqual(item["xpath"], '//div[(@class="e-text")]')


if __name__ == "__main__":
    unittest.main()
