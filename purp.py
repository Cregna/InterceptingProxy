
import sys
import argparse
if sys.version_info.major < 3:
    print("Purp supports only Python3. Rerun application in Python3 environment.")
    exit(0)

from InterceptingProxy.interpreter import Starting

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--intercepting", help="Start Purp in intercepting mode",action="store_true")
args = parser.parse_args()
def purp():
    purp = Starting
    if args.intercepting:
        purp.start('intercepting')
    else:
        purp.start()
1

if __name__ == "__main__":
    purp()
