
from datetime import datetime
def to_str(s):
    if type(s) == unicode:
        return s.encode("utf-8")
    return s

def now():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')


def regist_filter(global_config, options):
    def filter_by_title(context):
        index, feed = context
        for entry in feed["entries"]:
            updated = to_str(entry.get("updated"))
            if not updated:
                updated = now()
            entry["updated"] = updated
                
            published = to_str(entry.get("published"))
            if not published:
                entry["published"] = updated
            else:
                entry["published"] = published

            content_list = entry.get("content")
            if not content_list:
                summary_detail = entry.get("summary_detail")
                if summary_detail:
                    entry["content"] = [summary_detail]
                else:
                    entry["content"] = [{"type": "text/html",
                                         "value": ""}]
            else:
                content = content_list[0]
                if content["type"] == "application/xhtml+xml":
                    content["type"] = "text/html"
                    
            
        return context

    return filter_by_title
