import unittest
import rss_loader

class RssLoaderTest(unittest.TestCase):
    def testLoad(self):
        loader = rss_loader.regist_filter(None, None)
        # index, feed = loader(("myfeed", "http://blog.liris.org/feeds/posts/default"), None)
        index, feed = loader(("myfeed", "data/liris.rss"))
        self.assertEqual(index, "myfeed")
        self.assertNotEqual(feed, None)
        self.assertEqual(feed.bozo, 0)

    def testLoadHtml(self):
        loader = rss_loader.regist_filter(None, None)
        index, feed = loader(("myfeed", "data/invalid.html"))
        self.assertEqual(index, "myfeed")
        self.assertNotEqual(feed, None)
        self.assertNotEqual(feed.bozo, 0)
        self.assertEqual(feed.version, "")
        
        index, feed = loader(("myfeed", "data/valid.html"))
        self.assertEqual(index, "myfeed")
        self.assertNotEqual(feed, None)
        self.assertEqual(feed.bozo, 0)
        self.assertEqual(feed.version, "")
        

if __name__ == "__main__":
    unittest.main()
