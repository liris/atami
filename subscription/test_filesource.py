
import unittest
import file_source as fs


class FileSubscrptionTest(unittest.TestCase):
    def testRegist(self):
        fs_reader = fs.regist_filter(None, None)
        self.assertNotEqual(fs_reader, None)

    def testLoad(self):
        fs_reader = fs.regist_filter(None,
                                     {fs.FILEPATH_KEY: "data/test_urls.txt"})
        urls = fs_reader(None)
        self.assertEquals(urls, [("1", "http://www.google.com/"),
                                 ("2", "http://www.yahoo.com/")])
    def testLoadFail(self):
        fs_reader = fs.regist_filter(None, {fs.FILEPATH_KEY: "test_no_file.txt"})
        self.assertRaises(IOError, fs_reader, None)
        fs_reader = fs.regist_filter(None, {})
        self.assertRaises(KeyError, fs_reader, None)
        fs_reader = fs.regist_filter(None, None)
        self.assertRaises(TypeError, fs_reader, None)

if __name__ == "__main__":
    unittest.main()
