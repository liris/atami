
FILEPATH_KEY = "subscription.filepath"

def regist_filter(global_config, options):
    def read(context):
        filepath = options[FILEPATH_KEY]
        fp = open(filepath)
        index = 1
        result = []
        for line in fp.readlines():
            line = line.strip()
            if line:
                result.append((index, line))
                index += 1
        fp.close()
        return result

    return read

