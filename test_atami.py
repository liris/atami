import unittest
import atami

import subscription.file_source as fs

class EngineTest(unittest.TestCase):
    def testSomething(self):
        environ = {
            "max_thread": 32,
            "subscription.filepath": "subscription/data/test_urls.txt",
            "filter.ldrfullfeed.path":"pass",
            }
        filters = [fs.regist_filter(environ,
                                    {"subscription.filepath": "subscription/data/test_urls.txt"})]
        for i in range(3):
            def get_filter(findex):
                def filter(context):
                    print "context: " + str(context[0])
                    print findex
                    return context
                return filter
            filters.append(get_filter(i))
        engine = atami.AtamiEngine(environ)
        engine.set_filters(filters)
        engine.run()

    def testLoadModule(self):
        environ = {"plugin.path": ["test"]}
        filters = [{"module": "testfilter.nothing_filter",
                    "option": {},
                    },
                   {"module": "testfilter.nothing_filter",
                    "option": {},
                    },
                   {"module": "subscription.rss_loader",
                    "option": {},
                    }
                   ]
        filter_funcs =  atami.load_filters(environ, filters)
        self.assertNotEquals(filter_funcs[0], None)
        self.assertNotEquals(filter_funcs[1], None)
        self.assertNotEquals(filter_funcs[2], None)

if __name__ == "__main__":
    unittest.main()
