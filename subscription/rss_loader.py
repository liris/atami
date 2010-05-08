import feedparser

"""
load rss
load function:
  param context is tuple(index, url).
  options is no meaning.
  the result is tuple, containing index and the object parsed by feedparser
"""

def regist_filter(global_config, options):
    def load(context):
        index, url = context
        feed = feedparser.parse(url)
        return (index, feed)

    return load
