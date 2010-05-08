
import os, os.path
import unittest

if __name__ == "__main__":
    curdir = os.path.abspath(os.curdir)
    print curdir
    for dirname, dirs, files in os.walk("."):
        for name in files:
            os.chdir(dirname)
            if name.startswith("test_") and name.endswith(".py") and name != "test_all.py":
                print "#" * 78
                print dirname + "/" + name
                os.system("python " + name)
                
            os.chdir(curdir)
