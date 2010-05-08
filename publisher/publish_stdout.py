
def regist_filter(global_config, options):
    def dump(context):
        print "#"*70
        index, feed = context
        for entry in feed.entries:
            print entry.link
            print entry.title.encode("utf-8")
            print entry["full_content"]["value"].encode("utf-8")
            print "-" * 70
        return context
    return dump
