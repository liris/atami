
FITLER_TITLE_PREFIX = ["PR: ", "AD: "]
AD_FILTER_KEY = "ad_filter"

def regist_filter(global_config, options):
    prefixes = options.get("prefix") if options else FITLER_TITLE_PREFIX
    if not prefixes:
        prefxes = FITLER_TITLE_PREFIX
        
    def filter_by_title(context):
        index, feed = context
        for entry in feed["entries"]:
            for prefix in prefixes:
                if entry["title"].startswith(prefix):
                    entry[AD_FILTER_KEY] = 1
                    break
            else:
                entry[AD_FILTER_KEY] = 0
        return context

    return filter_by_title
