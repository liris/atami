#! env python

import gevent
from gevent import monkey
monkey.patch_all()

# threading.local additional patch
# http://code.google.com/p/gevent/issues/detail?id=24
import threading
import thread
threading.local = thread._local

import sys
import os.path
import imp

CURRENT_FILE_DIR  = os.path.abspath(os.path.dirname(__file__))



"""
gobal
 - max_thread : max thread size
 - plugin.path : plugin directory. default is current directory. "."
   and atami directory is always added as plugin directory.
 - filter.ldrfullfeed.path 

"""

class AtamiEngine:
    def __init__(self, global_config):
        self.max_thread = int(global_config.get("max_thread", 4))
        self.global_config = global_config
        
    def set_filters(self, filters):
        self.filters = filters

    def run_chain(self, filters, context):
        try:
            for f in filters:
                if self.global_config.get("verbose"):
                    print "filter run %d %s" % (context[0], f)
                context = f(context)
                if not context:
                    if self.global_config.get("verbose"):
                        print "filter chain finished. %d %s" % (context[0], f)
                        break
        except Exception, e:
            print e
            
    def run(self):
        if not self.filters:
            return
        filters = [f for f in self.filters]
        f = filters.pop(0)
        fetch_list = f(None)
        def run_filters():
            while len(fetch_list):
                context = fetch_list.pop(0)
                self.run_chain(filters, context)
        if fetch_list:
            thread_size = min(len(fetch_list), self.max_thread)
            jobs = [gevent.spawn(run_filters) for i in range(thread_size)]
            gevent.joinall(jobs)
        

def load_config(filename):
    import yaml
    config = yaml.load(open(filename).read().decode("utf-8"))
    return  config.get("global"), config.get("filters")

def load_filters(global_config, filters):
    filter_funcs = []
    plugin_path = global_config.get("plugin.path")
    if not plugin_path:
        plugin_path = ["."]
    if CURRENT_FILE_DIR not in plugin_path:
        plugin_path.append(CURRENT_FILE_DIR)
    
    for  config in filters:
        mod = load_module(config["module"], plugin_path)
        func = mod.regist_filter(global_config, config.get("option"))
        filter_funcs.append(func)
    return filter_funcs

module_cache = {}

def load_module(module_name, plugin_path):
    parents = module_name.split(".")
    sub_modules = None
    module_path = plugin_path
    for name in module_name.split("."):
        if sub_modules:
            sub_modules = sub_modules + "." + name
        else:
            sub_modules = name

        module = module_cache.get(sub_modules)
        if not module:
            info = imp.find_module(name, module_path)
            module = imp.load_module(sub_modules, *info)
            module_cache[sub_modules] = module
        module_path = [path + "/" + name for path in module_path]
    return module
                               
def main(options, args):
    global_config, filters = load_config(options.filename)
    engine = AtamiEngine(global_config)
    engine.set_filters(load_filters(global_config, filters))
    engine.run()
    


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(version="atami 0.3")
    parser.add_option("-f", "--file", dest="filename",
                      default="atami.yaml",
                      help="set the configuration yaml file")
    options, args = parser.parse_args()
    main(options, args)
